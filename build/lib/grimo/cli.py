import toml
import shutil 
import tempfile
import grimo.argparse_multi
import json
import os
import i18n
import requests
import asyncio  # 追加: asyncio モジュールのインポート
import aiohttp  # aiohttp をインポート
import aiofiles  # aiofiles をインポート
from getpass import getpass
from typing import List, Dict  # 追加: 型ヒント
import inspect
import logging
import re  # 追加: re モジュールのインポート
import subprocess  # 追加: subprocess モジュールのインポート
import shlex  # 追加: shlex モジュールのインポート

# サーバーの URL
SERVER_URL = "https://grimo-f0b5594b2437.herokuapp.com"  # 適宜変更
# SERVER_URL = "http://127.0.0.1:8000"  # 適宜変更

# ロギングの設定
# logging.basicConfig(level=logging.INFO,
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
def my_logger(*args, level='DEBUG'):
    """呼び出し元のファイル名、行番号、任意の引数を指定されたログレベルで出力する関数

    Args:
        *args: ログ出力する任意の引数
        level: ログレベル (DEBUG, INFO, WARNING, ERROR, CRITICAL). デフォルトは 'DEBUG'.
    """
    caller_frame = inspect.currentframe().f_back
    filename = caller_frame.f_code.co_filename
    lineno = caller_frame.f_lineno
    message = f"File \"{filename}\", line {lineno}: {' '.join(map(str, args))}"

    logger = logging.getLogger(__name__)
    color_map = {
        'DEBUG': '\033[94m',    # 青
        'INFO': '\033[38;2;51;204;153m',  # 明るい青みがかった緑色 (#33CC99)
        'WARNING': '\033[93m',  # 黄
        'ERROR': '\033[91m',    # 赤
        'CRITICAL': '\033[95m'  # 紫
    }
    reset_color = '\033[0m'
    colored_message = f"{color_map.get(level, '')}{message}{reset_color}"

    if level == 'DEBUG':
        logger.debug(colored_message)
    elif level == 'INFO':
        logger.info(colored_message)
    elif level == 'WARNING':
        logger.warning(colored_message)
    elif level == 'ERROR':
        logger.error(colored_message)
    elif level == 'CRITICAL':
        logger.critical(colored_message)
    else:
        raise ValueError(f"Invalid log level: {level}")


from grimo.utils import print_success, print_error, print_warning
# 認証トークンのファイルパス
GRIMO_TOKEN_PATH = ".grimo_token"


async def login(server_url):
    """Supabase にメールアドレスとパスワードでログインし、認証トークンを保存します。"""
    email = input("メールアドレス: ")
    password = getpass("パスワード: ")

    async with aiohttp.ClientSession() as session:  # aiohttp セッションを開始
        try:
            my_logger(f"ログインリクエストを送信中 - URL: {server_url}/login, Email: {email}", level='INFO')
            async with session.post(f"{server_url}/login", data={"email": email, "password": password}) as response:
                response.raise_for_status()
                data = await response.json()  # await を追加
                my_logger(f"レスポンスデータ - {data}", level='DEBUG')
                with open(GRIMO_TOKEN_PATH, "w") as f:
                    f.write(data["access_token"])
                print_success("ログインに成功しました！")
                my_logger("ログインに成功しました！", level='INFO')

        except aiohttp.ClientError as err:  # aiohttp の例外処理
            print_error(f"ログインに失敗しました: {err}")
            my_logger(f"HTTPエラー - {err}", level='ERROR')
        except Exception as e:
            print_error(f"ログイン中にエラーが発生しました: {str(e)}")
            my_logger(f"例外エラー - {str(e)}", level='ERROR')

