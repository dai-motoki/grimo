# cli.py

import grimo.argparse_multi
import json
import os
import i18n

from grimo.core import Grimo
from grimo.package import Package, search_packages, get_package, list_installed_packages
from grimo.utils import print_success, print_error, print_warning

# 翻訳ファイルをロード
i18n.load_path.append(os.path.join(os.path.dirname(__file__), 'i18n'))
i18n.set('locale', 'ja')  # Set default locale to English

def main():
    # --- Language Selection ---
    parser = grimo.argparse_multi.ArgumentParser(add_help=False)
    parser.add_argument(
        "-l", "--lang",
        choices=['ja', 'fr', 'de', 'en', 'es', 'it', 'pt', 'ru', 'zh', 'ko', 'ar'],
        default='ja',
        help="日本語: ja\nFrançais: fr\nDeutsch: de\nEnglish: en\nEspañol: es\nItaliano: it\nPortuguês: pt\nРусский: ru\n中文: zh\n한국어: ko\nالعربية: ar\n"

    )
    args, unknown = parser.parse_known_args()
    i18n.set('locale', args.lang)

    # --- Main Argument Parser ---
    parser = grimo.argparse_multi.ArgumentParser(
        description=i18n.t('message.cli_description'),
        parents=[parser],
        formatter_class=grimo.argparse_multi.RawDescriptionHelpFormatter  # ヘルプメッセージのフォーマットを変更
    )
    subparsers = parser.add_subparsers(
        dest="command",
        help=i18n.t('message.subcommand_help')
    )

    # --- Search Subcommand ---
    search_parser = subparsers.add_parser(
        "search",
        help=i18n.t('message.search_help'),
        # description="""\
        #     `grimo search` コマンドは、指定されたクエリに基づいてパッケージを検索するために使用されます。

        #     ### 使用方法

        #     ```sh
        #     grimo search <query> [オプション]
        #     ```

        #     ### 引数

        #     - `<query>`: 検索クエリを指定します。

        #     ### オプション

        #     - `-l`, `--language <言語>`: 言語を指定します。
        #     - `-c`, `--category <カテゴリ>`: カテゴリを指定します。
        #     - `-t`, `--tags <タグ>`: タグを指定します。複数のタグをスペースで区切って指定できます。

        #     ### 例

        #     1. 基本的な検索:
        #         ```sh
        #         grimo search "example query"
        #         ```

        #     2. 言語を指定して検索:
        #         ```sh
        #         grimo search "example query" --language "en"
        #         ```

        #     3. カテゴリを指定して検索:
        #         ```sh
        #         grimo search "example query" --category "utilities"
        #         ```

        #     4. タグを指定して検索:
        #         ```sh
        #         grimo search "example query" --tags "tag1" "tag2"
        #         ```

        #     このコマンドを使用することで、指定された条件に一致するパッケージを簡単に検索することができます。
        #     """
        # help=i18n.t('message.upload_success')
    )
    search_parser.add_argument(
        "query",
        type=str,
        help=i18n.t('message.query_help'),
        # nargs="?"  # ここへ追加
    )
    search_parser.add_argument(
        "-l", "--language", 
        type=str,
        help=i18n.t('message.language_help')
    )
    search_parser.add_argument(
        "-c", "--category",
        type=str,
        help=i18n.t('message.category_help')
    )
    search_parser.add_argument(
        "-t", "--tags",
        type=str,
        nargs="+",
        help=i18n.t('message.tags_help')
    )

    # --- Install Subcommand ---
    install_parser = subparsers.add_parser(
        "install",
        help=i18n.t('message.install_help')
    )
    install_parser.add_argument(
        "package",
        type=str,
        help=i18n.t('message.package_help')
    )
    install_parser.add_argument(
        "-v", "--version",
        type=str,
        help=i18n.t('message.version_help')
    )
    install_parser.add_argument(
        "-f", "--force",
        action="store_true",
        help=i18n.t('message.force_help')
    )

    # --- Update Subcommand ---
    update_parser = subparsers.add_parser(
        "update",
        help=i18n.t('message.update_help')
    )
    update_parser.add_argument(
        "package",
        type=str,
        help=i18n.t('message.package_help')
    )

    # --- Uninstall Subcommand ---
    uninstall_parser = subparsers.add_parser(
        "uninstall",
        help=i18n.t('message.uninstall_help')
    )
    uninstall_parser.add_argument(
        "package",
        type=str,
        help=i18n.t('message.package_help')
    )

    # --- Upload Subcommand ---
    upload_parser = subparsers.add_parser(
        "upload",
        help=i18n.t('message.upload_help')
    )
    upload_parser.add_argument(
        "package_path",
        type=str,
        help=i18n.t('message.package_path_help')
    )

    # --- List Subcommand ---
    list_parser = subparsers.add_parser(
        "list",
        help=i18n.t('message.list_help')
    )

    args = parser.parse_args(unknown)


    args = parser.parse_args(unknown) 

    if args.command == 'search':
        if args.query == "all":
            packages = search_packages()
        else:
            packages = search_packages(
            query=args.query,
            language=args.language,
            category=args.category,
            tags=args.tags
        )
        if packages:
            print_success(i18n.t('message.found_packages', count=len(packages)))
            for package in packages:
                print(f"- {package}")
        else:
            print_warning(i18n.t('message.no_packages_found'))

    elif args.command == 'install':
        try:
            if args.version:
                # package = get_package(args.package, args.version)
                get_package(args.package, args.version)
            else:
                print("デバッグ: 最新バージョンを取得")
                # package = get_package(args.package, "latest")
                get_package(args.package, "latest")
            # package.install(args.force)
            print_success(i18n.t('message.install_success',
                                 package=args.package+args.version))
            # print_success(i18n.t('message.install_success'))
        except Exception as e:
            print_error(i18n.t('message.install_error', error=str(e)))

    elif args.command == "update":                                                                                # updateサブコマンドの場合
        try:                                                                                                      # 例外処理のtry節
            latest_package = get_package(args.package, "latest")                                                  # - 最新バージョンのパッケージを取得
            installed_package = get_package(args.package, latest_package.version)                                 # - インストール済みのパッケージを取得
                                                                                                                  #
            if latest_package.version == installed_package.version:                                               # - 最新バージョンとインストール済みバージョンが同じ場合
                print_warning(i18n.t("message.already_up_to_date", package=args.package))                         # -- 既に最新であることを警告メッセージで表示
            else:                                                                                                 # - バージョンが異なる場合
                latest_package.install(force=True)                                                                # -- 最新バージョンを強制インストール
                print_success(                                                                                    # -- 成功メッセージを表示
                    i18n.t(                                                                                       # --- 多言語対応のメッセージを取得
                        "message.update_success",                                                                 # ---- updateの成功メッセージ
                        package=args.package,                                                                     # ---- パッケージ名
                        version=latest_package.version,                                                           # ---- 最新バージョン
                    )                                                                                             #
                )                                                                                                 #
        except Exception as e:                                                                                    # 例外処理のexcept節
            print_error(i18n.t("message.update_error", error=str(e)))                                             # - エラーメッセージを表示
                                                                                                                  #
    elif args.command == 'uninstall':
        try:
            package_name, package_version = args.package.split("==")
            package = get_package(package_name, package_version)
            package.uninstall()
            print_success(i18n.t('message.uninstall_success', package=package))
        except Exception as e:
            print_error(i18n.t('message.uninstall_error', error=str(e)))
    elif args.command == 'list':
        try:
            packages = list_installed_packages()  # インストール済みパッケージをリストする関数を呼び出す
            if packages:
                print_success(i18n.t('message.list_success', count=len(packages)))
                for package in packages:
                    print(f"- {package}")
            else:
                print_warning(i18n.t('message.no_packages_installed'))
        except Exception as e:
            print_error(i18n.t('message.list_error', error=str(e)))

    elif args.command == "upload":                                                                                # uploadサブコマンドの場合
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
        try:                                                                                                      # 例外処理のtry節
            metadata_path = os.path.join(args.package_path, "metadata.json")                                      # - メタデータファイルのパスを作成
            with open(metadata_path, "r") as f:                                                                   # - メタデータファイルを読み込みモードで開く
                metadata = json.load(f)                                                                           # -- メタデータをJSONとして読み込む
                                                                                                                  #
            package = Package(**metadata)                                                                         # - メタデータを使ってPackageインスタンスを作成
            package.upload(args.package_path)                                                                     # - パッケージをアップロード
            print_success(i18n.t("message.upload_success", package=package))                                      # - 成功メッセージを表示
        except Exception as e:                                                                                    # 例外処理のexcept節
            print_error(i18n.t("message.upload_error", error=str(e)))                                             # - エラーメッセージを表示
    else:
        parser.print_help()

if __name__ == "__main__":
    main()