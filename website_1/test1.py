import itertools
import json
from time import sleep

from bs4 import BeautifulSoup
import requests




# списки из ссылок, по которым будем забирать данные
lst_link = [
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=344706&source=posts',
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=344662&source=posts',
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=343685&source=posts',
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=343665&source=posts',
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=343533&source=posts',
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=1359&source=posts',
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=1355&source=posts',
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=1353&source=posts',
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=1352&source=posts',
    'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id=1333&source=posts'
]

lst_1321_1331 = [
    f'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id={1321 + i}&source=posts'
    for i in range(11)]

lst_1337_1350 = [
    f'https://dentalia.com/wp-json/jet-engine/v2/get-map-marker-info/?listing_id=6640&post_id={1337 + i}&source=posts'
    for i in range(14)]

# объединяем списки в один список
urls = list(itertools.chain(lst_link, lst_1337_1350, lst_1321_1331))

# список для записи в него словаря с данными
lst_data = []


# функция получает код html и записывает в файл
def get_html_write_file_web_1(url_s):
    for i, url in enumerate(url_s):
        get_html = requests.get(url=url)
        json_data = json.loads(get_html.text)
        html_response = json_data['html']
        # записываем полученный код в файл, для дальнейшей работы, чтобы не бомбить запросами сайт
        with open(f'index_web_{i + 1}.html', 'w') as file:
            file.write(html_response)

    print('файлы html записаны')


# функция читает файлы, берет данные
def read_file_get_data_web_1():
    for i in range(len(urls)):
        try:
            with open(f'index_web_{i + 1}.html') as file:
                src = file.read()
            soup = BeautifulSoup(src, 'html.parser')
            name = soup.find('h3').text
            address = soup.find('div', class_="jet-listing-dynamic-field__content").text.strip('\n').replace('\n',
                                                                                                             '').replace(
                '  ', '')
            phones = soup.find_all('div', class_="jet-listing-dynamic-field__content")[2].text.replace('\n', '').replace(
                '  ',
                '')
            work_time = soup.find_all('div', class_="jet-listing-dynamic-field__content")[1].text.replace('\n', '').replace(
                '  ', '')
            # формируем словарь с данными
            dict_data = {
                'name': name,
                'address': address,
                'latlon': [],
                'phones': [phones],
                'working_hours': [work_time]
                }
            lst_data.append(dict_data)

        except FileNotFoundError:
            print("Not file")
    return lst_data


# запись данных в json формат
def write_json_web_1(data):
    with open('data_website_1.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


