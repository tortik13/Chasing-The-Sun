import os
import sys
import pygame


WIDTH = 700
HEIGHT = 700


def load_screen_im(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Alto')
        self.fps = 200
        self.clock = pygame.time.Clock()
        self.start_game()

    def game(self):
        dog_surf = load_screen_im('pause.png')
        dog_rect = dog_surf.get_rect(bottomright=(60, 690))
        picture = Picture()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    if (x in range(10, 60)) and (y in range(640, 690)):
                        print('Пауза')

            self.screen.fill(pygame.Color('blue'))
            self.screen.blit(picture.image, picture.rect)
            self.screen.blit(picture.image2, picture.rect2)
            picture.update()
            self.screen.blit(dog_surf, dog_rect)
            pygame.display.flip()
            self.clock.tick(self.fps)

    def start_game(self):
        intro_text = ["ЗАСТАВКА", "",
                      "Правила игры",
                      "Начало игры",
                      "Достижения"]

        fon = pygame.transform.scale(load_screen_im('fon.jpg'), (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)

        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    if (x in range(10, 120)) and (y in range(60, 75)):
                        print('Заставка')
                    if (x in range(10, 147)) and (y in range(120, 135)):
                        print('Правила')
                    if (x in range(10, 150)) and (y in range(150, 165)):
                        self.game()
                    if (x in range(10, 180)) and (y in range(180, 195)):
                        print('Достижения')

            pygame.display.flip()
            self.clock.tick(self.fps)

    def finish_game(self):
        pass


class Picture():
    def __init__(self):

        self.image = pygame.image.load('data/test.png')
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 400

        self.image2 = pygame.image.load('data/test3.png')
        self.rect2 = self.image2.get_rect()
        self.rect2.left = 700
        self.rect2.top = 400

        self.first_im = True
        self.second_im = False

    def update(self):
        if self.first_im:
            self.rect = self.rect.move(-1, 0)
        if self.second_im:
            self.rect2 = self.rect2.move(-1, 0)

        if self.rect.left == -300 and self.first_im:
            self.second_im = True
            self.rect2.left = 700
            self.rect2.top = 400
        if self.rect.left == -1000 and self.first_im:
            self.first_im = False
        if self.rect2.left == -300 and self.second_im:
            self.rect.left = 700
            self.rect.top = 400
            self.first_im = True
        if self.rect2.left == -1000 and self.second_im:
            self.second_im = False





class Player:
    def __init__(self):
        pass


class Music:
    def __init__(self):
        pass


class Camera:
    def __init__(self):
        pass


if __name__ == '__main__':
    app = App()
