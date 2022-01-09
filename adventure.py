import os
import sqlite3
import sys
import pygame
import random


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


def music_play(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Звуковой файл '{fullname}' не найден")
        sys.exit()
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.play(-1)


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('DESERT Adventure')
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.prizes = pygame.sprite.Group()
        self.bird = AnimatedSprite(self, load_screen_im("birds5.png"), 8, 3, 700, 260)
        self.fps = 200.0
        self.clock = pygame.time.Clock()
        self.length = 0
        self.score = 0
        self.money = 0
        self.speed = 1
        self.mus = music_play('music.mp3')

    def terminate(self):
        pygame.quit()
        sys.exit()

    def game(self):
        dog_surf = load_screen_im('pause.png')
        dog_rect = dog_surf.get_rect(bottomright=(60, 690))
        picture = Picture()
        weather = Weather()
        gift = Gift(self)
        player = Player(self)
        pause = False
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    if (x in range(10, 60)) and (y in range(640, 690)):
                        print('Пауза')
                        if not pause:
                            pause = True
                            dog_surf = load_screen_im('play.png', -1)
                            rect = pygame.Rect(0, 60, 700, 640)
                            sub = self.screen.subsurface(rect)
                            pygame.image.save(sub, 'data/screenshot.jpg')
                            pause_screen = load_screen_im('screenshot.jpg')
                            pause_rect = pause_screen.get_rect(topleft=(0, 60))
                            self.screen.blit(pause_screen, pause_rect)
                            pygame.mixer.music.pause()

                        else:
                            pause = False
                            dog_surf = load_screen_im('pause.png', -1)
                            pygame.mixer.music.unpause()

            self.screen.fill('#99CCFF')
            self.all_sprites.draw(self.screen)
            self.player_group.draw(self.screen)
            self.prizes.draw(self.screen)

            if not pause:
                self.length += 0.06

                if int(self.length) % 20 == 0 and int(self.length) > 0:
                    self.speed += 0.005

                self.fps += 0.5

                self.all_sprites.update()
                self.player_group.update(picture)
                gift.update(player, picture)

                font = pygame.font.Font(None, 50)
                length = font.render(str(int(self.length)) + 'м', True, pygame.Color('white'))
                intro_rect = length.get_rect()
                intro_rect.top = 10
                intro_rect.x = 675 - 24 * len(str(int(self.length)))
                self.screen.blit(length, intro_rect)

            else:
                font = pygame.font.Font(None, 120)

                length = font.render(str(int(self.length)) + 'м', True, pygame.Color('white'))
                intro_rect = length.get_rect()
                intro_rect.top = 250
                intro_rect.x = (700 - 60 * len(str(int(self.length)))) // 2
                self.screen.blit(length, intro_rect)

            font = pygame.font.Font(None, 50)
            score = font.render(str(int(self.score)), True, pygame.Color('white'))
            intro_rect = score.get_rect()
            intro_rect.top = 50
            intro_rect.x = 700 - 28 * len(str(int(self.score)))
            self.screen.blit(score, intro_rect)

            money = font.render(str(int(self.money)), True, pygame.Color('white'))
            intro_rect = money.get_rect()
            intro_rect.top = 10
            intro_rect.x = 15
            self.screen.blit(money, intro_rect)

            self.screen.blit(picture.image, picture.rect)
            self.screen.blit(picture.image2, picture.rect2)

            if weather.clouds:
                self.screen.blit(weather.clouds_1, weather.rect)
                self.screen.blit(weather.clouds_2, weather.rect2)
                self.screen.blit(weather.clouds_3, weather.rect3)
            if weather.sun:
                self.screen.blit(weather.sun_1, weather.rect4)

            if int(self.length) % 119 == 0 and int(self.length) > 0:
                new_weather = random.choice(['clouds', 'sun'])

            if int(self.length) % 120 == 0 and int(self.length) > 2:
                self.bird.new_bird()
                weather.change_weather(new_weather)

            if int(self.length) % 100 == 0 and int(self.length) > 0:
                gift.new_gift()

            if gift.prize == 'ускорение':
                self.speed += 2

            if gift.prize == 'замедление':
                if self.speed > 3:
                    self.speed -= 2
                elif 2 < self.speed <= 3:
                    self.speed -= 1
                else:
                    self.speed -= 0.01

            if gift.prize == 'щит':
                print('Пока не реализовано')

            if gift.prize == 'очки':
                self.score += random.randrange(15, 201, 5)

            if gift.prize == 'монеты':
                self.money += random.randrange(10, 101, 10)

            picture.update(pause, self.speed)
            weather.update(pause)
            self.screen.blit(dog_surf, dog_rect)
            pygame.display.flip()
            self.clock.tick(int(self.fps))

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
                    self.terminate()
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game()

            pygame.display.flip()
            self.clock.tick(int(self.fps))

    def update_records(self):
        con = sqlite3.connect('info.sqlite')
        cur = con.cursor()
        length = cur.execute(f"""SELECT num from records
                                    WHERE type = 'length'""").fetchall()
        score = cur.execute(f"""SELECT num from records
                                    WHERE type = 'score'""").fetchall()
        con.close()

        if self.length > length[0]:
            con = sqlite3.connect('info.sqlite')
            cur = con.cursor()
            data = ('length', int(self.length))
            query = 'INSERT INTO records VALUES (?, ?)'
            cur.execute(query, data)
            con.commit()
            con.close()
        if self.score > score[0]:
            con = sqlite3.connect('info.sqlite')
            cur = con.cursor()
            data = ('score', int(self.score))
            query = 'INSERT INTO records VALUES (?, ?)'
            cur.execute(query, data)
            con.commit()
            con.close()

    def finish_game(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, app):
        super().__init__(app.player_group)
        self.image = load_screen_im("doll.png", -1)
        app.screen.fill('#99CCFF')
        picture = Picture()
        self.pic_rect = picture.mask.outline(every=1)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 100
        self.rect.y = 250

    def update(self, picture):
        y_now = []
        y_later = []
        for coord in self.pic_rect:
            if coord[0] == 205:
                y_now.append(coord[1])
            if coord[0] == 206:
                y_later.append(coord[1])

        distance = abs(max(y_later) - max(y_now))
        # вместо +-1 нужно будет подставить +-distance, но пока что не знаю, как

        if not pygame.sprite.collide_mask(self, picture):
            if max(y_now) < (self.rect.top - 150):
                self.rect = self.rect.move(0, -2)
            elif max(y_now) >= (self.rect.top - 150):
                self.rect = self.rect.move(0, 1)
        else:
            self.rect = self.rect.move(0, -1)


class Picture:
    def __init__(self):
        self.image = pygame.image.load('data/map1_v1.png')
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 300
        self.mask = pygame.mask.from_surface(self.image)

        self.image2 = pygame.image.load('data/map2_v1.png')
        self.rect2 = self.image2.get_rect()
        self.rect2.left = 700
        self.rect2.top = 300
        # self.mask2 = pygame.mask.from_surface(self.image2)

        self.first_im = True
        self.second_im = False
        self.pause = False

    def update(self, pause, speed):
        if not pause:
            if self.first_im:
                self.rect = self.rect.move(-1 * int(speed), 0)
            if self.second_im:
                self.rect2 = self.rect2.move(-1 * int(speed), 0)

            if self.rect.left == -300 and self.first_im:
                self.second_im = True
                self.rect2.left = 700
                self.rect2.top = 300
            if self.rect.left == -1000 and self.first_im:
                self.first_im = False
            if self.rect2.left == -300 and self.second_im:
                self.rect.left = 700
                self.rect.top = 300
                self.first_im = True
            if self.rect2.left == -1000 and self.second_im:
                self.second_im = False


class Gift(pygame.sprite.Sprite):
    def __init__(self, app):
        super().__init__(app.prizes)
        self.image = load_screen_im("prize.png", -1)
        self.rect = self.image.get_rect()
        self.rect.x = -200
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.prizes = ['ускорение', 'замедление', 'очки', 'монеты', 'щит']
        self.prize = ''

    def new_gift(self):
        self.rect.x = 700
        self.rect.y = 0

    def update(self, player, picture):
        if pygame.sprite.collide_mask(self, player):
            self.prize = random.choice(self.prizes)
            self.rect.x = -200
            self.rect.y = 0
            print(self.prize)
        elif pygame.sprite.collide_mask(self, picture):
            self.prize = ''
            self.rect = self.rect.move(-1, 0)
        else:
            self.prize = ''
            self.rect = self.rect.move(-3, 5)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, app, sheet, columns, rows, x, y):
        super().__init__(app.all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 0
        self.counter_of_fly = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.counter += 1
        self.counter_of_fly += 1
        if self.counter == 8:
            self.counter = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.counter_of_fly % 2 == 0:
            self.rect = self.rect.move(-3, 0)

    def new_bird(self):
        self.rect.top = 260
        self.rect.left = 700


class Weather:
    def __init__(self):
        self.clouds_1 = load_screen_im('cloud.png')
        self.clouds_2 = load_screen_im('cloud2.png')
        self.clouds_3 = load_screen_im('cloud3.png')
        self.rect = self.clouds_1.get_rect()
        self.rect.left, self.rect.top = 400, 0
        self.rect2 = self.clouds_1.get_rect()
        self.rect2.left, self.rect2.top = 700, -50
        self.rect3 = self.clouds_1.get_rect()
        self.rect3.left, self.rect3.top = 300, 50

        self.sun_1 = load_screen_im('sun.png')
        self.rect4 = self.sun_1.get_rect()
        self.rect4.left, self.rect4.top = 600, 100

        self.weather = 'sun'
        self.clouds = False
        self.sun = True
        self.catch_clouds = False
        self.catch_sun = False

        self.counter = 0

    def update(self, pause):
        self.counter += 1
        if not pause and self.counter % 3 == 0:
            if self.catch_clouds:
                if self.rect.left > -300:
                    self.rect = self.rect.move(-3, 0)
                if self.rect2.left > -300:
                    self.rect2 = self.rect2.move(-4, 0)
                if self.rect3.left > -300:
                    self.rect3 = self.rect3.move(-5, 0)
                if self.rect.left <= -300 and self.rect2.left <= -300 and self.rect3.left <= -300:
                    self.catch_clouds = False
                    self.clouds = False

            if self.catch_sun:
                if self.rect4.left > -300:
                    self.rect4 = self.rect4.move(-2, 0)
                if self.rect4.left <= -300:
                    self.catch_sun = False
                    self.sun = False

            if self.clouds and not self.catch_clouds:
                self.rect = self.rect.move(-2, 0)
                if self.rect.left <= -300:
                    self.rect.left = 700
                self.rect2 = self.rect2.move(-3, 0)
                if self.rect2.left <= -300:
                    self.rect2.left = 700
                self.rect3 = self.rect3.move(-4, 0)
                if self.rect3.left <= -300:
                    self.rect3.left = 700
            elif self.sun and not self.catch_sun:
                self.rect4 = self.rect4.move(-1, 0)
                if self.rect4.left <= -300:
                    self.rect4.left = 600

    def change_weather(self, weather):
        if self.weather != weather:
            if weather == 'sun':
                self.weather = 'sun'
                self.rect4.left, self.rect.top = 700, 0
                self.sun = True
                self.catch_clouds = True
            else:
                self.weather = 'clouds'
                self.rect.left, self.rect.top = 700, 0
                self.rect2.left, self.rect2.top = 850, -50
                self.rect3.left, self.rect3.top = 900, 50
                self.clouds = True
                self.catch_sun = True


if __name__ == '__main__':
    app = App()
    app.start_game()
