import os
import sys

import pygame
import requests


def get_response(adress):
    server_address = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "format": "json",
        "geocode": adress}
    response = requests.get(server_address, params=geocoder_params)
    if not response:
        print("Ошибка выполнения запроса")
        sys.exit(1)
    return response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']


def get_ll_spn(toponym):
    ll = ','.join(toponym['Point']['pos'].split())
    envelope = toponym['boundedBy']['Envelope']
    left, button = envelope['lowerCorner'].split()
    right, top = envelope['upperCorner'].split()
    dx = abs(float(right) - float(left)) / 2
    dy = abs(float(top) - float(button)) / 2
    return ll, f'{dx},{dy}'


def get_response_map(ll, spn, *pt):
    """pt = (style, coord)"""
    server_address = "https://static-maps.yandex.ru/v1"
    apikey = '0eea7a3e-806e-4b45-8976-3c543752e89c'
    map_params = {
        'll': ll,
        'spn': spn,
        'apikey': apikey,
        'pt': '~'.join([','.join(x) for x in pt]),
    }
    response = requests.get(server_address, params=map_params)
    if not response:
        print("Ошибка выполнения запроса")
        sys.exit(1)
    return response.content


def draw_map(map_file):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    # Удаляем за собой файл с изображением.
    os.remove(map_file)