async def signup(server_url):
    """Supabase に新規ユーザーを登録します。"""
    email = input("メールアドレス: ")
    password = getpass("パスワード: ")

    async with aiohttp.ClientSession() as session:  # aiohttp セッションを開始
        try:
            my_logger(f"新規登録リクエストを送信中 - URL: {server_url}/signup, Email: {email}", level='INFO')
            async with session.post(f"{server_url}/signup", data={"email": email, "password": password}) as response:
                response.raise_for_status()
                message = await response.json()["message"]  # await を追加
                my_logger(f"レスポンスメッセージ - {message}", level='DEBUG')
                print_success(message)
                my_logger("新規登録に成功しました！", level='INFO')

        except aiohttp.ClientError as err:  # aiohttp の例外処理
            print_error(f"新規登録に失敗しました: {err}")
            my_logger(f"HTTPエラー - {err}", level='ERROR')
        except Exception as e:
            print_error(f"新規登録中にエラーが発生しました: {str(e)}")
            my_logger(f"例外エラー - {str(e)}", level='ERROR')

def is_authenticated():
    """ユーザーが認証済みかどうかを確認します。"""
    authenticated = os.path.exists(GRIMO_TOKEN_PATH)
    my_logger(f"認証済みチェック - {authenticated}", level='DEBUG')
    return authenticated

def get_auth_token():
    """認証トークンを取得します。"""
    if not is_authenticated():
        print_error("ログインしていません。`grimo login` でログインしてください。")
        my_logger("認証トークンが存在しません。ログインしてください。", level='ERROR')
        return None
    with open(GRIMO_TOKEN_PATH, "r") as f:
        token = f.read().strip()
        my_logger(f"認証トークン取得 - {token}", level='DEBUG')
        return token

# --- リクエストヘッダーに認証トークンを追加する関数 ---
def make_api_request(method, url, **kwargs):
    """API リクエストを行い、認証トークンをヘッダーに含めます。"""
    my_logger(f"メソッド - {method}, URL - {url}", level='DEBUG')
    token = get_auth_token()
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    my_logger(f"ヘッダー - {headers}", level='DEBUG')

    # methodが"post"の時の処理
    if method.lower() == "post":
        try:
            my_logger(f"POSTリクエストを送信します - URL: {url}, ヘッダー: {headers}, その他の引数: {kwargs}", level='INFO')
            response = requests.post(url, headers=headers, **kwargs)
            response.raise_for_status()
            my_logger(f"レスポンス - {response.text}", level='DEBUG')
            return response
        except requests.exceptions.HTTPError as err:
            my_logger(f"HTTPエラーが発生しました - {err}", level='ERROR')
            if response.status_code == 422:
                from pydantic import BaseModel, ValidationError

                class Model(BaseModel):
                    x: str

                try:
                    my_logger(f"Pydanticモデルの検証を開始します", level='DEBUG')
                    Model()
                except ValidationError as exc:
                    my_logger(f"Pydanticモデルの検証エラー - {repr(exc.errors()[0]['type'])}", level='ERROR')
                    #> 'missing'
            else:
                my_logger(f"HTTPエラー - {err}", level='ERROR')
                raise
    else:
        response = requests.request(method, url, headers=headers, **kwargs)
        my_logger(f"レスポンスステータス - {response.status_code}", level='DEBUG')

        # ステータスコード200番台以外の場合、例外を発生させる
        response.raise_for_status()

        # my_logger(f"レスポンス - {response.text}", level='DEBUG')
        return response

# 翻訳ファイルをロード
i18n.load_path.append(os.path.join(os.path.dirname(__file__), "i18n"))
i18n.set("locale", "ja")  # Set default locale to Japanese

