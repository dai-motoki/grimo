import grimo.argparse_multi
import json
import os
import i18n
import requests
from getpass import getpass

from grimo.package import Package, search_packages, get_package, list_installed_packages
from grimo.utils import print_success, print_error, print_warning

# 認証トークンのファイルパス
GRIMO_TOKEN_PATH = ".grimo_token"

# サーバーの URL
# SERVER_URL = "http://43.206.232.28"
# SERVER_URL = "http://localhost:8000"
# SERVER_URL = "https://3bd1f058e743.ngrok.app"
SERVER_URL = "https://grimo-f0b5594b2437.herokuapp.com/"

def login(server_url):
    """Supabase にメールアドレスとパスワードでログインし、認証トークンを保存します。"""
    email = input("メールアドレス: ")
    password = getpass("パスワード: ")

    try:
        response = requests.post(
            f"{server_url}/login", data={"email": email, "password": password}
        )
        response.raise_for_status()  # HTTPエラーチェック

        data = response.json()
        with open(GRIMO_TOKEN_PATH, "w") as f:
            f.write(data["access_token"])
        print_success("ログインに成功しました！")

    except requests.exceptions.HTTPError as err:
        print_error(f"ログインに失敗しました: {err.response.text}")
    except Exception as e:
        print_error(f"ログイン中にエラーが発生しました: {str(e)}")


def signup(server_url):
    """Supabase に新規ユーザーを登録します。"""
    email = input("メールアドレス: ")
    password = getpass("パスワード: ")

    try:
        response = requests.post(
            f"{server_url}/signup", data={"email": email, "password": password}
        )
        response.raise_for_status()  # HTTPエラーチェック

        print_success(response.json()["message"])

    except requests.exceptions.HTTPError as err:
        print_error(f"新規登録に失敗しました: {err.response.text}")
    except Exception as e:
        print_error(f"新規登録中にエラーが発生しました: {str(e)}")


def is_authenticated():
    """ユーザーが認証済みかどうかを確認します。"""
    return os.path.exists(GRIMO_TOKEN_PATH)


def get_auth_token():
    """認証トークンを取得します。"""
    if not is_authenticated():
        print_error("ログインしていません。`grimo login` でログインしてください。")
        return None
    with open(GRIMO_TOKEN_PATH, "r") as f:
        return f.read().strip()

# --- リクエストヘッダーに認証トークンを追加する関数 ---
def make_api_request(method, url, **kwargs):
    """API リクエストを行い、認証トークンをヘッダーに含めます。"""
    token = get_auth_token()
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.request(method, url, headers=headers, **kwargs)

    # ステータスコード200番台以外の場合、例外を発生させる
    response.raise_for_status()

    return response

