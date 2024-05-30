# test_package.py
# パッケージ操作関連モジュールのテストケースを記述

import unittest
from unittest.mock import patch, MagicMock
from grimo.package import Package, install, uninstall, search, upgrade

class TestPackage(unittest.TestCase):

    def setUp(self):
        self.package = Package('test_package', '1.0.0', 'Test package', 'Python')

    def test_package_init(self):
        self.assertEqual(self.package.name, 'test_package')
        self.assertEqual(self.package.version, '1.0.0')
        self.assertEqual(self.package.description, 'Test package')
        self.assertEqual(self.package.language, 'Python')

    def test_package_str(self):
        self.assertEqual(str(self.package), 'test_package-1.0.0')

    def test_package_repr(self):
        self.assertEqual(repr(self.package), '<Package test_package-1.0.0>')

    @patch('grimo.package.subprocess.run')
    def test_install_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        result = install(self.package)
        self.assertTrue(result)

    @patch('grimo.package.subprocess.run')
    def test_install_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)
        result = install(self.package)
        self.assertFalse(result)

    @patch('grimo.package.subprocess.run')
    def test_uninstall_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        result = uninstall(self.package)
        self.assertTrue(result)

    @patch('grimo.package.subprocess.run')
    def test_uninstall_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)
        result = uninstall(self.package)
        self.assertFalse(result)

    @patch('grimo.package.requests.get')
    def test_search_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'name': 'test_package1', 'version': '1.0.0', 'description': 'Test package 1', 'language': 'Python'},
            {'name': 'test_package2', 'version': '2.0.0', 'description': 'Test package 2', 'language': 'Python'}
        ]
        mock_get.return_value = mock_response
        results = search('test')
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], Package)
        self.assertIsInstance(results[1], Package)

    @patch('grimo.package.requests.get')
    def test_search_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        results = search('test')
        self.assertEqual(results, [])

    @patch('grimo.package.subprocess.run')
    def test_upgrade_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        result = upgrade(self.package)
        self.assertTrue(result)

    @patch('grimo.package.subprocess.run')
    def test_upgrade_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)
        result = upgrade(self.package)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()