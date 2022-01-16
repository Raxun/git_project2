import os
import sys
import pygame


def load_image(name, colorkey=None):
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


pygame.init()
screen_size = (990, 600)
screen = pygame.display.set_mode(screen_size)
FPS = 60
tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png'),
    'spawn': load_image('spawn.png'),
    'finish': load_image('finish.png')
}
player_image = load_image('mario.png')


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 990, 600)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 8, tile_height * pos_y + 3)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0] + 10, tile_height * self.pos[1] + 3)


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
tile_width = tile_height = 30


def load_level(filename):
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Tile('empty', x, y)
                Tile('finish', x, y)
            elif level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                Tile('spawn', x, y)
                new_player = Player(x, y)
                level[y][x] == '.'
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    symbols_true = ['.', '@', '*']
    if movement == 'up':
        if y > 0 and (level_map[y - 1][x] in symbols_true):
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and (level_map[y + 1][x] in symbols_true):
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and (level_map[y][x - 1] in symbols_true):
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and (level_map[y][x + 1] in symbols_true):
            hero.move(x + 1, y)
    x, y = hero.pos
    if level_map[y][x] == '*':
        print('здесь будет оповещение о пройденом уровне')


def terminate():
    pygame.quit()
    sys.exit()


def start_game():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    hero.kill()
                    levels()
                elif event.key == pygame.K_UP:
                    move(hero, 'up')
                elif event.key == pygame.K_DOWN:
                    move(hero, 'down')
                elif event.key == pygame.K_LEFT:
                    move(hero, 'left')
                elif event.key == pygame.K_RIGHT:
                    move(hero, 'right')

        sprite_group.draw(screen)
        hero_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


def levels():
    global level_map
    screen.fill(pygame.Color(37, 9, 54))
    levels = []
    while True:
        pygame.display.update()
        for filename in os.walk("levels"):
            levels = filename[-1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            i = 0
            y = 0
            for elem in levels:
                if levels.index(elem) > 3:
                    y += 125
                    i = 0
                elem = elem[0:-4]
                button = Button(100, 100)
                level_map = load_level(elem + '.map')
                button.draw(50 + i, 50 + y, elem, selected_level, 100)
                i += 125
        '''button.draw(100, 420, 'Уровни', levels, 50)'''
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["Лабиринт"]
    screen.fill(pygame.Color(37, 9, 54))
    button = Button(250, 50)
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(255, 251, 22))
        intro_rect = string_rendered.get_rect()
        text_coord += 100
        intro_rect.top = text_coord
        intro_rect.x = 400
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            button.draw(100, 420, 'Уровни', levels, 30)
        '''button.draw(100, 420, 'Начать игру', start_game, 50)'''
        pygame.display.flip()
        clock.tick(FPS)


def selected_level():
    global hero, max_x, max_y
    screen.fill(pygame.Color(37, 9, 54))
    hero, max_x, max_y = generate_level(level_map)
    start_game()


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (37, 9, 54)
        self.active_color = (32, 33, 79)
        self.border_color = (255, 251, 22)

    def draw(self, x, y, message, action, size):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.border_color, (x, y, self.width, self.height))
            pygame.draw.rect(screen, self.active_color, (x + 5, y + 5, self.width - 10, self.height - 10))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, self.border_color, (x, y, self.width, self.height))
            pygame.draw.rect(screen, self.inactive_color, (x + 5, y + 5, self.width - 10, self.height - 10))

        font = pygame.font.Font(None, size)
        message = font.render(message, True, pygame.Color(255, 251, 22))
        screen.blit(message, (x + 15, y + 15))


start_screen()
pygame.quit()
