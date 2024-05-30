# test_core.py
# コアロジックのテストケースを記述

import unittest
from unittest.mock import patch, MagicMock
from grimo import core

class TestCore(unittest.TestCase):
    
    def setUp(self):
        # テスト前の準備
        pass

    def tearDown(self):
        # テスト後の後処理
        pass

    def test_search_package(self):
        # パッケージ検索機能のテスト
        # 正常系: キーワードに合致するパッケージが見つかる場合
        with patch('grimo.core.search_package_by_keyword', return_value=['package1', 'package2']):
            result = core.search_package('keyword')
            self.assertEqual(result, ['package1', 'package2'])
        
        # 異常系: キーワードに合致するパッケージが見つからない場合  
        with patch('grimo.core.search_package_by_keyword', return_value=[]):
            result = core.search_package('invalid_keyword')
            self.assertEqual(result, [])

    def test_install_package(self):
        # パッケージインストール機能のテスト
        # 正常系: パッケージが正常にインストールされる場合
        mock_package = MagicMock()
        mock_package.install.return_value = True
        with patch('grimo.core.get_package', return_value=mock_package):
            result = core.install_package('package_name', '1.0.0')
            self.assertTrue(result)
            mock_package.install.assert_called_once_with('1.0.0')

        # 異常系: 指定したバージョンのパッケージが存在しない場合
        with patch('grimo.core.get_package', return_value=None):
            with self.assertRaises(ValueError):
                core.install_package('invalid_package', '1.0.0')

    def test_update_package(self):
        # パッケージ更新機能のテスト
        # 正常系: パッケージが正常に更新される場合
        mock_package = MagicMock()
        mock_package.update.return_value = True
        with patch('grimo.core.get_installed_package', return_value=mock_package):
            result = core.update_package('package_name')
            self.assertTrue(result)
            mock_package.update.assert_called_once()

        # 異常系: 指定したパッケージがインストールされていない場合
        with patch('grimo.core.get_installed_package', return_value=None):
            with self.assertRaises(ValueError):
                core.update_package('not_installed_package')

    def test_uninstall_package(self):
        # パッケージアンインストール機能のテスト
        # 正常系: パッケージが正常にアンインストールされる場合
        mock_package = MagicMock()
        mock_package.uninstall.return_value = True
        with patch('grimo.core.get_installed_package', return_value=mock_package):
            result = core.uninstall_package('package_name')
            self.assertTrue(result)
            mock_package.uninstall.assert_called_once()

        # 異常系: 指定したパッケージがインストールされていない場合
        with patch('grimo.core.get_installed_package', return_value=None):
            with self.assertRaises(ValueError):
                core.uninstall_package('not_installed_package')

    def test_upload_package(self):
        # パッケージアップロード機能のテスト
        # 正常系: パッケージが正常にアップロードされる場合
        with patch('grimo.