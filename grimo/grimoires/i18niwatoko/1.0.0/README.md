# 多言語翻訳 i18niwatoko

i18niwatokoはそれぞれの母国語からあらゆる国の言語に一斉翻訳するAIツールです。
そしてここに存在するプログラムファイルは全て各々の母国語のみで書いてあり、高級言語は一切無い、全く新しいプログラムファイルです。

![i18niwatoko](../readme_rich_progress.png)


## i18niwatokoの理念

言語の壁を越えて、誰もがプログラミングを楽しめる世界を目指して。

i18niwatokoは、多言語翻訳の課題に立ち向かうために生まれた革新的なツールです。従来の多言語翻訳ツールでは、英語をベースとしたプログラミング言語を扱う必要があり、非英語圏の人々にとってハードルが高いという問題がありました。

しかし、i18niwatokoは違います。自然言語でシステムを動かすことができるプログラミング言語であり、誰もが母国語でプログラムを書くことができるのです。さらに、i18niwatokoは日本語のメッセージファイルを一括で複数の言語に自動翻訳する機能を備えています。これにより、手作業での翻訳が不要となり、効率的に多言語対応を行うことができます。

プログラミングは特別な才能を持った一部の人だけのものではありません。言語の壁を取り払い、世界中の人々がプログラミングの楽しさと可能性を体験できる。それがi18niwatokoの崇高な理念なのです。

i18niwatokoとともに、言語の多様性を尊重しながら、プログラミングを通じて世界中の人々が創造性を発揮し、新しいアイデアを生み出せる社会を実現するために。

## 必要なもの

- Python 3.x
- niwatoko ライブラリ
- GCP Vertex AI
- Anthropic Claude API
- OpenAI API

## セットアップ

1. niwatoko ライブラリをインストールします。

   ```
   pip install --upgrade niwatoko
   ```

2. OpenAI、Anthropic、GCP Vertex AI の設定を行います。

   ```
   # OpenAI APIキーの設定
   # https://platform.openai.com/api-keys
   export OPENAI_API_KEY=your_openai_api_key
   
   # Anthropic APIキーの設定  
   # https://console.anthropic.com/settings/keys
   export ANTHROPIC_API_KEY=your_anthropic_api_key
   
   # GCP Vertex AIの設定
   # GCP Vertex AIからproject idとlocationを取得し手ください。（わからなくなったら 元木Xに 連絡ください https://x.com/ai_syacho）
   export GEMINI_PROJECT=your_gcp_project_id
   export GEMINI_LOCATION=asia-northeast1
   ```
   
   <!-- 説明 -->
   <!-- OpenAI、Anthropic、GCP Vertex AIのAPIキーとプロジェクト設定を環境変数に設定します。 -->
   <!-- your_openai_api_key、your_anthropic_api_key、your_gcp_project_idは実際のAPIキーとプロジェクトIDに置き換えてください。 -->
   <!-- GEMINI_LOCATIONはGCP Vertex AIのリージョンを指定します。ここではアジア東京リージョン(asia-northeast1)を指定しています。 -->

## 使い方

1. 翻訳定義ファイル(`def_translation.md`)を用意します。

2. 以下のコマンドを実行して、翻訳を開始します。
＊gemini-1.5-flashが安定していますが、基本的に自然言語プログラムは過渡期であり基本的に不安定です。3回ほど行うとほぼ確実に動くかとおもいます。
＊AI自体のハルシネーション、自然言語プログラムの文法研究などこちらも進行中なので、次第に安定性は増します。動かしたいと思ったら中間ファイルであるpythonを直接いじることをお勧めします。

   ```
   niwatoko def_translation.md -o exe_translation.py -m gemini-1.5-flash
   ```

3. 翻訳が完了すると、各言語のメッセージファイルが生成されます。

4. def_translation.mdは要件定義書です。詳細はこのファイルを修正してください。

## i18nとの関係性について
上記はi18nの形式サンプルで行っています。
 pip install i18nice[YAML].



## 翻訳言語

このプロジェクトでは、以下の言語に翻訳します。

- ベンガル語(bn)
- 中国語(zh)
- デンマーク語(da)
- ドイツ語(de)
- 英語(en)
- 英語(en)
- スペイン語(es)
- ペルシャ語(fa)
- フィンランド語(fi)
- フランス語(fr)
- ヒンディー語(hi)
- イタリア語(it)
- 韓国語(ko)
- オランダ語(nl)
- ノルウェー語(no)
- ポーランド語(pl)
- ポルトガル語(pt)
- ロシア語(ru)
- スウェーデン語(sv)
- タイ語(th)
- トルコ語(tr)
- ウクライナ語(uk)
- ベトナム語(vi)

## 注意事項

- 翻訳には時間がかかる場合があります。
- APIの利用制限に注意してください。
- 翻訳結果は完璧ではないため、必要に応じて手動で修正してください。

