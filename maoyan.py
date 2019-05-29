import requests
from requests.exceptions import RequestException
import re
import json
import time


def get_one_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/72.0.3626.121 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?">(.*?)</i>.*?data-src="(.*?)".*?</a>.*?title="(.*?)".*?star">('
        '.*?)</p>.*?releasetime">(.*?)</p>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {'index': item[0],
               'image': item[1],
               'title': item[2],
               'actor': item[3].strip()[3:],
               'time': item[4].strip()[5:]
               }


def write_to_file(content):
    with open('latest.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://maoyan.com/board/6?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == "__main__":
    for i in range(5):
        main(offset=i * 10)
        time.sleep(1)
