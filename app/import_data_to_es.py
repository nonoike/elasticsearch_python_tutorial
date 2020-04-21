import json

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConflictError


def main():
    with open('data/rakuten_hotels.json', 'r') as f:
        rakuten_hotels = json.load(f)

    es = Elasticsearch([{'host': 'es01', 'port': '9200'}])
    for rakuten_hotel in rakuten_hotels:
        hotel_basic_info = rakuten_hotel['hotel'][0]['hotelBasicInfo']
        try:
            es.create(index='hotel', id=hotel_basic_info['hotelNo'], body=hotel_basic_info)
        except ConflictError:
            print("conflict. hotelNo: {hotelNo}".format(hotelNo=hotel_basic_info['hotelNo']))
            pass


if __name__ == '__main__':
    main()