def parse_version_spec(version_spec: str) -> Dict:
    """バージョン指定文字列を解析し、辞書形式で返します。
    
    Args:
        version_spec: バージョン指定文字列 (例: "3.3.2", "[3.3.2, 3.6.3]", "@M3.3.2")
    
    Returns:
        バージョン指定を表現する辞書。
        例:
            {"type": "exact", "version": "3.3.2"}
            {"type": "range", "start": "3.3.2", "end": "3.6.3", "inclusive": True}
            {"type": "major", "version": "3.3.2"}
    """
    if version_spec is None:
        return {"type": "latest", "version": None}
    elif re.match(r'^[\d\.]+$', version_spec):  # "3.3.2" のような形式
        return {"type": "exact", "version": version_spec}
    elif re.match(r'^\[([\d\.]+), *([\d\.]+)\]$', version_spec):  # "[3.3.2, 3.6.3]" のような形式
        start, end = re.match(r'^\[([\d\.]+), *([\d\.]+)\]$', version_spec).groups()
        return {"type": "range", "start": start, "end": end, "inclusive": True}
    elif re.match(r'^\((([\d\.]+), *([\d\.]+)\))$', version_spec):  # "(3.3.2, 3.6.3)" のような形式
        start, end = re.match(r'^\((([\d\.]+), *([\d\.]+)\))$', version_spec).groups()
        return {"type": "range", "start": start, "end": end, "inclusive": False}
    elif re.match(r'^@M([\d\.]+)$', version_spec):  # "@M3.3.2" のような形式
        version = re.match(r'^@M([\d\.]+)$', version_spec).group(1)
        return {"type": "major", "version": version}
    elif re.match(r'^@m([\d\.]+)$', version_spec):  # "@m3.3.2" のような形式
        version = re.match(r'^@m([\d\.]+)$', version_spec).group(1)
        return {"type": "minor", "version": version}
    else:
        raise ValueError(f"Invalid version spec: {version_spec}")

def run_grimo_command(command: str):
    """grimo コマンドを実行します。

    Args:
        command (str): 実行する grimo コマンド (例: "grimo install banner@[1.0.34,1.0.40]")
    """
    escaped_command = shlex.quote(command)  # コマンド全体をエスケープ
    zsh_command = ["zsh", "-c", escaped_command]
    process = subprocess.Popen(zsh_command, stderr=subprocess.PIPE, text=True)
    _, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error executing command: {command}\n{stderr}") 

def main():
    # --- Language Selection ---
    parser = grimo.argparse_multi.ArgumentParser(add_help=False)
    parser.add_argument(
        "-l",
        "--lang",
        choices=["ja", "fr", "de", "en", "es", "it", "pt", "ru", "zh", "ko", "ar"],
        default="ja",
        help="日本語: ja\nFrançais: fr\nDeutsch: de\nEnglish: en\nEspañol: es\nItaliano: it\nPortuguês: pt\nРусский: ru\n中文: zh\n한국어: ko\nالعربية: ar\n",
    )
    args, unknown = parser.parse_known_args()
    i18n.set("locale", args.lang)
    my_logger(f"言語設定 - {args.lang}", level='DEBUG')

    # --- Main Argument Parser ---
    parser = grimo.argparse_multi.ArgumentParser(
        description=i18n.t("message.cli_description"),
        parents=[parser],
        formatter_class=grimo.argparse_multi.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="command", help=i18n.t("message.subcommand_help")
    )

    # --- Login Subcommand ---
    login_parser = subparsers.add_parser("login", help="Grimo にログインします")
    login_parser.set_defaults(func=lambda args: login(SERVER_URL))

    # --- Signup Subcommand ---
    signup_parser = subparsers.add_parser("signup", help="Grimo に新規登録します")
    signup_parser.set_defaults(func=lambda args: signup(SERVER_URL))

    # --- Search Subcommand ---
    search_parser = subparsers.add_parser(
        "search", help=i18n.t("message.search_help")
    )
    search_parser.add_argument(
        "package_name", type=str, help=i18n.t("message.query_help")
    )
    search_parser.set_defaults(func=lambda args: search(args.package_name))

    # --- Install Subcommand ---
    install_parser = subparsers.add_parser(
        "install", help=i18n.t("message.install_help")
    )
    install_parser.add_argument(
        "package_spec", type=str, help=i18n.t("message.package_help")
    )
    install_parser.set_defaults(func=handle_install)  # コマンドハンドラを変更

    # --- Update Subcommand ---
    update_parser = subparsers.add_parser(
        "update", help=i18n.t("message.update_help")
    )
    update_parser.add_argument(
        "package_name", type=str, help=i18n.t("message.package_help")
    )
    update_parser.set_defaults(func=lambda args: update(args.package_name))

    # --- Uninstall Subcommand ---
    uninstall_parser = subparsers.add_parser(
        "uninstall", help=i18n.t("message.uninstall_help")
    )
    uninstall_parser.add_argument(
        "package_name", type=str, help=i18n.t("message.package_help")
    )
    uninstall_parser.set_defaults(func=lambda args: uninstall(args.package_name))

    # --- Upload Subcommand ---
    upload_parser = subparsers.add_parser(
        "upload", help=i18n.t("message.upload_help")
    )
    upload_parser.add_argument(
        "package_path", type=str, help=i18n.t("message.package_path_help")
    )
    upload_parser.set_defaults(func=lambda args: upload(args.package_path))

    # --- List Subcommand ---
    list_parser = subparsers.add_parser("list", help=i18n.t("message.list_help"))
    list_parser.set_defaults(func=lambda args: list_packages())

    args = parser.parse_args(unknown)
    my_logger(f"コマンドライン引数 - {args}", level='DEBUG')

    # --- コマンド実行前の認証チェック ---
    if args.command not in ["login", "signup", "install", None] and not is_authenticated():
        print_error("ログインが必要です。`grimo login` でログインしてください。")
        my_logger("認証が必要です。ログインしてください。", level='ERROR')
        exit(1)

    if hasattr(args, "func"):
        import asyncio  # asyncio をインポート
        my_logger(f"コマンド実行 - {args.command}", level='DEBUG')
        asyncio.run(args.func(args))  # await を追加して asyncio.run で実行
        if args.command in ["login", "signup"]:
            exit(0)
    else:
        parser.print_help()

