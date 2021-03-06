import os
import pygame
import random
import sys

pygame.init()
FPS = 50
fps = 10
points = 0
fenses = ["black_fense.png", "green_fense.png", "white_fense.png"]
chickens = ["black_chicken.png", 'green_chicken.png', 'white_chicken.png']
clock = pygame.time.Clock()
size = WIDTH, HEIGHT = 300, 400
screen = pygame.display.set_mode(size)
running = True
rule_group = pygame.sprite.Group()
lose_group = pygame.sprite.Group()
play_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
start_button = pygame.draw.rect(screen, (0, 0, 240), (25, 130, 245, 50))
pygame.display.flip()
all_sprites = pygame.sprite.Group()


def load_file(filename):
    filename = "data/" + filename
    f = open(filename, encoding="utf8")
    data = f.read()
    return data


def save_file(filename, number):
    filename = "data/" + filename
    f = open(filename, 'w')
    data = f.write(str(number))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


def nole_results():
    filenames = ['record.txt', 'move.txt', 'level.txt']
    for file in filenames:
        if file == 'move.txt':
            filename = "data/" + file
            f = open(filename, 'w')
            data = f.write(str(8))
        else:
            filename = "data/" + file
            f = open(filename, 'w')
            data = f.write(str(0))


def terminate():
    pygame.quit()
    sys.exit()


