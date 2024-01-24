import json
from bs4 import BeautifulSoup
import requests


url = 'https://omsk.yapdomik.ru/about'


# список для хранения данных
list_data = []


# получаем html и записываем в файл
def get_html_write_file_web_2():
    html = requests.get(url=url).text
    with open('index.html', 'w') as file:
        file.write(html)


# получаем ссылки по которым будем собирать данные
def get_link_web_2():
    try:
        with open('index.html', 'r') as file:
            src = file.read()
        sou_p = BeautifulSoup(src, 'html.parser')
        all_link = sou_p.find(class_='city-select').find_all(class_="city-select__item")
        link_dict = {'Омск': 'https://omsk.yapdomik.ru'}
        for item in all_link:
            city = item.text.strip()
            link = item.get('href')
            link_dict[city] = link
        return link_dict
    except FileNotFoundError:
        print("Not file")


def get_data_web_2():
    for i in get_link_web_2():
        src = requests.get(url=get_link_web_2()[i]).text
        soup = BeautifulSoup(src, 'html.parser')
        name = soup.find(class_='site-footer__description').find('h2').text.split('-')[1].strip(' ''"')
        city = soup.find('div', class_='site-footer__address-list').find_all('h2')[1].text.split()[1].replace(':', ',')
        addresses = soup.find('div', class_='site-footer__address-list').find_all('li')
        phone = soup.find('div', class_='contacts__phone').find('a').text
        for address in addresses:
            data_dict = {'name': name,
                         'address': city + address.text,
                         'latlon': [],
                         'phones': [phone],
                         'working_hours': []
                          }
            list_data.append(data_dict)
    return list_data


def write_json_web_2(data):
    with open('data_website_2.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)






