async def handle_install(args):
    """install コマンドを処理する関数。
    パッケージ名とバージョン指定を分離します。
    """
    package_parts = args.package_spec.split('@')
    package_name = package_parts[0]
    version_spec = package_parts[1] if len(package_parts) > 1 else None

    # install 関数を直接呼び出す
    await install(package_name, version_spec)  # run_grimo_command を削除


async def search(package_name: str):
    """
    指定されたパッケージを検索します。

    Args:
        package_name (str): 検索するパッケージ名
    """
    try:
        my_logger(f"search package: {package_name} - APIリクエストを送信中", level='DEBUG')
        response = make_api_request("GET", f"{SERVER_URL}/packages/search/{package_name}")
        versions = response.json()
        my_logger(f"search package: {package_name} - レスポンス受信: {versions}", level='DEBUG')

        if versions and 'metadata' in versions:
            print_success(
                i18n.t("message.found_packages", count=len(versions['metadata']))
            )
            # バージョンを昇順にソート
            sorted_versions = sorted(versions['metadata'], key=lambda v: list(map(int, v.split('.'))))
            print(f"{package_name} -v {sorted_versions}")
        else:
            print_warning(i18n.t("message.no_packages_found"))
            my_logger("パッケージが見つかりませんでした", level='WARNING')
    except requests.exceptions.HTTPError as err:
        print_error(f"パッケージの検索に失敗しました: {err.response.text}")
        my_logger(f"search package: {package_name} - HTTPエラー: {err.response.text}", level='ERROR')
    except Exception as e:
        print_error(f"パッケージの検索中にエラーが発生しました: {str(e)}")
        my_logger(f"search package: {package_name} - 例外エラー: {str(e)}", level='ERROR')

