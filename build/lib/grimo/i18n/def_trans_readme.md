## 引用

- `翻訳言語集` = [./multilang.md]
- `日本語ファイル` = [./README.md]
- `claude3` = [./claude.md]

## TODO

以下の手順で翻訳を行います。

1. 以下を`翻訳言語集`にて`言語`に対して繰り返し実行します

出力表示は以下の通り （以下1行1行全て表示を残して、ピラミッドのようにして欲しい） 
翻訳中...                                           0% -:--:--Traduction en français terminée
翻訳中... ━╸                                         4% -:--:--Übersetzung ins Deutsche abgeschlossen
翻訳中... ━━━                                        9% 0:02:47Translation into English completed

    - rich.progressを利用してプログレスバーを表示
    - `出力ファイル形式` = README_`言語記号`.md（例えばREADME_fr.mdなど）
    - 実行状況がわかるように、進行バーと隣に何の言語を翻訳しているか記述
    1-1. Claude3実行、以下変数群は忠実に再現
    1-1. Claude3を利用して翻訳を実行します。以下の変数を設定してください。
        - japanese_content: `日本語ファイル`の内容を読み込んで設定
        - model: haikuを指定
        - messages: 以下の形式で設定
            [
                {
                    "role": "user",
                    "content": "{japanese_content}を{language_name}で翻訳"
                }
            ]
        注意: `日本語ファイル`を1行ずつ訳すのではなく、一括翻訳すること
    2. `出力ファイル形式`で出力します
    3. 翻訳結果をファイルに出力
        - Readme_translate/ ディレクトリに前ファイル格納。ファイルは上書き
        - encoding="utf-8"
        - "{language_name}翻訳完了"と書く
        - 翻訳完了は各々の言語で記載


## 実行言語
- python
- 1枚のファイル

## 条件
- `日本語ファイル`と同じスタイルで出力
- 注意: `日本語ファイル`を1行ずつ訳すのではなく、一括翻訳すること
- allow_unicode=True 文字化け対策
- if __name__ == "__main__": は使わない

