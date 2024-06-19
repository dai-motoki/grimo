from setuptools import setup, find_packages

setup(
    name='gowl',
    version='0.0.1',
    description='自然言語プログラムのテスト・評価システム',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',  # 追加: long_descriptionの形式を指定
    author='dai motoki',
    author_email='dai.motoki@gmail.com',
    url='https://github.com/dai-motoki/gowl',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests',
        'click',
        'colorama',
        'boto3',
        'streamlit',
        'aiohttp',
        'aiofiles',
        'i18nice[YAML]',
    ],
    entry_points={
        'console_scripts': [
            'gowl=gowl.cli:main',
        ],
    },
    package_data={
    '': ['*.txt', '*.md', '*.json', '*.csv', '*.yaml', '*.yml'],
    'gowl': ['i18n/*'],
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
