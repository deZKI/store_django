import json
import random

import requests
from django.core.files import File
from django.http import HttpResponse, HttpResponseNotAllowed
from django.db import IntegrityError

from games.models import Game, GameGenre, Tag, GameImage

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


def parsing(request_dj, page):
    if request_dj.user.is_superuser:
        response = requests.get(
            f'https://ag.ru/api/games/lists/popular?discover=true&&page_size=10page={page}&key=1287fbd232d14b00b7af6b11868f9c6b',
            cookies=cookies,
            headers=headers,
        ).content.decode('UTF-8')
        games = json.loads(response)
        games = games['results']
        count = 0
        for game in games:
            try:
                image = requests.get(game['background_image'])
                img = open('media/1.jpg', 'wb')
                img.write(image.content)
                obj = Game.objects.get_or_create(
                    name=game['name'],
                    slug=game['slug'],
                    main_image=File(open('media/1.jpg', 'rb')),
                    price=random.randint(1000, 2000),
                    release_date=game['released'],
                    developer_id=2,
                    publisher_id=2,
                    ready=False,
                    description='Здесь могла быть ваша реклама',

                )
                img.close()
                for genre in game['genres']:
                    genre_temp = GameGenre.objects.get_or_create(name=genre['name'], slug=genre['slug'])
                    obj[0].genres.add(genre_temp[0])
                for tag in game['tags']:
                    tag_temp = Tag.objects.get_or_create(name=tag['name'], slug=tag['slug'])
                    obj[0].tags.add(tag_temp[0])

                for photo in game['short_screenshots'][1:]:
                    image = requests.get(photo['image'])
                    img = open('media/1.jpg', 'wb')
                    img.write(image.content)
                    GameImage.objects.create(game=obj[0], image=File(open('media/1.jpg', 'rb')))
                    img.close()
            except IntegrityError:
                continue
            count += 1
        return HttpResponse(f'скачалось вот столько {count}\n. А ваша Тильда так может?')
    return HttpResponseNotAllowed('Отказано')
