import math
import sys

import requests


def get_response(adress):
    server_address = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "format": "json",
        "geocode": adress}
    response = requests.get(server_address, params=geocoder_params)
    if not response:
        print(f"Ошибка выполнения запроса: {response.url}")
        sys.exit(1)
    return response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']


def get_spn(lowerCorner, upperCorner):
    left, button = lowerCorner.split()
    right, top = upperCorner.split()
    dx = abs(float(right) - float(left))
    dy = abs(float(top) - float(button))
    return f'{dx},{dy}'


def get_response_map(ll, spn, *pt):
    """pt = (style, coord)"""
    server_address = "https://static-maps.yandex.ru/v1"
    apikey = '0eea7a3e-806e-4b45-8976-3c543752e89c'
    map_params = {
        'll': ll,
        'spn': spn,
        # 'style': 'tags.any:water;road;transit_location;poi;admin|elements:label|stylers.opacity:0',
        'style': 'tags.any:transit_location;admin;park;sports_ground;national_park;major_landmark;medical|elements:label|stylers.opacity:0',
        'apikey': apikey
        # 'pt': '~'.join([','.join(x) for x in pt]),
    }
    response = requests.get(server_address, params=map_params)
    if not response:
        print(f"Ошибка выполнения запроса: {response.url}")
        sys.exit(1)
    return response.content


# Определяем функцию, считающую расстояние между двумя точками, заданными координатами
def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance
