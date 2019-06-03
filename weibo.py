from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq


base_url = 'https://m.weibo.cn/api/container/getIndex?'
client = MongoClient()
db = client['weibo']
collection = db['weibo']

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 '
                  'Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(weibo_page):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': weibo_page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(weibo_json):
    if weibo_json:
        items = weibo_json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = dict(id=item.get('id'), attitudes=item.get('attitudes_count'), comments=item.get('comments_count'),
                         reposts=item.get('reposts_count'), text=pq(item.get('text')).text())
            yield weibo


if __name__ == '__main__':
    for page in range(1, 11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)