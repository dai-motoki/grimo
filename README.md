# 抽象プログラミング言語パッケージマネージャー「grimo」


## 0. 利用方法
＊ 現在パッケージマネージャーは各々ご自身のAWSアカウントにおけるS3バケットに格納する形になっています。
バージョンアップに従って、全員共有バケットにする予定です。


1. grimo install
```
pip install grimo
```

2. AWSのバケットとしてgrimoを作成

3. AWSのローカル設定を行う
```
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_ACCESS_KEY_ID=xxx
```

### コマンドラインオプション
```
                        利用可能なサブコマンド
    install             パッケージをインストールする（利用可）
    upload              パッケージをアップロードする（利用可）
    search              パッケージを検索する（未開発）
    update              パッケージをアップデートする（未開発）
    uninstall           パッケージをアンインストールする（未開発）
```

### パッケージのアップロード

```

project/
├── metadata.json # パッケージのメタデータ
├── package_name/
│   ├── def.md # パッケージの定義
│   ├── util.md # パッケージのユーティリティ
│   ├── var.md # パッケージの変数
│   └── ...

```

```metadata.json

{
  "name": "package_name",
  "version": "1.0.0",
  "language": "python",
  "description": "package_description",
  "category": "ai",
  "tags": [
    "tool",
    "development"
  ]
}
```

project ディレクトリ内で
```
grimo upload .

```


### 検索コマンド

`grimo search` コマンドは、指定されたクエリに基づいてパッケージを検索するために使用されます。以下はその使い方です。

### 使用方法

```sh
grimo search <query> [オプション]
```

### 引数

- `<query>`: 検索クエリを指定します。
ex. grimo search "banner"

### オプション

- `-l`, `--language <言語>`: 言語を指定します。（別の-lコマンドとバッティングしているので修正します）
- `-c`, `--category <カテゴリ>`: カテゴリを指定します。
- `-t`, `--tags <タグ>`: タグを指定します。複数のタグをスペースで区切って指定できます。

### 例

1. 基本的な検索:
    ```sh
    grimo search "example query"
    ```

2. 言語を指定して検索: （
    ```sh
    grimo search "example query" --language "python"
    ```

3. カテゴリを指定して検索:
    ```sh
    grimo search "example query" --category "utilities"
    ```

4. タグを指定して検索:
    ```sh
    grimo search "example query" --tags "tag1" "tag2"
    ```

このコマンドを使用することで、指定された条件に一致するパッケージを簡単に検索することができます。




## 開発者向け
### パッケージのインストール

インストールされたファイルはgrimoiresディレクトリに格納されます。
-v でバージョン指定をお願いします（ここも何も指定がない場合最新を取得するようにする予定です）

```
grimo install package_name -v version

project/
├── grimoires/
│   ├── package_name/
│   │   ├── metadata.json # パッケージのメタデータ
│   │   ├── def.md # パッケージの定義
│   │   ├── util.md # パッケージのユーティリティ
│   │   ├── var.md # パッケージの変数
│   │   └── ...

```

## 1. 目的

多様なプログラミング言語のパッケージを一元管理できる、強力かつユーザーフレンドリーな抽象プログラミング言語パッケージマネージャー「grimo」をPythonで実装する。grimoは、プログラミング言語に依存せず、あらゆるパッケージの検索、インストール、アップグレードをシームレスに実行できるツールを目指します。

## 2. パッケージの基本構造

```
grimo/
├── grimo/                # パッケージのコアロジック
│   ├── __init__.py
│   ├── core.py
│   ├── utils.py
│   ├── package.py      # パッケージ操作関連モジュール
│   ├── storage.py      # ストレージ操作関連モジュール
│   └── ...
├── tests/
│   ├── test_core.py
│   ├── test_utils.py
│   ├── test_package.py
│   ├── test_storage.py
│   └── ...
├── docs/
│   ├── conf.py
│   ├── index.rst
│   └── ...
├── README.md
├── LICENSE
├── setup.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml
└── app.py                # Streamlit/Gradio アプリケーション
```

## 3. setup.pyの記述

```python
from setuptools import setup, find_packages

setup(
    name='grimo',
    version='0.1.0',
    description='Abstract Programming Language Package Manager',
    long_description=open('README.md', 'r').read(),
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/your-username/grimo',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests',
        'click',
        'colorama',
        'boto3',          # AWS SDK for Python
        'streamlit',      # or 'gradio'
    ],
    entry_points={
        'console_scripts': [
            'grimo=grimo.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
```


## 3. setup.pyを利用したPyPIへのアップロード方法