# 翻訳ファイルをロード
i18n.load_path.append(os.path.join(os.path.dirname(__file__), "i18n"))
i18n.set("locale", "ja")  # Set default locale to Japanese


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

    # --- Main Argument Parser ---
    parser = grimo.argparse_multi.ArgumentParser(
        description=i18n.t("message.cli_description"),
        parents=[parser],
        formatter_class=grimo.argparse_multi.RawDescriptionHelpFormatter,  # ヘルプメッセージのフォーマットを変更
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
        "query", type=str, help=i18n.t("message.query_help")
    )
    search_parser.add_argument(
        "-l", "--language", type=str, help=i18n.t("message.language_help")
    )
    search_parser.add_argument(
        "-c", "--category", type=str, help=i18n.t("message.category_help")
    )
    search_parser.add_argument(
        "-t", "--tags", type=str, nargs="+", help=i18n.t("message.tags_help")
    )

    # --- Install Subcommand ---
    install_parser = subparsers.add_parser(
        "install", help=i18n.t("message.install_help")
    )
    install_parser.add_argument(
        "package", type=str, help=i18n.t("message.package_help")
    )
    install_parser.add_argument(
        "-v", "--version", type=str, help=i18n.t("message.version_help")
    )
    install_parser.add_argument(
        "-f", "--force", action="store_true", help=i18n.t("message.force_help")
    )

    # --- Update Subcommand ---
    update_parser = subparsers.add_parser(
        "update", help=i18n.t("message.update_help")
    )
    update_parser.add_argument(
        "package", type=str, help=i18n.t("message.package_help")
    )

    # --- Uninstall Subcommand ---
    uninstall_parser = subparsers.add_parser(
        "uninstall", help=i18n.t("message.uninstall_help")
    )
    uninstall_parser.add_argument(
        "package", type=str, help=i18n.t("message.package_help")
    )

    # --- Upload Subcommand ---
    upload_parser = subparsers.add_parser(
        "upload", help=i18n.t("message.upload_help")
    )
    upload_parser.add_argument(
        "package_path", type=str, help=i18n.t("message.package_path_help")
    )

    # --- List Subcommand ---
    list_parser = subparsers.add_parser("list", help=i18n.t("message.list_help"))

    # すべてのサブコマンド定義の後に args = parser.parse_args(unknown) を移動
    args = parser.parse_args(unknown)

    # --- コマンド実行前の認証チェック ---
    if args.command != "login" and args.command != "signup" and not is_authenticated():
        print_error("ログインが必要です。`grimo login` でログインしてください。")
        exit(1)

    if hasattr(args, "func"):
        args.func(args)  # サブコマンドに対応する関数を呼び出す
        if (
            args.command == "login" or args.command == "signup"
        ):  # login または signup コマンド実行後なら終了
            exit(0)
    else:
        parser.print_help()

    if args.command == "search":
        if args.query == "all":
            packages = search_packages()
        else:
            packages = search_packages(
                query=args.query,
                language=args.language,
                category=args.category,
                tags=args.tags,
            )
        if packages:
            print_success(i18n.t("message.found_packages", count=len(packages)))
            for package in packages:
                print(f"- {package}")
        else:
            print_warning(i18n.t("message.no_packages_found"))

    elif args.command == "install":
        try:
            if args.version:
                # 特定バージョンが指定されている場合
                package = get_package(args.package, args.version)
            else:
                # バージョン指定がない場合は最新バージョンを取得
                package = get_package(args.package, "latest")
            print_success(
                i18n.t("message.install_success", package=args.package + args.version)
            )
        except Exception as e:
            print_error(i18n.t("message.install_error", error=str(e)))

    elif args.command == "update":  # updateサブコマンドの場合
        try:  # 例外処理のtry節
            latest_package = get_package(
                args.package, "latest"
            )  # - 最新バージョンのパッケージを取得
            installed_package = get_package(
                args.package, latest_package.version
            )  # - インストール済みのパッケージを取得

            if (
                latest_package.version == installed_package.version
            ):  # - 最新バージョンとインストール済みバージョンが同じ場合
                print_warning(
                    i18n.t("message.already_up_to_date", package=args.package)
                )  # -- 既に最新であることを警告メッセージで表示
            else:  # - バージョンが異なる場合
                latest_package.install(
                    force=True
                )  # -- 最新バージョンを強制インストール
                print_success(  # -- 成功メッセージを表示
                    i18n.t(  # --- 多言語対応のメッセージを取得
                        "message.update_success",  # ---- updateの成功メッセージ
                        package=args.package,  # ---- パッケージ名
                        version=latest_package.version,  # ---- 最新バージョン
                    )  #
                )  #
        except Exception as e:  # 例外処理のexcept節
            print_error(
                i18n.t("message.update_error", error=str(e))
            )  # - エラーメッセージを表示
        #
    elif args.command == "uninstall":
        try:
            package_name, package_version = args.package.split("==")
            package = get_package(package_name, package_version)
            package.uninstall()
            print_success(i18n.t("message.uninstall_success", package=package))
        except Exception as e:
            print_error(i18n.t("message.uninstall_error", error=str(e)))
    elif args.command == "list":
        try:
            packages = list_installed_packages()  # インストール済みパッケージをリストする関数を呼び出す
            if packages:
                print_success(i18n.t("message.list_success", count=len(packages)))
                for package in packages:
                    print(f"- {package}")
            else:
                print_warning(i18n.t("message.no_packages_installed"))
        except Exception as e:
            print_error(i18n.t("message.list_error", error=str(e)))

    elif (
        args.command == "upload"
    ):  # uploadサブコマンドの場合
        """
        uploadサブコマンドの処理を行います。
        指定されたパッケージのメタデータを読み込み、パッケージをアップロードします。

        手順:
        1. メタデータファイル(metadata.json)のパスを作成
        2. メタデータファイルを読み込み、JSONとしてパース
        3. メタデータを使ってPackageインスタンスを作成
        4. パッケージをアップロード
        5. 成功メッセージを表示

        Args:
            args.package_path (str): アップロードするパッケージのパス

        Raises:
            Exception: アップロード処理中にエラーが発生した場合
        """
        try:  # 例外処理のtry節
            metadata_path = os.path.join(
                args.package_path, "metadata.json"
            )  # - メタデータファイルのパスを作成
            print(metadata_path)
            with open(
                metadata_path, "r"
            ) as f:  # - メタデータファイルを読み込みモードで開く
                metadata = json.load(f)  # -- メタデータをJSONとして読み込む

            package = Package(
                **metadata
            )  # - メタデータを使ってPackageインスタンスを作成
            # package.upload(metadata_path)
            print(args.package_path)
            package.upload(
                args.package_path
            )  # - パッケージをアップロード
            print_success(
                i18n.t("message.upload_success", package=package)
            )  # - 成功メッセージを表示
        except Exception as e:  # 例外処理のexcept節
            print_error(
                i18n.t("message.upload_error", error=str(e))
            )  # - エラーメッセージを表示
    else:
        parser.print_help()


if __name__ == "__main__":
    main()