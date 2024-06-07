import os
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi.responses import JSONResponse, PlainTextResponse
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # .env ファイルから環境変数をロード

# 環境変数から設定を読み込み
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")

# Supabase クライアントの初期化
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# OAuth2 スキーマ (ダミー)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI アプリケーションの設定
app = FastAPI()

@app.get("/supabase_anon_key")
async def get_supabase_anon_key():
    return PlainTextResponse(os.environ.get("SUPABASE_ANON_KEY"))

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

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    print(f"email: {email}")
    print(f"password: {password}")
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        # 認証失敗時は response が None になる
        if response is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # デバッグ用のprint文
        print(f"Login successful for email: {email}")

        return JSONResponse({
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        })
    except Exception as e:
        # デバッグ用のprint文
        print(f"Login failed for email: {email}, error: {str(e)}")

        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.post("/signup")
async def signup(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password
            }
        )
        if response is None:
            raise HTTPException(status_code=400, detail=response.error.message)

        return JSONResponse({"message": "User created successfully. Please check your email for confirmation."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)