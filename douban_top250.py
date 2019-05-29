import requests
from requests.exceptions import RequestException
import re
import time
import json
import time


def get_one_page(url):
    try:
        html = requests.get(url)
        if html.status_code == 200:
            return html.text
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<li>.*?<em.*?="">(.*?)</em>.*?src="(.*?)".*?<span.*?title">(.*?)</span>.*?<p.*?<br>(.*?)</p>.*?average">('
        '.*?)</span>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {'index': item[0],
               'image': item[1],
               'title': item[2],
               'time': item[3].strip()[:4],
               'rating': item[4]
               }


def write_to_file(content):
    with open("douban.txt", "a", encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + "\n")


def main(offset):
    url = 'https://movie.douban.com/top250?start=' + str(offset) + '&filter='
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == "__main__":
    for i in range(10):
        main(offset=25 * i)
        time.sleep(1)