class BackButton(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(rule_group, lose_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("lightskyblue"))
        font = pygame.font.Font(None, 50)
        text = font.render(title, 1, (255, 255, 255))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class NoleButton(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(lose_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("lightskyblue"))
        font = pygame.font.Font(None, 50)
        text = font.render(title, 1, (255, 255, 255))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class RuleButton(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(rule_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("lightskyblue"))
        font = pygame.font.Font(None, 50)
        text = font.render(title, 1, (255, 255, 255))
        text_x = 5
        text_y = 7
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class PlayButton(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(play_group, lose_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("lightskyblue"))
        font = pygame.font.Font(None, 50)
        text = font.render(title, 1, (255, 255, 255))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class ExitButton(pygame.sprite.Sprite):
    def __init__(self, width, height, title, x, y):
        super().__init__(play_group, all_sprites)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color("lightskyblue"))
        font = pygame.font.Font(None, 50)
        text = font.render(title, 1, (255, 255, 255))
        text_x = 65
        text_y = 7
        self.image.blit(text, (text_x, text_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return True


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def getter(self):
        return self.x, self.y


class Fence(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        image = pygame.transform.scale(load_image(name), (300, 85))
        super().__init__(all_sprites)
        self.image = image
        self.name = name
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect = self.rect.move(0, 10)
        if pygame.sprite.collide_mask(self, chicken):

            return True
        else:
            return self.rect.y


class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        image = pygame.transform.scale(load_image(name), (100, 85))
        super().__init__(all_sprites)
        self.image = image
        self.name = name
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global chicken_color, movement
        global chicken, random_fence
        self.rect = self.rect.move(0, movement)
        if pygame.sprite.collide_mask(self, chicken):
            if self.name[0] == chickens[chicken_color][0]:
                self.kill()

                return True
            else:
                return False
        if pygame.sprite.collide_mask(self, random_fence):
            self.rect = self.rect.move(0, 7)
        return self.rect.y


chicken_color = 0
chicken = AnimatedSprite(load_image(chickens[chicken_color]), 3, 1, 113, 300)
fences = ["black_fense.png", "green_fense.png", "white_fense.png"]
fence_color = random.randint(0, 2)
random_fence = Fence(0, -85, fences[fence_color])
egg_sound = pygame.mixer.Sound('data/egg_sound.wav')


def pause():
    PAUSED = False
    pygame.mixer.music.pause()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.unpause()
                    PAUSED = not PAUSED
                    return


def game_screen():
    global chicken, points, movement
    global chicken_color
    pygame.mixer.music.load('data/fon1.mp3')
    movement = int(load_file('move.txt'))
    end_sound = pygame.mixer.Sound('data/end_sound.wav')
    fense_sound = pygame.mixer.Sound('data/fense_sound.wav')
    start_sound = pygame.mixer.Sound('data/start_sound.wav')
    win_sound = pygame.mixer.Sound('data/win_sound.wav')
    start_sound.play()
    level = int(load_file('level.txt'))
    screen = pygame.display.set_mode(size)
    running = True
    fences = ["black_fense.png", "green_fense.png", "white_fense.png"]
    chickens = ["black_chicken.png", 'green_chicken.png', 'white_chicken.png']
    eggs = ["black_egg.png", "green_egg.png", "white_egg.png"]
    x = 125
    fence_fox = False
    egg_fox = False
    chicken_color = 0
    screen.blit(load_image("game_fon.png"), (0, 0))
    chicken = AnimatedSprite(load_image(chickens[chicken_color]), 3, 1, chicken.rect[0], 300)
    chicken_group = pygame.sprite.Group(chicken)
    USEREVENT = 31
    USEREVENT1 = 23
    USEREVENT2 = 30
    pygame.time.set_timer(USEREVENT, 12000)
    pygame.time.set_timer(USEREVENT1, 3000)
    pygame.time.set_timer(USEREVENT2, 30000)
    points = 0
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)
    while running:
        screen.blit(load_image("game_fon.png"), (0, 0))
        font = pygame.font.Font(None, 50)
        points_text = font.render(str(points), 1, (0, 0, 0))
        screen.blit(points_text, (10, 10))
        level_text = font.render('L' + ' ' + str(level), 1, (0, 0, 0))
        screen.blit(level_text, (250, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                if WIDTH > (chicken.rect[0] - 100) > 0:
                    chicken.rect[0] -= 100
            if keys_pressed[pygame.K_RIGHT]:
                if (chicken.rect[0] + 100) < WIDTH:
                    chicken.rect[0] += 100
            if event.type == USEREVENT:
                fence_fox = True
                fence_color = random.randint(0, 2)
                random_fence = Fence(0, -85, fences[fence_color])
                fence_group = pygame.sprite.Group(random_fence)
                random_fence.update()
                fence_group.update()
                fence_group.draw(screen)

            if event.type == USEREVENT1:
                egg_fox = True
                random.shuffle(eggs)
                random_egg1 = Egg(0, -185, eggs[0])
                random_egg2 = Egg(100, -185, eggs[1])
                random_egg3 = Egg(200, -185, eggs[2])
                egg_group1 = pygame.sprite.Group(random_egg1)
                egg_group2 = pygame.sprite.Group(random_egg2)
                egg_group3 = pygame.sprite.Group(random_egg3)
                random_egg1.update()
                random_egg2.update()
                random_egg3.update()
                egg_group1.draw(screen)
                egg_group2.draw(screen)
                egg_group3.draw(screen)
            if event.type == USEREVENT2:
                movement += 2
                level += 1
                if level % 2 == 0:
                    points += 30
                    win_sound.play()
                    points_text = font.render(str(points), 1, (0, 0, 0))
                    screen.blit(points_text, (10, 10))
                random_egg1.update()
                random_egg2.update()
                random_egg3.update()
        if egg_fox:
            if random_egg1.update() > 500:
                egg_fox = False
                pygame.time.set_timer(USEREVENT1, 2600)
            if (random_egg1.update() is False) or (random_egg2.update() is False) or (random_egg3.update() is False):
                pygame.mixer.music.pause()
                end_sound.play()
                max_points = load_file('record.txt')
                save_file('level.txt', level)
                save_file('move.txt', movement)
                if points >= int(max_points):
                    max_points = points
                    save_file('record.txt', max_points)
                    lose_screen(max_points, max_points)
                else:
                    save_file('record.txt', max_points)
                    lose_screen(points, max_points)


            if (random_egg1.update() is True) or (random_egg2.update() is True) or (random_egg3.update() is True):
                egg_sound.play()
                points += 1

            random_egg2.update()
            random_egg3.update()
            egg_group1.draw(screen)
            egg_group2.draw(screen)
            egg_group3.draw(screen)

        if fence_fox:
            if random_fence.update() > 550:
                fence_fox = False
                pygame.time.set_timer(USEREVENT, 12000)
            if random_fence.update() == True:
                fense_sound.play()
                chicken_color = fence_color
                chicken = AnimatedSprite(load_image(chickens[chicken_color]), 3, 1, chicken.rect[0], 300)
                chicken_group = pygame.sprite.Group(chicken)
                chicken_group.update()
            random_fence.update()
            fence_group.draw(screen)
            chicken.update()
            chicken_group.draw(screen)
        if not fence_fox:
            chicken.update()
            chicken_group.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


def lose_screen(points, max_points):
    screen = pygame.display.set_mode(size)
    running = True
    intro_text1 = 'Вы проиграли('
    intro_text = ['Ваш рекорд' + ' ' + str(max_points), 'Вы набрали' + ' ' + str(points)]
    button_text = ["Меню", 'Играть', 'Новая игра']
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 65
    font1 = pygame.font.Font('data/STIXGeneralBolIta.ttf', 40)
    text = font1.render(intro_text1, 1, (200, 0, 0))
    text_x = 15
    text_y = 20
    screen.blit(text, (text_x, text_y))
    for line in intro_text:
        string_rendered = font.render(line, 2, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 17
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    back_button = BackButton(250, 40, button_text[0], 25, 200)
    new_button = PlayButton(250, 40, button_text[1], 25, 270)
    nole_button = NoleButton(250, 40, button_text[2], 25, 340)
    lose_group.draw(screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_click(event.pos):
                    back_button.kill()
                    new_button.kill()
                    nole_button.kill()
                    start_screen()
                else:
                    pass
                if new_button.check_click(event.pos):
                    new_button.kill()
                    back_button.kill()
                    nole_button.kill()
                    game_screen()
                else:
                    pass

                if nole_button.check_click(event.pos):
                    nole_results()
                    new_button.kill()
                    back_button.kill()
                    nole_button.kill()
                    start_screen()
                else:
                    pass

        pygame.display.flip()
        clock.tick(FPS)


def rule_screen():
    screen = pygame.display.set_mode(size)
    running = True
    intro_text = ["Правила игры", 'Назад']
    fon = pygame.transform.scale(load_image('rule_fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    back_button = BackButton(250, 50, intro_text[1], 25, 340)
    rule_group.draw(screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_click(event.pos):
                    print("clicked")
                    back_button.kill()
                    start_screen()
                else:
                    pass
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["COLOR ROAD", "",
                  "Правила игры",
                  "Играть", 'Выход']

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(intro_text[0], 1, (176, 226, 255))
    text_x = 30
    text_y = 30
    screen.blit(text, (text_x, text_y))
    rule_button = RuleButton(250, 50, intro_text[2], 20, 160)
    play_button = PlayButton(250, 50, intro_text[3], 20, 230)
    exit_button = ExitButton(250, 50, intro_text[4], 20, 300)
    exit_group.draw(screen)
    rule_group.draw(screen)
    play_group.draw(screen)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rule_button.check_click(event.pos):
                    print("clicked")
                    rule_button.kill()
                    play_button.kill()
                    rule_screen()
                else:
                    pass

                if play_button.check_click(event.pos):
                    print("clicked")
                    rule_button.kill()
                    play_button.kill()
                    game_screen()
                else:
                    pass

                if exit_button.check_click(event.pos):
                    print("clicked")
                    pygame.quit()
                else:
                    pass

        pygame.display.flip()
        clock.tick(FPS)


start_screen()
