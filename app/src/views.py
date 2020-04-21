from elasticsearch import Elasticsearch
from flask import request, render_template

from src import app


@app.route('/', methods=['GET', 'POST'])
def show_results():
    es = Elasticsearch([{'host': 'es01', 'port': '9200'}])

    body = {
        "query": {
            "bool": {
                "must": []
            }
        },
        "sort": [
            {
                "hotelNo": {
                    "order": "asc"
                }
            }
        ]
    }

    if search_word := request.form.get('search_word'):
        body['query']['bool']['must'].append(
            {
                "bool": {
                    "should": [
                        {"match": {"hotelName": search_word}},
                        {"match": {"hotelKanaName": search_word}},
                        {"match": {"hotelSpecial": search_word}}
                    ]
                }
            }
        )
        body['highlight'] = {
            "fields": {
                "hotelName": {},
                "hotelKanaName": {},
                "hotelSpecial": {}
            }
        }

    if review_min := request.form.get('review_min'):
        body['query']['bool']['must'].append({"range": {"reviewAverage": {"gte": review_min}}})

    if review_max := request.form.get('review_max'):
        body['query']['bool']['must'].append({"range": {"reviewAverage": {"lte": review_max}}})

    if charge_min := request.form.get('charge_min'):
        body['query']['bool']['must'].append({"range": {"hotelMinCharge": {"gte": charge_min}}})

    if charge_max := request.form.get('charge_max'):
        body['query']['bool']['must'].append({"range": {"hotelMinCharge": {"lte": charge_max}}})

    result = es.search(index='hotel', body=body, size=1000)
    result_num = result['hits']['total']['value']
    hotels = result['hits']['hits']

    return render_template('index.html', result_num=result_num, hotels=hotels, request_form=request.form)