1. **PyPIアカウントの作成**:
   - まず、[PyPI](https://pypi.org/) にアカウントを作成します。

2. **`setup.py`の準備**:
   - `setup.py` ファイルが正しく記述されていることを確認します。例として以下のような内容です。

   ```python
   from setuptools import setup, find_packages

   setup(
       name='grimo',
       version='0.1.0',
       description='Abstract Programming Language Package Manager',
       long_description=open('README.md', 'r').read(),
       author='Your Name',
       author_email='your@email.com',
       url='https://github.com/your-username/grimo',
       packages=find_packages(exclude=['tests']),
       install_requires=[
           'requests',
           'click',
           'colorama',
           'boto3',
           'streamlit',
       ],
       entry_points={
           'console_scripts': [
               'grimo=grimo.cli:main',
           ],
       },
       classifiers=[
           'Development Status :: 3 - Alpha',
           'Intended Audience :: Developers',
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 3',
           'Programming Language :: Python :: 3.7',
           'Programming Language :: Python :: 3.8',
           'Programming Language :: Python :: 3.9',
           'Programming Language :: Python :: 3.10',
       ],
   )
   ```

3. **必要なパッケージのインストール**:
   - パッケージをアップロードするために、`twine` をインストールします。
     ```sh
     pip install twine
     ```

4. **パッケージのビルド**:
   - パッケージをビルドします。
     ```sh
     python setup.py sdist bdist_wheel
     ```

5. **PyPIへのアップロード**:
   - `twine` を使用してパッケージをPyPIにアップロードします。
     ```sh
     twine upload dist/*
     ```

6. **アップロードの確認**:
   - アップロードが成功したかどうかをPyPIのウェブサイトで確認します。

これで、`setup.py` を利用してパッケージをPyPIにアップロードする手順は完了です。




## 4. __init__.py の役割

- パッケージの初期化処理
- `__version__` 変数でパッケージバージョンを定義
- パッケージの公開APIをインポート

## 5. README.md の記述内容

- **パッケージの概要**: grimoの目的、機能、メリットを具体的に記述
- **インストール方法**: `pip install grimo` 等の手順を明記
- **使用方法**: 基本的なコマンド (`grimo install`, `grimo search` など) の使用例を提示
- **サポートするプログラミング言語とパッケージ**: 具体的に記載
- **ライセンス**: パッケージのライセンス情報を記載
- **貢献方法**: バグ報告、プルリクエスト、ドキュメント改善などの方法を説明
- **サポート方法**: 問い合わせ先 (メーリングリスト、Issue tracker、Slackチャンネルなど) を記載

## 6. LICENSE ファイル

- **MIT License** 
- **Apache License 2.0**
- **GNU General Public License (GPL)**
- **BSD License** 
  上記から選択、またはその他の適切なライセンスを明記

## 7. パッケージのバージョン管理

- セマンティックバージョニング (MAJOR.MINOR.PATCH) を採用

## 8. テスト

- ユニットテストと統合テストを実施
  - `unittest` モジュールを使用
  - テストケース: 正常系、異常系、境界値などを網羅
  - カバレッジ測定: `coverage.py` などを使用
  - CLIコマンドの実行結果を検証: 
    - 異なるコマンドラインオプション、引数の組み合わせをテスト
    - 想定される標準出力、標準エラー出力を検証
    - エラー処理 (不正な引数、ファイルが存在しない場合など) をテスト

## 9. ドキュメント作成

- Sphinx を使用し、以下の内容を記述
  - インストール方法
  - コマンドリファレンス: `grimo install`, `grimo search` など、各コマンドの詳細な説明、オプション、使用例を記載
  - APIドキュメント
  - パッケージの依存関係
  - 開発者向けドキュメント: 貢献方法、テスト方法、コーディング規約など
  - ドキュメントはHTML形式で生成し、Vercel等を用いてWeb上に公開

## 10. Docker化とCI/CD

- Docker:
  - `Dockerfile` でビルドと実行環境を定義
  - `docker-compose.yml` で複数コンテナ (アプリケーション、データベースなど) を定義
- CI/CD:
  - GitHub Actions を使用
  - `ci.yml`:
    - push, pull request 毎に実行
    - コードチェック (flake8, pylint など)、テスト実行、カバレッジ測定
  - `cd.yml`:
    - タグプッシュ時に実行
    - Dockerイメージのビルド、Docker Hub への push
    - PyPI へのパッケージリリース

## 11. Webアプリケーション (Streamlit/Gradio)

- UI:
  - パッケージの検索: 
    - キーワード検索
    - プログラミング言語、カテゴリ、タグによる絞り込み
  - パッケージの詳細表示:
    - パッケージ名、バージョン、説明、作者、ライセンス、依存関係などを表示
    - README.md の内容を表示
  - パッケージのインストール、アップデート、アンインストール:
    - プログレスバーを表示
    - エラー発生時はエラーメッセージを表示
  - パッケージのアップロード:
    - パッケージ名、バージョン、説明、プログラミング言語、カテゴリ、タグなどを設定
    - パッケージファイルをアップロード
- バックエンド:
  - `grimo` パッケージのコマンドを呼び出して処理を実行
  - AWS S3 などのストレージサービスと連携し、パッケージファイルを保存、取得

## 12. ストレージ

- AWS S3 を使用
  - Terraform を使用して S3 バケットを作成、管理
  - パッケージファイル (テキスト、画像、動画など) を保存
- `grimo.storage` モジュール:
  - S3 へのファイルアップロード、ダウンロード、削除機能を提供
  - ファイルのメタデータ (パッケージ名、バージョン、説明など) を保存、取得する機能を提供

## 13. その他

- ロギング: 処理の記録、エラー発生時の原因究明に役立てる
- エラー処理: 想定されるエラーを適切に処理し、分かりやすいエラーメッセージを表示
- セキュリティ: パッケージのアップロード、ダウンロード時のセキュリティ対策を実施
- パフォーマンス: 処理速度の向上、リソース使用量の削減に取り組む

## 14. 開発体制

- チームで開発を行う場合は、GitHub Flow などの開発フローを定義し、円滑な開発を進める

## 15. 今後の展望

- パッケージの依存関係解決機能の追加
- 仮想環境管理機能の追加
- GUIクライアントの開発
- プラグイン機構による拡張性の向上
