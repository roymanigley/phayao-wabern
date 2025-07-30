from flask import Flask
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)
http_proxy = "http://200.174.198.86:8888"
# https_proxy = "https://103.113.3.240:3128"

proxies = {
    "http": http_proxy,
}


@app.route('/')
def hello_world():
    url = 'https://phayao1.jimdoweb.com/'
    try:
        response = requests.get(
            url,
            proxies=proxies,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
        )
    except Exception as e:
        return str(e)
    if response.status_code != 200:
        print('[!] Unavailable', url)
        return response.text
    soup = BeautifulSoup(response.text, features="html.parser")
    try:
        text = soup.select('#content_area > div > div > h1')[1].text
        if text.find('Angebot von Heute') != -1:
            text = text.split('Angebot von Heute')[1].strip()
        lines = []
        for index, line in enumerate(re.sub(r'\)', ')\n\n', text).split('\n\n')):
            line = re.sub(r'[^a-zA-ZäöüÄÖÜ()]', '_', line)
            line = re.sub(r'_+', ' ', line)
            line = re.sub(r'\(\s+', '(', line)
            line = re.sub(r'\s\)+', ')', line)
            if line.find('Frühlingsrollen') != -1:
                lines.append('    Frühlingsrollen')
                break
            lines.append('[' + str(index + 1) + ']' + line.strip())

        return '<br>\n'.join(lines)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
