from random import choice

from support import *

CITY = ["Краснодар", "Казань", "Нижний Новгород", "Великий Новгород", "Анадырь", "Хабаровск", "Махачкала"]


def save_image(city):
    toponym_to_find = city
    toponym = get_response(toponym_to_find)
    spn_toponym = ','.join(map(lambda x: str(float(x) / 10),
                               get_spn(toponym['boundedBy']['Envelope']['lowerCorner'],
                                       toponym['boundedBy']['Envelope']['upperCorner']).split(',')))
    ll_toponym = ','.join(map(lambda x: str(float(x) - 0.005), toponym['Point']['pos'].split()))

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(get_response_map(ll_toponym, spn_toponym))


def draw_pygame_map(map_file):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                city = choice(CITY)
                save_image(city)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    save_image(choice(CITY))
    draw_pygame_map("map.png")
