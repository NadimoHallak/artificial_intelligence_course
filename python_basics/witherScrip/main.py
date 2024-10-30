import json
from bs4 import BeautifulSoup
from datetime import date
from tabulate import tabulate
import requests
import re


def getForcastData():
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "cookie": "celsius=1"
    }
    url = "https://world-weather.info/"

    response = requests.get(url=url, headers=header)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        resorts = soup.findAll('div', id='resorts')
        reCiteis = r'">([\w\s]+)<\/a><span>'
        cities = re.findall(reCiteis, str(resorts))

        reTemp = r'<span>(\+\d+|-\d+|0)<span'
        temps = re.findall(reTemp, str(resorts))
        temps = [int(temp) for temp in temps]
        conditionTags = soup.findAll('span', class_='tooltip')
        conditions = [condition.get('title') for condition in conditionTags]
        data = zip(cities, temps, conditions)
        # 
        #? How to print zip 
        #Todo:  print(list(data))
        # 
        return data

    return False


def get_forcast_today():
    data = getForcastData()
    if data:
        today = date.today().strftime('%d/%m/%Y')
        with open('output.txt', 'w') as file:
            file.write("Popular Cities Forcast\n")
            file.write(today + '\n')
            file.write("=" * 23 + '\n')
            table = tabulate(
                data, headers=['cities', 'temp', 'condition'], tablefmt='fancy_grid')
            file.write(table)


def get_forcast_today_json():
    data = data = getForcastData()
    if data:
        today = date.today().strftime('%d/%m/%Y')
        cities = [{'city': city, 'temp': temp, 'condition': condition}
                  for city, temp, condition in data]
        data_json = {'title': 'Popular Cities Forcast',
                     'date': today, 'cities': cities}
        with open('output.json', 'w') as f:
            json.dump(data_json, f, ensure_ascii=False)




if __name__ == '__main__':
    get_forcast_today()
    get_forcast_today_json()

#  File "C:\Users\L\Desktop\python_project\witherScrip\venv\Lib\site-packages\bs4\element.py", line 2571, in __getattr__
#     raise AttributeError(
# AttributeError: ResultSet object has no attribute "find_all". You're probably treating a list of elements like a single element. Did you call find_all() when you meant to call find()?
