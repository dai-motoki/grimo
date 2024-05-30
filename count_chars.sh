#!/bin/bash

total_chars=0

# 指定されたディレクトリ内のすべてのファイルに対して再帰的にループを実行
function process_files() {
  local dir="$1"
  
  # ディレクトリ内のすべてのファイルに対してループを実行
  for file in "$dir"/*; do
    # ファイルかどうかを確認
    if [ -f "$file" ]; then
      # ファイル名を表示
      echo "File: $file"
      # ファイルの文字数を取得し、合計に加算
      chars=$(wc -c < "$file")
      total_chars=$((total_chars + chars))
      echo "Characters: $chars"
    elif [ -d "$file" ]; then
      # サブディレクトリの場合は再帰的に処理
      process_files "$file"
    fi
  done
}

# 指定されたディレクトリを再帰的に処理
process_files "/Users/motokidaisuke/zoltraak/generated/grimoire_2024_v1"

# 全ての合計文字数を表示
echo "Total characters: $total_chars"