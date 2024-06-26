# 校舎の午後のイメージ画像とストーリー生成要件定義書

## 引用
- `OpenAI` = [./OpenAI.md] 
- `画像生成` = `OpenAI`.画像生成
- `音声合成` = `OpenAI`.音声合成


## TODO
1.  `画像生成`と`音声合成`を使って校舎の午後のイメージ画像とナレーションを作る
    - 画像に関する情報
    - `イメージテーマ` = "夏の午後の校舎の風景。青空に大きな入道雲が浮かび、校舎に影を落としている。窓から差し込む日差しが教室の机に反射し、静かな雰囲気を醸し出している。" 
    - `イメージスタイル` = "リアルな写真のようなディテールのあるイラスト。光と影のコントラストを強調し、夏の暑さと静けさを表現する。"
    - `ナレーション文章`から音声を作る
      - "夏の午後、青空に大きな入道雲が浮かんでいます。雲の影が校舎に落ち、教室にひんやりとした空気が流れ込んでいます。窓からの日差しが机に反射し、静かな雰囲気が漂っています。"

2. `字幕ファイル`を作る
    - `ナレーション文章`から字幕を作る
    - 字幕ファイル形式 = "srt"

3. `画像ファイル`を`字幕ファイル`と同じ長さの`動画ファイル`に変換する
    - ffmpegを使用して画像ファイルを動画ファイルに変換
    - mediaディレクトリに保存

4. `画像ファイル`と`音声ファイル`と`字幕ファイル`から`ビデオファイル`を作る
    - ffmpegを使用してビデオファイルを生成
      - `音声ファイル`を読み込んで`オーディオクリップ`を作成 
      - `字幕ファイル`を読み込んで`字幕トラック`を作成
      - `ビデオクリップ`、`オーディオクリップ`、`字幕トラック`を結合
    - 生成したビデオファイルをmediaディレクトリに保存

## 成果物
- 成果物は全て./mediaディレクトリに格納
- mediaディレクトリがない場合は作成

## 実行言語
- python 
- 1枚のファイル

## 制約
- import requests, os を必ず記述するように
- '__file__' はつかわない
- OPENAI_API_KEYを環境変数に設定する
- サーバーの立ち上げはしない。
- ffmpegのコマンドが長いとエラーが出るので、改行を入れる
- if __name__ == "__main__": を使わない