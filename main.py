from support import *

if __name__ == '__main__':
    toponym_to_find = " ".join(sys.argv[1:])
    ll, spn = get_ll_spn(get_response(toponym_to_find))

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(get_response_map(ll, spn, (ll, 'vkbkm')))
    draw_map(map_file)
