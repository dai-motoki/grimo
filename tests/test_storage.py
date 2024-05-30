import unittest
from unittest.mock import patch, MagicMock
from grimo.storage import Storage

class TestStorage(unittest.TestCase):
    
    def setUp(self):
        self.storage = Storage()

    @patch('boto3.client')
    def test_upload_package(self, mock_boto3_client):
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        
        self.storage.upload_package('test_package.tar.gz', 'package_name', '1.0.0', 'Test package')
        
        mock_boto3_client.assert_called_once_with('s3')
        mock_s3.upload_file.assert_called_once_with(
            'test_package.tar.gz',
            self.storage.bucket_name,
            'packages/package_name/1.0.0/package_name-1.0.0.tar.gz',
            ExtraArgs={'Metadata': {'name': 'package_name', 'version': '1.0.0', 'description': 'Test package'}}
        )

    @patch('boto3.client')
    def test_download_package(self, mock_boto3_client):
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        
        self.storage.download_package('package_name', '1.0.0', 'test_package.tar.gz')
        
        mock_boto3_client.assert_called_once_with('s3')
        mock_s3.download_file.assert_called_once_with(
            self.storage.bucket_name,
            'packages/package_name/1.0.0/package_name-1.0.0.tar.gz',
            'test_package.tar.gz'
        )

    @patch('boto3.client')
    def test_delete_package(self, mock_boto3_client):
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        
        self.storage.delete_package('package_name', '1.0.0')
        
        mock_boto3_client.assert_called_once_with('s3')
        mock_s3.delete_object.assert_called_once_with(
            Bucket=self.storage.bucket_name,
            Key='packages/package_name/1.0.0/package_name-1.0.0.tar.gz'
        )

    @patch('boto3.client')
    def test_get_package_metadata(self, mock_boto3_client):
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        mock_s3.head_object.return_value = {
            'Metadata': {
                'name': 'package_name',
                'version': '1.0.0',
                'description': 'Test package'
            }
        }
        
        metadata = self.storage.get_package_metadata('package_name', '1.0.0')
        
        self.assertEqual(metadata, {
            'name': 'package_name',
            'version': '1.0.0',
            'description': 'Test package'
        })
        
        mock_boto3_client.assert_called_once_with('s3')
        mock_s3.head_object.assert_called_once_with(
            Bucket=self.storage.bucket_name,
            Key='packages/package_name/1.0.0/package_name-1.0.0.tar.gz'
        )

if __name__ == '__main__':
    unittest.main()
# 
# このテストケースでは、`grimo.storage` モジュールの主要な機能をテストしています。
# 
# 1. `test_upload_package`: パッケージのアップロード処理をテスト
#    - `