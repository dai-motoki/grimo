# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'grimo'
copyright = '2023, Your Name'
author = 'Your Name'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for autodoc extension -------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'special-members': '__init__',
    'inherited-members': True,
    'show-inheritance': True,
}

# -- Options for napoleon extension ------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#configuration

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
# 
# このSphinxの設定ファイル(`conf.py`)では以下の設定を行っています。
# 
# 1. プロジェクト情報の設定
#    - プロジェクト名、著作権表示、作者名、リリースバージョンを指定
# 
# 2. 一般的な設定
#    - 拡張機能の指定 (`autodoc`, `viewcode`, `napoleon`)
#    - テンプレートファイルのパスを指定
#    - ビルド時に除外するファイルパターンを指定
# 
# 3. HTML出力オプション
#    - HTMLテーマを指定 (`alabaster`)
#    - 静的ファイル (画像など) のパスを指定
# 
# 4. `autodoc` 拡張機能のオプション
#    - メンバーの表示順序 (`bysource`: ソースコードの順番)
#    - デフォルトオプションの設定
#      - `members`: モジュールのメンバーを含める
#      - `undoc-members`: docstringが無いメンバーも含める
#      - `private-members`: プライベートメンバー (`_` から始まる) も含める
#      - `special-members`: 特殊メソッド (`__init__` など) を含める
#      - `inherited-members`: 継承したメンバーを含める
#      - `show-inheritance`: クラスの継承関係を表示する
# 
# 5. `napoleon` 拡張機能のオプション
#    - Google形式とNumPy形式のdocstringをサポート
#    - `__init