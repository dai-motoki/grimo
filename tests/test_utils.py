# test_utils.py
import unittest
from grimo.utils import (
    parse_package_name,
    validate_version,
    normalize_path,
    download_file,
    extract_archive,
)

class TestUtils(unittest.TestCase):
    def test_parse_package_name(self):
        # 正常系: パッケージ名が正しく解析される
        self.assertEqual(parse_package_name("package-name-1.0.0.tar.gz"), "package-name")
        self.assertEqual(parse_package_name("package_name-2.0.0-beta.zip"), "package_name")
        
        # 異常系: 不正なパッケージ名
        with self.assertRaises(ValueError):
            parse_package_name("invalid_package_name")
        
    def test_validate_version(self):
        # 正常系: 有効なバージョン
        self.assertTrue(validate_version("1.0.0"))
        self.assertTrue(validate_version("2.0.0-beta"))
        
        # 異常系: 不正なバージョン
        self.assertFalse(validate_version("invalid_version"))
        self.assertFalse(validate_version("1.0"))
        
    def test_normalize_path(self):
        # 正常系: パスが正規化される
        self.assertEqual(normalize_path("/path/to/dir"), "/path/to/dir")
        self.assertEqual(normalize_path("/path/to/dir/"), "/path/to/dir")
        self.assertEqual(normalize_path("/path/to/dir/../file"), "/path/to/file")
        
    def test_download_file(self):
        # 正常系: ファイルがダウンロードされる
        url = "https://example.com/file.txt"
        dest = "/tmp/file.txt"
        download_file(url, dest)
        self.assertTrue(os.path.exists(dest))
        
        # 異常系: 無効なURL
        with self.assertRaises(ValueError):
            download_file("invalid_url", dest)
        
    def test_extract_archive(self):
        # 正常系: アーカイブが展開される
        archive = "/path/to/archive.tar.gz"
        dest = "/tmp/extracted"
        extract_archive(archive, dest)
        self.assertTrue(os.path.exists(dest))
        
        # 異常系: 無効なアーカイブファイル
        with self.assertRaises(ValueError):
            extract_archive("/path/to/invalid_archive.txt", dest)

if __name__ == "__main__":
    unittest.main()
# 
# このテストファイルでは、`grimo.utils` モジュールの各関数に対して、正常系と異常系のテストケースを記述しています。
# 
# - `test_parse_package_name`: パッケージ名の解析が正しく行われるかをテスト
# - `test_validate_version`: バージョンの検証が正しく行われるかをテスト
# - `test_normalize_path`: パスの正規化が正しく行われるかをテスト
# - `test_download_file`: ファイルのダウンロードが正常に行われるかをテスト
# - `test_extract_archive`: アーカイブの展開が正常に行われるかをテスト
# 
# 異常系のテストでは、不正な入力値を与えた場合に適切な例外が発生することを確認しています。
# 
# 実際のテストでは、テスト用のダミーファイルやダミーのURLを用意し、ファイルの存在確認やダウンロード、展開が正しく行われることを検証します。
# 
# このように、ユーティリティ関数の主要な機能について