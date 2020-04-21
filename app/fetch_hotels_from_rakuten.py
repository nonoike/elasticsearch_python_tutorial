import json
import time

import requests

APPLICATION_ID = "dummy"
TOKYO_STATION_LATITUDE = 128440.51
TOKYO_STATION_LONGITUDE = 503172.21
SEARCH_RADIUS = 3.0
API_BASE_URL = 'https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426'

SLEEP_SEC = 1


def main():
    page = 0
    hotels = []
    while (page := page + 1) <= 20:  # avoid infinite loop
        response_json = fetch_api_response_json(page)
        page_count = response_json['pagingInfo']['pageCount']
        hotels.extend(response_json['hotels'])

        print('finish {page} / {pageCount} loop.'.format(page=page, pageCount=page_count))
        if response_json['pagingInfo']['pageCount'] <= page:
            break
        time.sleep(SLEEP_SEC)

    with open('data/rakuten_hotels.json', 'w') as f:
        json.dump(hotels, f)


def fetch_api_response_json(page: int) -> json:
    params = {
        'applicationId': APPLICATION_ID,
        'latitude': TOKYO_STATION_LATITUDE,
        'longitude': TOKYO_STATION_LONGITUDE,
        'searchRadius': SEARCH_RADIUS,
        'page': page
    }
    response = requests.get(API_BASE_URL, params=params)
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    return json.loads(response.text)


if __name__ == '__main__':
    main()
