# docker-django

## 📚 概要
私用で作ったdjangoアプリの開発用docker-composeとその他諸々  
外部リポジトリにdjangoリポジトリを取り込める設定込み

## 🌏 動作環境
- ubuntu :16.*, 18.*

## ⚙ 使用法
- ノード生成
    1. 必要モジュール
        - python-dotenv  
        `pip install python-dotenv`
    1. `config.py`を実行。応答で必要情報を.envに書き出したり情報を付与したマウント用ファイルを生成する。  
        `python3 config.py`  
        - オプション  
            - `--reset` or `-r`: 設定ファイルをすべてリセット  
    1. (初回のみ)イメージ作成  
        `docker-compose build`
    1. コンテナ生成
        `sudo python3 init.py`  
        - ボリュームやlogの削除は都度判断。
        - nodeの種類を切り替えたい場合config.pyをサイド実施してコンテナ生成スクリプトを再実行。
