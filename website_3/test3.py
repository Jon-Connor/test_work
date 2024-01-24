import json
from bs4 import BeautifulSoup
import requests

url = "https://www.santaelena.com.co/"

list_data = []


# получаем html и сохраняем в файл
def get_html_write_file_web_3():
    html = requests.get(url=url).text
    with open('index.html', 'w') as file:
        file.write(html)


# получаем ссылки для сбора данных
def get_link_web_3():
    try:
        with open('index.html', 'r') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'html.parser')
        all_link = soup.find_all('ul', class_='elementor-nav-menu--dropdown')[-1].find_all('a')
        link_dict = {}
        for item in all_link:
            key = item.text.split()[2]
            value = item.get('href')
            link_dict[key] = value

        return link_dict

    except Exception:
        print("not file")


# получаем html и записываем в файл для дальнейшего сбора данных
def get_html_web_3():
    count = 1
    for key, link in get_link_web_3().items():
        rec = requests.get(url=link).text
        with open(f'index{count}.html', 'w') as file:
            file.write(rec)
        count += 1


def get_data_web_3():
    count = 1

    try:
        for city, link in get_link_web_3().items():

            with open(f'index{count}.html', 'r') as file:
                src = file.read()
            soup = BeautifulSoup(src, 'html.parser')
            names = soup.find_all('h3', class_="elementor-heading-title")
            if city == 'Medellín':
                data = soup.find_all('div', class_="elementor-text-editor elementor-clearfix")[4:-1]
                addresses = [item.find('p').text.split(':')[1].lstrip() for item in data]
                phones = [item.find('p').find_next('p').text for item in data]
                phone = [i.split(':')[1].lstrip() if i != 'Local 005' else '316 017 5000 ext 4902' for i in phones]
                work_time_1 = [item.find('p').find_next('p').find_next('p').find_next('p').text for item in data]
                work_time_2 = [item.find('p').find_next('p').find_next('p').find_next('p').find_next('p').text for item in data]
                work_time = [[work_time_1[i], work_time_2[i]] for i in range(len(work_time_1))]
                get_dict(names, city, addresses, phone, work_time)

            if city == 'Bogotá':
                data = soup.find_all('div', class_="elementor-text-editor elementor-clearfix")[3:]
                addresses = [item.find('p').text.split(':')[1].replace('  ', '').replace('\n', ' ').replace('#', '') for
                             item in data]
                phone = ['Not phone'] * len(names)
                work_time_1 = [item.find('p').find_next('p').find_next('p').find_next('p').text.replace('  ', '').replace(
                    '\xa0', ' 8:00') for item in data][0:6]
                work_time_2 = [item.find('p').find_next('p').find_next('p').text for item in data][0:6]
                work_time = [[work_time_1[i], work_time_2[i]] for i in range(len(work_time_1))] + [['Horario de atención:']] * 5
                get_dict(names, city, addresses, phone, work_time)

            if city == 'Montería':
                data = soup.find_all('div', class_="elementor-text-editor elementor-clearfix")[3:]
                addresses = [item.find('p').text.replace('\xa0', ' ') for item in data]
                phone = [item.find('p').find_next('p').text for item in data]
                work_time = [item.find('p').find_next('p').find_next('p').text.replace('\xa0', '') for item in data]
                get_dict(names, city, addresses, phone, work_time)

            if city == 'Pereira':
                data = soup.find_all('div', class_="elementor-text-editor elementor-clearfix")[3:]
                addresses = [item.find_all('h4') for item in data][0][1].text
                phone = [[item.find('p').text.split(':') for item in data][0][1]]
                work_time = [item.find('p').find_next('p').text for item in data]
                get_dict(names, city, addresses, phone, work_time)


            if city == 'Barranquilla':
                data = soup.find_all('div', class_="elementor-text-editor elementor-clearfix")[3:]
                addresses = [item.find('p') for item in data][0].text
                phone = [[item.find('p').find_next('p').text.split(':') for item in data][0][1].strip()]
                work_time_1 = [item.find('p').find_next('p').find_next('p').text for item in data][0]
                work_time_2 = [item.find('p').find_next('p').find_next('p').find_next('p') for item in data][0].text
                work_time = [work_time_1, work_time_2]
                get_dict(names, city, addresses, phone, work_time)

            count += 1
        return list_data
    except Exception:
        print('Not file')


def get_dict(names, city, address, phone, work_time):
    for i, name in enumerate(names):
        dict_data = {
            'name': name.text.strip().replace("  ", '').replace("\n", ' '),
            'address': city + ', ' + address[i],
            'latlon': [],
            'phones': [phone[i]],
            'working_hours': work_time[i]
        }
        list_data.append(dict_data)


# запись данных в json формат
def write_json_web_3(data):
    with open('data_website_1.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

x = get_data_web_3()
print(x)