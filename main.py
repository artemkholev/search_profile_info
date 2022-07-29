import requests
from bs4 import BeautifulSoup
import csv

CSV = 'people.csv'
hoste = 'https://vk.com'
# URL = 'https://vk.com/people/%D0%90%D0%BD%D1%82%D0%BE%D0%BD_%D0%9F%D1%80%D0%BE%D0%BD%D0%B8%D0%BD'
headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36'
}

def get_html(url, PARAMS = ''):
        r = requests.get(url, headers=headers)
        return r

def get_content(html, l):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.findAll('div', class_='people_row search_row clear_fix')
        friends = []
        for i in items:
                friends.append(
                        {
                                'name': i.find('div', class_='labeled name').get_text(strip=True),
                                'id': i.find('div', class_='labeled name').find('a').get('href')[1:],
                                'land': i.find('div', class_='info').get_text(strip=True)[l:],
                                'photo': i.find('div', class_='img').find('img').get('src'),
                                'path': (hoste + i.find('div', class_='labeled name').find('a').get('href'))
                        }
                )
        return friends

def save(items, path):
        with open(path, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['Имя', 'id', 'Место проживания, образование', 'Фото', 'Ссылка'])
                for i in items:
                        writer.writerow( [i['name'], i['id'], i['land'], i['photo'], i['path']])

mn = 0
def parser():
        URL = input('Введите ссылку:')
        html = get_html(URL)
        l = len(BeautifulSoup(html.text, 'html.parser').find('div', class_='ui_search_input_block').find('input').get('value'))
        print('Начинаем обработку.')
        if int(html.status_code) == 200:
                print('Ошибки нет продолжаем дальше, вывод данных.')
                input()
                cards = []
                m = get_content(html.text, l)
                print(m)
                save(m, CSV)
        else:
                print('Ошибка')

parser()
print('End.')
