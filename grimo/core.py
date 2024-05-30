# core.py

import os
import requests
from .utils import print_success, print_error, print_warning, setup_logger
from .package import Package, search_packages, get_package
from .storage import StorageManager

# ロガーを設定
logger = setup_logger(__name__)

class Grimo:
    def __init__(self, storage_provider='s3', bucket_name='grimo', region_name='ap-northeast-1'):
        self.storage = StorageManager(bucket_name, region_name)
        self.package_cache = {}

    def search_packages(self, keyword, language=None, category=None, tag=None):
        """パッケージを検索する"""
        logger.info(f"Searching packages for keyword: {keyword}")
        packages = search_packages(query=keyword, language=language, category=category, tags=[tag] if tag else [])
        return packages

    def get_package_details(self, package_name, version=None):
        """パッケージの詳細情報を取得する"""
        logger.info(f"Getting details for package: {package_name}")
        package = get_package(package_name, version)
        return package

    def install_package(self, package_name, version=None, force=False):
        """パッケージをインストールする"""
        logger.info(f"Installing package: {package_name}")
        package = get_package(package_name, version)
        package.install(force=force)
        print_success(f"Successfully installed {package}")

    def update_package(self, package_name):
        """パッケージをアップデートする"""
        logger.info(f"Updating package: {package_name}")
        latest_package = get_package(package_name, "latest")
        latest_package.install(force=True)
        print_success(f"Successfully updated {package_name} to version {latest_package.version}")

    def uninstall_package(self, package_name, version):
        """パッケージをアンインストールする"""
        logger.info(f"Uninstalling package: {package_name}")
        package = get_package(package_name, version)
        package.uninstall()
        print_success(f"Successfully uninstalled {package}")

    def upload_package(self, package_path, metadata):
        """パッケージをアップロードする"""
        logger.info(f"Uploading package: {metadata['name']}")
        package = Package.from_metadata(metadata)
        package.upload(package_path)
        print_success(f"Successfully uploaded {package}")

# 以下、package.pyとstorage.pyの主要な機能の実装イメージ

# package.py

class Package:
    def __init__(self, name, version, language, description="", category="", tags=[]):
        self.name = name
        self.version = version
        self.language = language
        self.description = description
        self.category = category
        self.tags = tags
        self.metadata_file = "metadata.json"
        self.storage = StorageManager(bucket_name="your-bucket-name")

    def __str__(self):
        return f"{self.name} {self.version} ({self.language})"

    def install(self, force=False):
        """パッケージをインストールする"""
        package_path = get_package_path(self.name, self.version)
        if os.path.exists(package_path) and not force:
            raise FileExistsError(f"Package {self.name} {self.version} is already installed. Use --force to overwrite.")
        
        # ストレージからパッケージファイルをダウンロード
        print(f"デバッグ: ダウンロード開始: {self.name} {self.version}")
        self.storage.download_file(f"{self.name}/{self.version}", package_path)

        # パッケージメタデータを書き込む
        metadata = {
            "name": self.name,
            "version": self.version,
            "language": self.language,
            "description": self.description,
            "category": self.category,
            "tags": self.tags
        }
        with open(os.path.join(package_path, self.metadata_file), "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"Installed {self}")

    def uninstall(self):
        """パッケージをアンインストールする"""
        package_path = get_package_path(self.name, self.version)
        if not os.path.exists(package_path):
            raise FileNotFoundError(f"Package {self.name} {self.version} is not installed.")
        
        shutil.rmtree(package_path)
        print(f"Uninstalled {self}")

    def upload(self, package_path):
        """パッケージをアップロードする"""
        # ストレージにパッケージファイルをアップロード
        self.storage.upload_file(package_path, f"{self.name}/{self.version}/package.zip")

        # パッケージメタデータをアップロード
        metadata = {
            "name": self.name,
            "version": self.version,
            "language": self.language,
            "description": self.description,
            "category": self.category,
            "tags": self.tags
        }
        metadata_path = os.path.join(package_path, self.metadata_file)
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        self.storage.upload_file(metadata_path, f"{self.name}/{self.version}/metadata.json")

        print(f"Uploaded {self}")

    @classmethod
    def from_metadata(cls, metadata):
        return cls(
            name=metadata["name"],
            version=metadata["version"],
            language=metadata["language"],
            description=metadata.get("description", ""),
            category=metadata.get("category", ""),
            tags=metadata.get("tags", [])
        )