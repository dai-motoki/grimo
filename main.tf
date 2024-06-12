# プロバイダーの設定
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# AWS プロバイダーの設定
provider "aws" {
  region = "ap-northeast-1" # 適宜変更してください
}

# 変数の定義
variable "aws_region" {
  default = "ap-northeast-1" # 適宜変更してください
}

variable "instance_type" {
  default = "t3.micro"
}

variable "env_vars" {
  type = map(string)
  default = {
    SUPABASE_URL = "https://mukjvosxeszasehzsora.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im11a2p2b3N4ZXN6YXNlaHpzb3JhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc3NTEzMzQsImV4cCI6MjAzMzMyNzMzNH0.5saniCzo2ieQ7tPt8AxY9NmzJQlM4cAseogs-rj9Fkw"
    # その他の環境変数
  }
}

# Ubuntu AMI を取得
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "owner-id"
    values = ["099720109477"]
  }

  owners = ["099720109477"]
}

# EC2 インスタンスの設定
resource "aws_instance" "grimo_server" {
  ami           = data.aws_ami.ubuntu.id # <= ここで参照
  instance_type = var.instance_type

  tags = {
    Name = "Grimo Server"
  }

  # ユーザーデータ
  user_data = <<-EOF
#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y python3 git nginx python3-pip

# pip で必要なパッケージをインストール
pip3 install fastapi uvicorn python-multipart boto3 python-dotenv requests supabase python-jose[cryptography]

# server.py をコピーして利用
mkdir /home/ubuntu/grimo-server  # ディレクトリを作成
aws s3 cp s3://my-bucket/server.py /home/ubuntu/grimo-server/server.py

# .env ファイルを作成
cat <<EOL > /home/ubuntu/grimo-server/.env
${join("\n", [for key, value in var.env_vars : "${key}=${value}"])}
EOL

# supervisor をインストール
sudo apt-get install -y supervisor

# supervisor の設定ファイルを作成
cat <<EOL > /etc/supervisor/conf.d/grimo-server.conf
[program:grimo-server]
directory=/home/ubuntu/grimo-server
command=uvicorn server:app --host 0.0.0.0 --port 8000 --env-file .env
autostart=true
autorestart=true
stdout_logfile=/var/log/grimo-server.log
stderr_logfile=/var/log/grimo-server.err.log
EOL

# supervisor を起動
sudo systemctl enable supervisor
sudo systemctl start supervisor

# nginx を設定 (リバースプロキシ)
sudo chown www-data:www-data /etc/nginx/sites-available/grimo-server
sudo rm /etc/nginx/sites-enabled/default
cat <<EOL > /etc/nginx/sites-available/grimo-server
server {
  listen 80;

  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
  }
}
EOL
sudo ln -s /etc/nginx/sites-available/grimo-server /etc/nginx/sites-enabled/
# nginx を起動
sudo systemctl enable nginx
sudo systemctl start nginx
EOF

  # セキュリティグループの設定を追加
  vpc_security_group_ids = [aws_security_group.grimo_server_sg.id]

  # キーペアの設定を追加
  key_name = aws_key_pair.grimo_server_key.key_name
}

# セキュリティグループの設定
resource "aws_security_group" "grimo_server_sg" {
  name = "grimo-server-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol   = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol   = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0 # <= 値を 0 に設定
    to_port     = 0
    protocol   = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# キーペアの設定
resource "aws_key_pair" "grimo_server_key" {
  key_name   = "grimo-server-key"
  public_key = file("~/.ssh/grimo_key.pub") # 生成した公開鍵ファイルのパス
}