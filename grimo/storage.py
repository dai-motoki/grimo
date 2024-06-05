import boto3
from botocore.exceptions import ClientError
import logging
import os

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, bucket_name, region_name="ap-northeast-1"):
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        self.bucket_name = bucket_name

    def upload_file(self, file_path, object_name):
        """S3バケットにファイルをアップロードする

        :param file_path: アップロードするファイルのパス
        :param object_name: S3バケット内のオブジェクト名
        :return: アップロードの成否
        """
        try:
            if os.path.isfile(file_path):  # file_pathがファイルかどうかチェックを追加
                bucket = self.s3.Bucket(self.bucket_name)

                bucket.put_object(
                    Key=object_name,
                    Body=open(file_path, 'rb')
                )
            else:
                print(f"デバッグ: アップロードに失敗: {file_path}はファイルではありません")  # デバッグ用のprint文を追加
                return False
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download_file(self, object_name, version):
        """
        S3バケットからファイルをダウンロードする

        :param object_name: S3バケット内のオブジェクト名
        :param version: オブジェクトのバージョン
        :return: ダウンロードの成否
        """
        try:
            prefix = f"{object_name}/{version}/"

            # バケット内のオブジェクト一覧を取得
            objects = self.s3.Bucket(self.bucket_name).objects.filter(Prefix=prefix)
            for obj in objects:
                # 各オブジェクトをダウンロード
                # grimoires_dir = os.path.join(os.getcwd(), "grimoires")
                package_first_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                grimoires_dir = os.path.join(package_first_dir, "grimoires")
                file_path = os.path.join(grimoires_dir, obj.key)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                self.s3.Object(self.bucket_name, obj.key).download_file(file_path)
                print(f"{obj.key} を {file_path} にダウンロードしました。")
            
        except ClientError as e:
            print(f"デバッグ: ダウンロードに失敗: {e}")  # デバッグ用のprint文を追加
            logging.error(e)
            return False
        return True

    def delete_file(self, object_name):
        """
        S3バケットからファイルを削除する

        :param object_name: S3バケット内のオブジェクト名
        :return: 削除の成否
        """
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def list_files(self, prefix=''):
        """
        S3バケット内のファイル一覧を取得する

        :param prefix: 検索するプレフィックス
        :return: ファイル一覧
        """
        try:
            # list_objects_v2メソッドはs3.ServiceResourceには存在しないため、クライアントを使用する
            response = self.s3.meta.client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            files = [content['Key'] for content in response.get('Contents', [])]
        except ClientError as e:
            logging.error(e)
            return None
        return files

    def get_file_metadata(self, object_name):
        """
        S3バケット内のファイルのメタデータを取得する

        :param object_name: S3バケット内のオブジェクト名
        :return: ファイルのメタデータ
        """
        try:
            import json
            obj = self.s3.Object(self.bucket_name, object_name)
            metadata = json.loads(obj.get()['Body'].read().decode('utf-8'))

        except ClientError as e:
            logging.error(e)
            return None
        return metadata

    def set_file_metadata(self, object_name, metadata):
        """
        S3バケット内のファイルにメタデータを設定する

        :param object_name: S3バケット内のオブジェクト名
        :param metadata: 設定するメタデータ
        :return: 設定の成否
        """
        try:
            self.s3.copy_object(Bucket=self.bucket_name, 
                                CopySource={'Bucket': self.bucket_name, 'Key': object_name},
                                Key=object_name,
                                Metadata=metadata,
                                MetadataDirective='REPLACE')
        except ClientError as e:
            logging.error(e)
            return False
        return True
# 
# このモジ