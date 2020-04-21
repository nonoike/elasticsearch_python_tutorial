from elasticsearch import Elasticsearch
from flask import request

from src import app


@app.route('/')
def show_results():
    es = Elasticsearch([{'host': 'es01', 'port': '9200'}])

    body = {
        "query": {
            "bool": {
                "must": []
            }
        },
        "highlight": {
            "fields": {
                "hotelSpecial": {}
            }
        }
    }

    if search_word := request.form.get('search_word'):
        body['query']['bool']['must'].append(
            {
                "bool": {
                    "should": [
                        {"match": {"hotelName": request.form.get(search_word)}},
                        {"match": {"hotelKanaName": request.form.get(search_word)}},
                        {"match": {"hotelSpecial": request.form.get(search_word)}}
                    ]
                }
            }
        )

    if review_min := request.form.get('review_min'):
        body['query']['bool']['must'].append({"range": {"reviewAverage": {"gte": request.get(review_min)}}})

    if review_max := request.form.get('review_max'):
        body['query']['bool']['must'].append({"range": {"reviewAverage": {"gte": request.get(review_max)}}})

    result = es.search(index='hotel', body=body, size=1000)
    result_num = result['hits']['total']['value']
    hotels = result['hits']['hits']

    return str(hotels)
