import os
import rich
from rich.progress import track
from rich import print
from rich.panel import Panel
import anthropic
import time

# Anthropic APIキーを設定
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")

# 翻訳言語集
languages = {
    "bn": "ベンガル語",
    "zh": "中国語",
    "da": "デンマーク語",
    "de": "ドイツ語",
    "en": "英語",
    "es": "スペイン語",
    "fa": "ペルシャ語",
    "fi": "フィンランド語",
    "fr": "フランス語",
    "hi": "ヒンディー語",
    "it": "イタリア語",
    "ko": "韓国語",
    "nl": "オランダ語",
    "no": "ノルウェー語",
    "pl": "ポーランド語",
    "pt": "ポルトガル語",
    "ru": "ロシア語",
    "sv": "スウェーデン語",
    "th": "タイ語",
    "tr": "トルコ語",
    "uk": "ウクライナ語",
    "vi": "ベトナム語",
}

# 日本語ファイルの読み込み
with open("README.md", "r", encoding="utf-8") as f:
    japanese_content = f.read()

# Claude3のクライアントを作成
client = anthropic.Anthropic(api_key=anthropic_api_key)

# 翻訳の実行
for language_code, language_name in track(languages.items(), description="翻訳中..."):
    print(f"翻訳中... {language_name}翻訳...")
    # Claude3を利用して翻訳を実行
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"{japanese_content}を{language_name}で翻訳"
            }
        ]
    )

    # 翻訳結果をファイルに出力
    translated_content = message.content[0].text
    with open(f"Readme_translate/README_{language_code}.md", "w", encoding="utf-8") as f:
        f.write(translated_content)

    print(f"{language_name}翻訳完了")
    time.sleep(1)
