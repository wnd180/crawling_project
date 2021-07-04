import csv
import time
import os.path
import threading

import requests as req
from bs4 import BeautifulSoup

file_dir = os.path.dirname(os.path.realpath(__file__))
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        div {{
            width: 50%;
            padding-bottom: 1%;
        }}
        a {{
            text-decoration: none;
            font-weight: bold;
            font-size: 1.2rem;
            color: black;
        }}
        table {{
            width: 100%;
            border: 1px solid black;
            border-collapse: collapse;
        }}
        th, td {{
            text-align: center;
            border: 1px solid gray;
        }}
        .stock {{
            background-color: black;
        }}
    </style>
</head>
<body>
    <div>
        <a href="{}">{}</a>
    </div>
    <div>
        <table>
            <thead>
                <th>시각</th>
                <th>00</th>
                <th>05</th>
                <th>10</th>
                <th>15</th>
                <th>20</th>
                <th>25</th>
                <th>30</th>
                <th>35</th>
                <th>40</th>
                <th>45</th>
                <th>50</th>
                <th>55</th>
            </thead>
            <tbody>
                {}
            </tbody>
        </table>
    </div>
    <div>
        <button type="button" onclick="openCSV()">csv 파일 열기</button>
    </div>
    <script>
        function openCSV() {{
            let fname = window.location.pathname.replace("html", "csv");
            location.href = "ms-excel:ofv|u|file://" + fname;
        }}
    </script>
</body>
</html>
'''
HTML_TEMPLATE2 = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        .grid_container {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(auto, 20rem));
            grid-auto-rows: minmax(auto, 20rem);
            row-gap: 7rem;
            column-gap: 15px;
            justify-items: center;
            justify-content: space-around;
            padding-top: 1.7em;
            padding-left: 10%;
            padding-right: 10%;
        }}
        .grid_item img {{
            width: 20rem;
            height: 20rem;
        }}
        .grid_item a {{
            display: block;
            text-decoration: none;
            color: black;
        }}
    </style>
</head>
<body>
    <div class="grid_container">
        {}
    </div>
</body>
</html>
'''


class Worker:
    def __init__(self, url):
        self.url = url
        self.num = url.split('/')[-1]
        self.name = None
        self.stack = None
        self.image = None

    def load_stock(self):
        _header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        }

        res = req.get(self.url, headers=_header)
        if res.status_code != 200:
            print(f'[{self.num}] HTTP Error: {res.status_code}')

        parser = BeautifulSoup(res.text, "html.parser")
        self.name = parser.find('meta', {'property': 'og:title'}).get('content').strip()
        self.stack = bool('out' not in parser.find('meta', {'property': 'og:availability'}).get('content').strip())
        self.image = parser.find('meta', {'property': 'og:images'}).get('content').strip().replace('/b/', '/l/')

    def write_csv(self):
        init = bool(not os.path.isfile(f'{file_dir}/data/{self.num}.csv'))

        with open(f'{file_dir}/data/{self.num}.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)

            if init:
                writer.writerow(['날짜', '시각', '재고'])

            writer.writerow([time.strftime('%m/%d'), time.strftime('%H:%M'), 'O' if self.stack else 'X'])

    def make_html(self):
        with open(f'{file_dir}/data/{self.num}.csv', 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            result = []
            temp = {}
            c_time = None
            b_time = None

            for row in reader:
                times = row['시각'].split(':')
                c_time = f"{row['날짜']} {times[0]}시"
                if b_time is not None and c_time != b_time:
                    result.append([b_time, temp])
                    temp = {}

                temp[times[1]] = row['재고']

                b_time = c_time

            result.append([b_time, temp])

            table = ''
            for e in result:
                text = f'<tr><td style="font-weight: bold;">{e[0]}</td>'

                for i in range(0, 60, 5):
                    data = e[1].get(f'{i:02}')

                    if data is None:
                        text += '<td class="stock"></td>'
                    elif data == 'O':
                        text += '<td class="stock" style="background-color: #377EB8">O</td>'
                    else:
                        text += '<td class="stock" style="background-color: #B8374A">X</td>'

                text += '<tr>\n'

                table += text

        with open(f'{file_dir}/data/{self.num}.html', 'w', encoding='utf-8') as file:
            file.write(HTML_TEMPLATE.format(self.url, self.name, table))

    def main(self):
        self.load_stock()
        self.write_csv()
        self.make_html()


if __name__ == '__main__':
    try:
        os.mkdir(f'{file_dir}/data')
    except FileExistsError:
        pass

    with open(f'{file_dir}/list.txt', 'r', encoding='utf-8') as file:
        products = [l.strip() for l in file.readlines()]

    workers = []
    for url in products:
        worker = Worker(url)
        workers.append(worker)
        th = threading.Thread(target=worker.main)
        th.start()

    while threading.active_count() > 1:
        time.sleep(0.05)

    with open(f'{file_dir}/products.html', 'w', encoding='utf-8') as file:
        grid = ''
        for worker in workers:
            grid += f'<div class="grid_item"><a href="data/{worker.num}.html"><img src="{worker.image}"><div>{worker.name}</div></a></div>\n'

        file.write(HTML_TEMPLATE2.format(grid))
