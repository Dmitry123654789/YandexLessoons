from support import *

if __name__ == '__main__':
    toponym_to_find = " ".join(sys.argv[1:])
    result = 10
    toponym = get_response(toponym_to_find)
    spn_toponym = get_spn(toponym['boundedBy']['Envelope']['lowerCorner'],
                          toponym['boundedBy']['Envelope']['upperCorner'])
    ll_toponym = ','.join(toponym['Point']['pos'].split())

    point_in_map = []
    points_x = [float(ll_toponym.split(",")[0])]
    points_y = [float(ll_toponym.split(",")[1])]
    points= []

    organizations = get_response_organization(ll_toponym, spn_toponym, str(result), 'аптека')
    for i in range(result):
        point = organizations[i - 1]["geometry"]["coordinates"]
        org_point = f"{point[0]},{point[1]}"
        points_x.append(point[0])
        points_y.append(point[1])
        time = organizations[i-1]['properties']['CompanyMetaData']['Hours']['text'].split()[1]
        if not time:
            points.append((org_point, 'pm2grl'))
        elif 'круглосуточн' in time:
            points.append((org_point, 'pm2gnl'))
        else:
            points.append((org_point, 'pm2bll'))


    spn = get_spn(f'{min(points_x)} {min(points_y)}', f'{max(points_x)} {max(points_y)}')
    ll = ','.join([str(min(points_x) - ((min(points_x) - max(points_x)) / 2)),
                   str(min(points_y) - ((min(points_y) - max(points_y)) / 2))])


    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(get_response_map(ll, spn, (ll_toponym, 'pm2al'), *points))
    draw_map(map_file)
