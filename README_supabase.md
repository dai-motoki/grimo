了解しました！Grimo CLI で Supabase のメール認証を使ってログインできるように、手順を整理して説明します。今回は、シンプルにするためにメール認証に焦点を当て、Google 認証や AWS Secrets Manager の部分は省略します。

**1. Supabase プロジェクトの設定**

1. **プロジェクト作成:** Supabase ダッシュボードで新規プロジェクトを作成します（既に作成済みの場合はこの手順は不要です）。
2. **API キーの確認:** プロジェクト設定 > API タブから、以下のキーをメモしておきます。
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
3. **メール認証の有効化:**
   - Supabase ダッシュボード > Authentication > Providers > Email を選択します。
   - "Enable Email Confirmations?" を **無効** にします。
     - 開発中は、確認メールの処理をスキップするためです。
     - 本番環境では、セキュリティのため有効にすることをお勧めします。
   - 必要であれば、"Welcome Email" や "Password Recovery" の設定も行います。

**2. FastAPI サーバーの実装**

1. **プロジェクトディレクトリ作成 & 仮想環境設定:** (既に実施済みならスキップ)
   ```bash
   mkdir grimo-server
   cd grimo-server
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **必要なパッケージのインストール:**
   ```bash
   pip install fastapi uvicorn python-multipart python-dotenv requests python-jose[cryptography]
   ```
3. **`server.py` の作成:**
   ```python
   import os
   from fastapi import FastAPI, Depends, HTTPException, Request
   from fastapi.security import OAuth2PasswordBearer
   from starlette.status import HTTP_401_UNAUTHORIZED
   from fastapi.responses import JSONResponse
   from dotenv import load_dotenv
   from supabase import create_client, Client

   load_dotenv()

   app = FastAPI()

   # Supabase クライアントの初期化
   supabase_url = os.environ.get("SUPABASE_URL")
   supabase_anon_key = os.environ.get("SUPABASE_ANON_KEY")
   supabase: Client = create_client(supabase_url, supabase_anon_key)

   # OAuth2 スキーマ (ダミー)
   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

   # 認証デコレータ
   async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
       try:
           user = await supabase.auth.get_user(token)
           if not user:
               raise HTTPException(
                   status_code=HTTP_401_UNAUTHORIZED,
                   detail="Invalid authentication credentials",
                   headers={"WWW-Authenticate": "Bearer"},
               )
           return user.user
       except Exception as e:
           raise HTTPException(
               status_code=HTTP_401_UNAUTHORIZED,
               detail=f"Authentication failed: {str(e)}",
               headers={"WWW-Authenticate": "Bearer"},
           )

   @app.post("/install")
   async def install(request: Request, package_name: str, current_user=Depends(get_current_user)):
       return JSONResponse({'message': f'Package {package_name} installed for user {current_user.id}'})

   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```
4. **`.env` ファイルの作成:**
   ```
   SUPABASE_URL=<Supabase プロジェクトの URL>
   SUPABASE_ANON_KEY=<Supabase プロジェクトのアノニマスパブリックキー>
   ```


**3. Grimo CLI の実装**

1. **プロジェクトディレクトリ作成 & 仮想環境設定:** (既に実施済みならスキップ)
   ```bash
   mkdir grimo-cli
   cd grimo-cli
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **必要なパッケージのインストール:**
   ```bash
   pip install requests
   ```
3. **`grimo.py` の作成:**
   ```python
   import os
   import argparse
   import requests
   from getpass import getpass
   from supabase import create_client, Client

   # Supabase クライアントの初期化
   supabase_url = os.environ.get("SUPABASE_URL")
   supabase_anon_key = os.environ.get("SUPABASE_ANON_KEY")
   supabase: Client = create_client(supabase_url, supabase_anon_key)

   def login(args):
       """Supabase にメールアドレスとパスワードでログインし、認証トークンを保存します。"""
       email = input("メールアドレス: ")
       password = getpass("パスワード: ")

       try:
           response = supabase.auth.sign_in(email=email, password=password)
           if response.error:
               print(f"ログインに失敗しました: {response.error}")
           else:
               with open('.grimo_token', 'w') as f:
                   f.write(response.data.access_token)
               print("ログインに成功しました！")
       except Exception as e:
           print(f"ログイン中にエラーが発生しました: {e}")

   def install(args):
       if not os.path.exists('.grimo_token'):
           print("You need to login first using 'grimo login'")
           return

       with open('.grimo_token', 'r') as f:
           token = f.read().strip()

       headers = {
           'Authorization': f'Bearer {token}'
       }
       response = requests.post(
           'http://localhost:8000/install',  # FastAPI の URL (後で ngrok の URL に変更)
           headers=headers,
           json={'package_name': args.package_name}
       )
       if response.status_code == 200:
           print(response.json().get('message'))
       else:
           print(f"An error occurred: {response.text}")

   # ... (他のコマンドの定義)

   def main():
       parser = argparse.ArgumentParser(description='Grimo CLI', prog='grimo')
       subparsers = parser.add_subparsers(dest='command', help='Sub-commands')

       # login コマンド
       login_parser = subparsers.add_parser('login', help='Login to Grimo')
       login_parser.set_defaults(func=login)

       # install コマンド
       install_parser = subparsers.add_parser('install', help='Install a package')
       install_parser.add_argument('package_name', help='Name of the package to install')
       install_parser.set_defaults(func=install)

       # ... (他のコマンドの登録)

       args = parser.parse_args()

       if args.command:
           args.func(args)
       else:
           parser.print_help()

   if __name__ == '__main__':
       main()
   ```

4. **`grimo.py` に実行権限を付与:**

   ```bash
   chmod +x grimo.py
   ```

**4. ngrok の起動と CLI ツールの動作確認**

1. **FastAPI サーバーを起動:**
   ```bash
   cd <server.pyのあるディレクトリ>
   uvicorn server:app --reload
   ```
2. **ngrok で FastAPI サーバーを公開:**
   ```bash
   ngrok http 8000
   ```

3. **`grimo.py` の修正:**
   - ngrok によって発行された URL (例: `https://xxxxxxxx.ngrok.io`) をコピーし、`grimo.py` の `install` 関数内のリクエスト送信先 URL を書き換えます。

     ```python
     response = requests.post(
         'https://xxxxxxxx.ngrok.io/install',  # ngrok の URL に変更
         # ...
     )
     ```

4. **CLI ツールの実行:**

   ```bash
   ./grimo.py login
   # ユーザー登録済みのメールアドレスとパスワードを入力
   ./grimo.py install <package_name> 
   ```

これで、Supabase のメール認証を使って Grimo CLI にログインし、`install` コマンドを実行できるようになりました。 必要に応じて、他のコマンドも実装し、CLI ツールを拡張していきましょう。