from support import *

if __name__ == '__main__':
    toponym_to_find = " ".join(sys.argv[1:])
    toponym = get_response(toponym_to_find)
    spn_toponym = get_spn(toponym['boundedBy']['Envelope']['lowerCorner'],
                          toponym['boundedBy']['Envelope']['upperCorner'])
    ll_toponym = ','.join(toponym['Point']['pos'].split())

    organization = get_response_organization(ll_toponym, spn_toponym, 'аптека')[0]
    point = organization["geometry"]["coordinates"]
    org_point = f"{point[0]},{point[1]}"

    points = [list(map(float, ll_toponym.split(","))), list(map(float, org_point.split(",")))]
    spn = get_spn(' '.join([str(max(x, y)) for x, y in zip(points[0], points[1])]),
                  ' '.join([str(min(x, y)) for x, y in zip(points[0], points[1])]))
    ll = ','.join(
        [str(float(x) - ((float(x) - float(y)) / 2)) for x, y in zip(ll_toponym.split(','), org_point.split(','))])

    print(f'Адрес: {organization["properties"]["CompanyMetaData"]["address"]}\n'
          f'Названия аптеки: {organization["properties"]["CompanyMetaData"]["name"]}\n'
          f'Время работы: {organization["properties"]["CompanyMetaData"]["Hours"]["text"]}\n'
          f'Расстояние до аптеки: {int(lonlat_distance(*points))} метров')

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(get_response_map(ll, spn, (ll_toponym, 'vkbkm'), (org_point, 'pm2al')))
    draw_map(map_file)
