import json
import random
from datetime import datetime
from django.http import HttpResponse
from django.core.files import File
import requests

from games.models import Game

cookies = {
    'SL_G_WPT_TO': 'ru',
    'SL_GWPT_Show_Hide_tmp': '1',
    'SL_wptGlobTipTmp': '1',
    'referer': 'https://www.google.com/',
    'dg': 'q06dz0i88fqjif5sf78sivzkfr76f0r5',
    'csrftoken': 'SejMivv2qLx9ZvCiUYneGJ3VYjzbp5D3wndJ7XeX3CSWum7mOsLed3Maoq3EnUcf',
}

headers = {
    'authority': 'ag.ru',
    'accept': 'application/json',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    # 'cookie': 'SL_G_WPT_TO=ru; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; referer=https://www.google.com/; dg=q06dz0i88fqjif5sf78sivzkfr76f0r5; csrftoken=SejMivv2qLx9ZvCiUYneGJ3VYjzbp5D3wndJ7XeX3CSWum7mOsLed3Maoq3EnUcf',
    'referer': 'https://ag.ru/discover/all-time-top?page=5',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
    'x-api-client': 'website',
    'x-api-language': 'ru',
    'x-api-referer': '%2Fdiscover%2Fall-time-top',
    'x-csrftoken': 'SejMivv2qLx9ZvCiUYneGJ3VYjzbp5D3wndJ7XeX3CSWum7mOsLed3Maoq3EnUcf',
}


def parsing(request):
    response = requests.get(
        'https://ag.ru/api/games/lists/popular?discover=true&&page_size=100&page=2&key=1287fbd232d14b00b7af6b11868f9c6b',
        cookies=cookies,
        headers=headers,
    ).content.decode('UTF-8')
    games = json.loads(response)
    print(type(games))
    games = games['results']
    for game in games:
        if not Game.objects.filter(name=game['name']).exists():
            image = requests.get(game['background_image'])
            img = open('1.jpg', 'wb')
            img.write(image.content)
            Game.objects.create(
                name=game['name'],
                slug=game['slug'],
                main_image=File(open('1.jpg', 'rb')),
                price=random.randint(1000, 2000),
                release_date=datetime.strptime("01/01/2001", "%d/%m/%Y"),
                developer_id=5,
                publisher_id=5,
                ready=False,
            )
            img.close()
    return HttpResponse('скачалось')