async def install(package_name: str, version_spec: str = None):
    """
    指定されたパッケージをインストールします。

    Args:
        package_name (str): インストールするパッケージ名
        version_spec (str, optional): インストールするバージョン. 
                                       指定しない場合は最新バージョンがインストールされます。
    """
    try:
        my_logger(f"install: パッケージ名 - {package_name}, バージョン指定 - {version_spec}", level='INFO')
        version_data = parse_version_spec(version_spec)
        my_logger(f"install: 解析済みバージョンデータ - {version_data}", level='DEBUG')

        data = {"package_name": package_name, "version": version_data["version"]}
        my_logger(f"install: data 構築完了 - {data}", level='DEBUG')

        my_logger("install: APIリクエスト送信開始", level='INFO')
        async with aiohttp.ClientSession() as session:
            my_logger("install: aiohttp.ClientSession 開始", level='DEBUG')
            async with session.post(f"{SERVER_URL}/packages/install", json=data) as response:
                my_logger("install: POSTリクエスト送信", level='DEBUG')
                response.raise_for_status()
                import base64
                my_logger(f"デバッグ: {__file__}: install: APIリクエスト送信完了 - レスポンス: {response}", level='DEBUG')
                json_response = await response.json()
                encoded_response = json_response.get("file_content")
                decoded_response = base64.b64decode(encoded_response)
                my_logger(f"デバッグ: {__file__}: install: APIリクエスト送信完了 - レスポンス内容: {decoded_response}", level='DEBUG')

                # --- 変更箇所ここから ---
                # レスポンスヘッダーから実際のバージョンを取得
                actual_version = response.headers.get("Grimo-Package-Version") 
                if not actual_version:
                    # レスポンスヘッダーにバージョンがない場合は、エラーとする
                    raise ValueError("Could not get the package version from the response.")

                package_dir = os.path.dirname(os.path.abspath(__file__)) + "/grimoires/" + package_name + "/" + actual_version
                # --- 変更箇所ここまで ---

                os.makedirs(package_dir, exist_ok=True)  # ディレクトリがない場合は作成
                filename = f"{package_dir}/{package_name}-{actual_version}.zip"

                with open(filename, "wb") as file:
                    file.write(decoded_response)
                    my_logger(f"ファイルが保存されました: {filename}", level='INFO')
                

                # zipファイルを展開する
                my_logger(f"install: zipファイルを展開開始 - {filename}", level='INFO')
                import zipfile
                # zipファイルを展開
                if filename.endswith(".zip"):
                    my_logger("zipファイルです", level='DEBUG')
                    with zipfile.ZipFile(filename, 'r') as zip_ref:
                        zip_ref.extractall(package_dir)
                    my_logger(f"install: zipファイルを展開完了 - {package_dir}", level='INFO')
                else:
                    my_logger("zipファイルではありません", level='WARNING')

                print_success(f"パッケージ {package_name} {actual_version} を正常にインストールしました")
                my_logger(f"install: インストール完了 - パッケージ: {package_name}, バージョン: {actual_version}, インストール先: {package_dir}", level='INFO')
    except aiohttp.ClientError as err:
        print_error(f"パッケージのインストールに失敗しました: {err}")
        my_logger(f"install: HTTPエラー - {err}", level='ERROR')
    except Exception as e:
        print_error(f"パッケージのインストール中にエラーが発生しました: {str(e)}")
        my_logger(f"install: 例外エラー - {str(e)}", level='ERROR')
async def update(package_name: str):
    """
    指定されたパッケージを更新します。

    Args:
        package_name (str): 更新するパッケージ名
    """
    try:
        my_logger(f"update package: {package_name} - APIリクエストを送信中", level='INFO')
        response = make_api_request("POST", f"{SERVER_URL}/packages/update/{package_name}")
        my_logger(f"update package: {package_name} - レスポンス受信: {response.json()}")
        print_success(response.json()["message"])
    except requests.exceptions.HTTPError as err:
        print_error(f"パッケージの更新に失敗しました: {err.response.text}")
        my_logger(f"update package: {package_name} - HTTPエラー: {err.response.text}", level='ERROR')
    except Exception as e:
        print_error(f"パッケージの更新中にエラーが発生しました: {str(e)}")
        my_logger(f"update package: {package_name} - 例外エラー: {str(e)}", level='ERROR')

