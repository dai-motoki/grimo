モジュール概要

| モジュール | 大カテゴリ | 関数 | 使い方 | 効果 |
|---|---|---|---|---|
| **core.py** | パッケージ管理 | `search_packages(keyword, language, category, tag)` | `grimo.search_packages("画像処理", language="python", category="機械学習")` | 指定したキーワード、言語、カテゴリ、タグでパッケージを検索 |
| | | `get_package_details(package_name, version)` | `grimo.get_package_details("opencv-python", version="4.5.5")` | 指定したパッケージ名とバージョン詳細情報を取得 |
| | | `install_package(package_name, version)` | `grimo.install_package("opencv-python", version="4.5.5")` | 指定したパッケージ名とバージョンをインストール |
| | | `update_package(package_name)` | `grimo.update_package("opencv-python")` | 指定したパッケージを最新バージョンにアップデート |
| | | `uninstall_package(package_name)` | `grimo.uninstall_package("opencv-python")` | 指定したパッケージをアンインストール |
| | | `upload_package(package_file, metadata)` | `grimo.upload_package("my_package-1.0.0.tar.gz", metadata)` | 指定したパッケージファイルとメタデータをアップロード |
| **package.py** | パッケージ操作 | `install(force=False)` | `package.install(force=True)` | パッケージをインストール。force=Trueで上書きインストール |
| | | `uninstall()` | `package.uninstall()` | パッケージをアンインストール |
| | | `upload(package_path)` | `package.upload("/path/to/my_package")` | パッケージをアップロード |
| | | `from_metadata(metadata)` | `package = Package.from_metadata(metadata)` | メタデータからPackageオブジェクトを生成 |
| |  | `search_packages(query, language, category, tags)` | `packages = package.search_packages(query="画像処理", language="python")` |  指定した条件でパッケージを検索 |
| | | `get_package(name, version)` | `package = package.get_package("my_package", "1.0.0")` | パッケージ名とバージョンを指定してPackageオブジェクトを取得 |
| **storage.py** | ストレージ操作 | `upload_file(file_path, object_name)` | `storage.upload_file("/path/to/my_file", "my_file")` | ローカルファイルをS3バケットにアップロード |
| | | `download_file(object_name, file_path)` | `storage.download_file("my_file", "/path/to/download")` | S3バケットからローカルにファイルをダウンロード |
| | | `delete_file(object_name)` | `storage.delete_file("my_file")` | S3バケットからファイルを削除 |
| | | `list_files(prefix='')` | `files = storage.list_files(prefix="my_folder/")` | S3バケット内のファイル一覧を取得 |
| | | `get_file_metadata(object_name)` | `metadata = storage.get_file_metadata("my_file")` | S3バケット内のファイルのメタデータを取得 |
| | | `set_file_metadata(object_name, metadata)` | `storage.set_file_metadata("my_file", {"author": "John Doe"})` | S3バケット内のファイルにメタデータを設定 |
| **utils.py** | ユーティリティ | `setup_logger(name, level)` | `logger = utils.setup_logger(__name__, logging.DEBUG)` | ロガーを設定 |
| | | `print_success(message)` | `utils.print_success("処理が完了しました")` | 成功メッセージを緑色で表示 |
| | | `print_error(message)` | `utils.print_error("エラーが発生しました")` | エラーメッセージを赤色で表示 |
| | | `print_warning(message)` | `utils.print_warning("処理に時間がかかっています")` | 警告メッセージを黄色で表示 |
| | | `get_package_dir(package_name)` | `package_dir = utils.get_package_dir("my_package")` | パッケージのディレクトリパスを取得 |
| | | `get_package_file(package_name, filename)` | `file_path = utils.get_package_file("my_package", "requirements.txt")` | パッケージ内のファイルパスを取得 |
| | | `read_file(file_path)` | `content = utils.read_file("my_file.txt")` | ファイルを読み込む |
| | | `write_file(file_path, content)` | `utils.write_file("my_file.txt", "Hello, world!")` | ファイルに書き込む |
| | | `run_command(command)` | `utils.run_command("ls -l")` | コマンドを実行 | 