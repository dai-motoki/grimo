# package.py

import os
import shutil
import json
import requests
from typing import List, Dict
from .storage import StorageManager
from .utils import get_package_dir, get_package_file, print_success, print_error, print_warning

class Package:
    def __init__(self, name: str, version: str, language: str, description: str = "", category: str = "", tags: List[str] = []):
        self.name = name
        self.version = version
        self.language = language
        self.description = description
        self.category = category
        self.tags = tags
        self.metadata_file = "metadata.json"
        self.storage = StorageManager(bucket_name="grimo")

    def __str__(self):
        return f"{self.name} {self.version} ({self.language})"

    def install(self, force: bool = False) -> None:
        package_path = get_package_dir(self.name)
        if os.path.exists(package_path) and not force:
            raise FileExistsError(f"Package {self.name} {self.version} is already installed. Use --force to overwrite.")
        
        # ストレージからパッケージファイルをダウンロード
        if not self.storage.download_file(f"{self.name}/{self.version}", package_path):
            raise RuntimeError(f"Failed to download package {self.name} {self.version} from storage.")

        # パッケージメタデータを書き込む
        metadata = {
            "name": self.name,
            "version": self.version,
            "language": self.language,
            "description": self.description,
            "category": self.category,
            "tags": self.tags
        }
        with open(get_package_file(self.name, self.metadata_file), "w") as f:
            json.dump(metadata, f, indent=2)

        print_success(f"Installed {self}")

    def uninstall(self) -> None:
        package_path = get_package_dir(self.name)
        if not os.path.exists(package_path):
            raise FileNotFoundError(f"Package {self.name} {self.version} is not installed.")
        
        shutil.rmtree(package_path)
        print_success(f"Uninstalled {self}")

    def upload(self, package_path: str) -> None:                                                                # パッケージをアップロードする関数
        package_dir = get_package_dir(self.name)
        for root, _, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, package_dir)
                storage_path = f"{self.name}/{self.version}/{relative_path}"
                if not self.storage.upload_file(file_path, storage_path):
                    raise RuntimeError(f"Failed to upload file {file_path} to storage at {storage_path}.")
                print("Uploaded: " + file)

        print_success(f"Uploaded all files for {self}")
    @classmethod
    def from_metadata(cls, metadata: Dict[str, str]) -> 'Package':
        return cls(
            name=metadata["name"],
            version=metadata["version"],
            language=metadata["language"],
            description=metadata.get("description", ""),
            category=metadata.get("category", ""),
            tags=metadata.get("tags", [])
        )

def search_packages(query: str = "", language: str = "", category: str = "", tags: List[str] = []) -> List[Package]:
    packages = []
    metadata_list = StorageManager(bucket_name="grimo").list_files()
    for metadata in metadata_list:
        package = Package.from_metadata(metadata)
        if query and query not in package.name:
            continue
        if language and language != package.language:
            continue
        if category and category != package.category:
            continue
        if tags and not set(tags).issubset(set(package.tags)):
            continue
        packages.append(package)
    return packages

def get_package(object_name: str, version: str) -> Package:
    # print(f"デバッグ: package.pyのget_package関数が呼び出されました。")
    # print(f"デバッグ: object_name: {object_name}, version: {version}")
    # メタデータを取得する
    try:
        # metadata = StorageManager(bucket_name="grimo").get_file_metadata(f"{name}/{version}/metadata.json")
        metadata = StorageManager(bucket_name="grimo").download_file(object_name, version)
        # print(f"デバッグ: 取得したメタデータ: {metadata}")  #  デバッグ用のprint文を追加
    except AttributeError as e:
        if "'s3.ServiceResource' object has no attribute 'head_object'" in str(e):
            raise RuntimeError("S3のServiceResourceオブジェクトにhead_object属性がありません。S3の設定を確認してください。")
        else:
            raise
    if not metadata:
        raise ValueError(f"Package {object_name} {version} not found.")
    # return Package.from_metadata(metadata)
# 
