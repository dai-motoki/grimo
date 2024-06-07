import getpass
import os

from supabase import Client

# Supabase クライアントの初期化
# ... (上記コードと同じ)

def login(supabase: Client) -> None:
    """ユーザーを認証します。"""
    username = input("ユーザー名: ")
    password = getpass.getpass("パスワード: ")

    try:
        # Supabase でユーザーを認証
        response = supabase.auth.sign_in(email=username, password=password)

        # エラー処理
        if response.error:
            print(f"ログインに失敗しました: {response.error}")
            return

        # アクセストークンを環境変数に保存
        os.environ["SUPABASE_ACCESS_TOKEN"] = response.data.access_token
        print("ログインに成功しました。")

    except Exception as e:
        print(f"ログイン中にエラーが発生しました: {e}")

def logout() -> None:
    """ユーザーをログアウトします。"""
    # アクセストークンを環境変数から削除
    if os.environ.get("SUPABASE_ACCESS_TOKEN"):
        del os.environ["SUPABASE_ACCESS_TOKEN"]
        print("ログアウトしました。")
    else:
        print("すでにログアウトしています。")

def get_authenticated_client() -> Client:
    """認証済みの Supabase クライアントを取得します。"""
    access_token = os.environ.get("SUPABASE_ACCESS_TOKEN")
    if access_token:
        return create_client(url, key, access_token=access_token)
    else:
        print("ログインしてください。")
        exit(1)