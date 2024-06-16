import os
from supabase import create_client, Client
from supabase.storage import StorageFileAPI

class StorageManager:
    def __init__(self, bucket_name: str):
        supabase_url: str = os.environ.get('SUPABASE_URL')
        supabase_key: str = os.environ.get('SUPABASE__KEY')
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.storage: StorageFileAPI = self.supabase.storage()
        self.bucket_name: str = bucket_name

    async def upload_file(self, file_path: str, object_name: str) -> bool:
        """Supabase Storage にファイルをアップロードする

        :param file_path: アップロードするファイルのパス
        :param object_name: Storage バケット内のオブジェクト名
        :return: アップロードの成否
        """
        try:
            if not os.path.isfile(file_path):
                print(f"デバッグ: アップロードに失敗: {file_path} はファイルではありません")
                return False

            with open(file_path, "rb") as f:
                response = await self.storage.from_(self.bucket_name).upload(object_name, f)

            if response.error:
                print(f"デバッグ: アップロードに失敗: {response.error}")
                return False

            print(f"ファイルをアップロードしました: {response.data.path}")
            return True

        except Exception as e:
            print(f"デバッグ: アップロードに失敗: {e}")
            return False

    async def download_file(self, object_name: str, destination_path: str) -> bool:
        """
        Supabase Storage からファイルをダウンロードする

        :param object_name: Storage バケット内のオブジェクト名
        :param destination_path: ダウンロード先のパス
        :return: ダウンロードの成否
        """
        try:
            response = await self.storage.from_(self.bucket_name).download(object_name)

            if response.error:
                print(f"デバッグ: ダウンロードに失敗: {response.error}")
                return False
            
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            with open(destination_path, "wb") as f:
                f.write(response.content)
            print(f"{object_name} を {destination_path} にダウンロードしました。")
            return True

        except Exception as e:
            print(f"デバッグ: ダウンロードに失敗: {e}")
            return False

    async def delete_file(self, object_name: str) -> bool:
        """
        Supabase Storage からファイルを削除する

        :param object_name: Storage バケット内のオブジェクト名
        :return: 削除の成否
        """
        try:
            response = await self.storage.from_(self.bucket_name).remove([object_name])
            if response.error:
                print(f"デバッグ: 削除に失敗: {response.error}")
                return False
            print(f"ファイルを削除しました: {object_name}")
            return True
        except Exception as e:
            print(f"デバッグ: 削除に失敗: {e}")
            return False

    async def list_files(self, prefix: str = '') -> list:
        """
        Supabase Storage バケット内のファイル一覧を取得する

        :param prefix: 検索するプレフィックス
        :return: ファイル一覧
        """
        try:
            response = await self.storage.from_(self.bucket_name).list(path=prefix)
            if response.error:
                print(f"デバッグ: ファイル一覧の取得に失敗: {response.error}")
                return []
            return [file.name for file in response.data]
        except Exception as e:
            print(f"デバッグ: ファイル一覧の取得に失敗: {e}")
            return []