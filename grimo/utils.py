# utils.py

import os
import logging
from colorama import Fore, Style

def setup_logger(name, level=logging.INFO):
    """ロガーを設定する"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def print_success(message):
    """成功メッセージを緑色で表示する"""
    print(Fore.GREEN + message + Style.RESET_ALL)

def print_error(message):
    """エラーメッセージを赤色で表示する"""
    print(Fore.RED + message + Style.RESET_ALL)

def print_warning(message):
    """警告メッセージを黄色で表示する"""
    print(Fore.YELLOW + message + Style.RESET_ALL)

def get_package_dir(package_name):
    """パッケージのディレクトリパスを取得する"""
    return os.path.join(os.getcwd(), package_name)

def get_package_file(package_name, filename):
    """パッケージ内のファイルパスを取得する"""
    package_dir = get_package_dir(package_name)
    return os.path.join(package_dir, filename)

def read_file(file_path):
    """ファイルを読み込む"""
    with open(file_path, 'r') as f:
        return f.read()

def write_file(file_path, content):
    """ファイルに書き込む"""
    with open(file_path, 'w') as f:
        f.write(content)

def run_command(command):
    """コマンドを実行する"""
    return os.system(command)