async def uninstall(package_name: str):
    """
    指定されたパッケージをアンインストールします。

    Args:
        package_name (str): アンインストールするパッケージ名
    """
    try:
        my_logger(f"uninstall package: {package_name} - APIリクエストを送信中")
        response = make_api_request("DELETE", f"{SERVER_URL}/packages/uninstall/{package_name}")
        print_success(response.json()["message"])
    except requests.exceptions.HTTPError as err:
        print_error(f"パッケージのアンインストールに失敗しました: {err.response.text}")
        my_logger(f"uninstall package: {package_name} - HTTPエラー: {err.response.text}", level='ERROR')
    except Exception as e:
        print_error(f"パッケージのアンインストール中にエラーが発生しました: {str(e)}")
        my_logger(f"uninstall package: {package_name} - 例外エラー: {str(e)}", level='ERROR')


async def upload(package_path: str):
    """
    指定されたパッケージをアップロードします。
    Args:
        package_path (str): アップロードするパッケージのディレクトリパス
    """
    try:
        my_logger(f"パッケージパス = {package_path}")

        # パッケージディレクトリを zip 圧縮
        with tempfile.TemporaryDirectory() as temp_dir:  # 一時ディレクトリを作成
            my_logger(f"一時ディレクトリ作成: {temp_dir}", level='DEBUG')
            zip_file_path = os.path.join(temp_dir, 'package.zip')
            my_logger(f"zipファイルパス: {zip_file_path}", level='INFO')
            shutil.make_archive(zip_file_path[:-4], 'zip', package_path)  # zip ファイルを作成
            my_logger(f"zipファイル作成完了: {zip_file_path}", level='DEBUG')

            # grimo.toml からメタデータを読み込み
            with open(os.path.join(package_path, "grimo.toml"), "r") as f:
                metadata = toml.load(f)
            my_logger(f"メタデータ読み込み完了: {metadata}", level='INFO')

            # FastAPI の /upload エンドポイントにリクエストを送信
            with open(zip_file_path, "rb") as package_file:  # zip ファイルを開く
                my_logger(f"zipファイルオープン: {zip_file_path}", level='DEBUG')
                response = make_api_request(
                    "POST",
                    f"{SERVER_URL}/upload",
                    files={"package": (metadata["name"] + "-" + metadata["version"] + ".zip", package_file)},  # ファイル名を設定
                    data=metadata,
                )
            my_logger(f"APIリクエスト送信完了 - ステータスコード: {response.status_code}", level='DEBUG')
            my_logger(f"APIリクエスト送信完了 - レスポンスヘッダー: {response.headers}", level='DEBUG')
            my_logger(f"APIリクエスト送信完了 - レスポンス内容: {response.text}", level='DEBUG')
            my_logger(f"レスポンス = {response}", level='DEBUG')

        print_success(response.json()["message"])  # 成功メッセージを表示
        my_logger(f"アップロード成功 - メッセージ: {response.json()['message']}", level='INFO')
    except Exception as e:
        print_error(i18n.t("message.upload_error", error=str(e)))
        my_logger(f"アップロード中にエラーが発生しました: {str(e)}", level='ERROR')
        my_logger(f"エラー = {str(e)}", level='DEBUG')

async def list_packages():
    """
    インストール済みのパッケージを一覧表示します。
    """
    try:
        response = make_api_request("GET", f"{SERVER_URL}/packages")
        my_logger(f"APIリクエスト送信完了 - ステータスコード: {response.status_code}", level='DEBUG')
        packages = response.json()
        my_logger(f"レスポンス内容: {packages}", level='DEBUG')
        if packages:
            print_success(i18n.t("message.list_success", count=len(packages)))
            for package in packages:
                print(f"- {package['package_name']} {package['version']} ({package['description']})")
        else:
            print_warning(i18n.t("message.no_packages_installed"))
    except requests.exceptions.HTTPError as err:
        print_error(f"パッケージの一覧取得に失敗しました: {err.response.text}")
        my_logger(f"パッケージの一覧取得に失敗しました: {err.response.text}", level='ERROR')
    except Exception as e:
        print_error(f"パッケージの一覧取得中にエラーが発生しました: {str(e)}")
        my_logger(f"パッケージの一覧取得中にエラーが発生しました: {str(e)}", level='ERROR')

if __name__ == "__main__":
    main()

