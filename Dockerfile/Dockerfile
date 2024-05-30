# Dockerfile
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# Streamlit/Gradioアプリケーションを起動
CMD ["streamlit", "run", "app.py"]
# または
# CMD ["python", "app.py"]

# # docker-compose.yml
# version: '3'

# services:
#   app:
#     build: .
#     ports:
#       - "8501:8501"  # Streamlitの場合
#       # - "7860:7860"  # Gradioの場合
#     volumes:
#       - .:/app
#     environment:
#       - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
#       - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
#       - AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}

#   db:
#     image: postgres:13
#     volumes:
#       - db_data:/var/lib/postgresql/data
#     environment:
#       - POSTGRES_DB=grimo
#       - POSTGRES_USER=grimo
#       - POSTGRES_PASSWORD=grimo

# volumes:
#   db_data:

# # .github/workflows/ci.yml
# name: CI

# on:
#   push:
#     branches: [main]
#   pull_request:
#     branches: [main]

# jobs:
#   build:
#     runs-on: ubuntu-latest

#     steps:
#     - uses: actions/checkout@v3
#     - name: Set up Python
#       uses: actions/setup-python@v4
#       with:
#         python-version: 3.9
#     - name: Install dependencies
#       run: |
#         python -m pip install --upgrade pip
#         pip install -r requirements.txt
#     - name: Lint with flake8
#       run: |
#         flake8 .
#     - name: Test with unittest
#       run: |
#         python -m unittest discover tests
#     - name: Measure coverage
#       run: |
#         pip install coverage
#         coverage run -m unittest discover tests
#         coverage report

# # .github/workflows/cd.yml  
# name: CD

# on:
#   push:
#     tags:
#       - 'v*'

# jobs:
#   deploy:
#     runs-on: ubuntu-latest

#     steps:
#     - uses: actions/checkout@v3
#     - name: Set up Python
#       uses: actions/setup-python@v4
#       with:
#         python-version: 3.9
#     - name: Install dependencies
#       run: |
#         python -m pip install --upgrade pip
#         pip install -r requirements.txt
#     - name: Build and push Docker image
#       run: |
#         echo ${{ secrets.DOCKERHUB_PASSWORD }} | docker login -u ${{ secrets.DOCKERHUB_USERNAME }} --password-stdin
#         docker build -t grimo .
#         docker tag grimo ${{ secrets.DOCKERHUB_USERNAME }}/grimo:${{ github.ref }}
#         docker push ${{ secrets.DOCKERHUB_USERNAME }}/grimo:${{ github.ref }}
#     - name: Publish to PyPI
#       uses: pypa/gh-action-pypi-publish@master
#       with:
#         user: __token__
#         password: ${{ secrets.PYPI_API_TOKEN }}

# 上記のDockerfile、docker-compose.yml、GitHub Actionsの設定ファイルは、要件定義書の内容に基づいて作成されています。

# Dockerfileでは、Pythonの実行環境を構築し、必要なパッケージをインストールしています。また、アプリケーションのソ