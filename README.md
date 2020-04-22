# elasticsearch_python_tutorial
[「Pythonで作るはじめてのElasticsearchアプリケーション」サンプルコード](https://github.com/chaingng/elasticsearch_python_tutorial) の写経

# 実行
0. `app/fetch_hotels_from_rakuten.py`にアプリIDを設定する
1. dockerを起動する `docker-compose.yml up -d`
2. 楽天トラベル施設検索APIを実行しレスポンスをファイル保存する `docker exec elasticsearch_python_tutorial_app python fetch_hotels_from_rakuten.py`
3. 保存したレスポンスをElasticsearchにインポートする `docker exec elasticsearch_python_tutorial_app python import_data_to_es.py`
4. http://0.0.0.0:5000/ にアクセス
