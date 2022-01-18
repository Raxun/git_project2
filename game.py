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
FPS = 30
notification = False
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
    global notification
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
        notification = True
        hero.kill()
        levels()



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
    global name_map, delete_name, notification
    screen.fill(pygame.Color(37, 9, 54))
    name_levels = []
    if notification:
        font = pygame.font.Font(None, 40)
        message = font.render('Уровень пройден!', True, pygame.Color(255, 251, 22))
        screen.blit(message, (635, 215))
        notification = False
    font = pygame.font.Font(None, 40)
    message = font.render('Мои уровни:', True, pygame.Color(255, 251, 22))
    screen.blit(message, (80, 215))
    while True:

        pygame.display.update()
        for filename in os.walk("levels"):
            name_levels = filename[-1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            i = 0
            y = 0
            for elem in name_levels:
                if name_levels.index(elem) > 3 and y == 0:
                    y += 240
                    i = 0
                if name_levels.index(elem) > 3:
                    delete_name = elem
                    button = Button(175, 50)
                    button.draw(80 + i, 455, 'удалить', delete_level, 30, 45, 15)
                elem = elem[0:-4]
                button = Button(175, 175)
                name_map = elem + '.map'
                button.draw(80 + i, 20 + y, elem, selected_level, 100, 68, 55)
                i += 210
            button = Button(805, 60)
            button.draw(80, 520, 'Создать уровень', create_level, 45, 270, 15)
        pygame.display.flip()
        clock.tick(FPS)


def delete_level():
    name_levels = []
    for filename in os.walk("levels"):
        name_levels = filename[-1]
    for i in range(4, len(name_levels)):
        if name_levels.index(name_levels[i]) > name_levels.index(delete_name):
            name = int(name_levels[i][0:-4]) - 1
            os.replace('levels/' + name_levels[i], 'levels/' + str(name) + '.map')
        elif name_levels.index(name_levels[i]) == name_levels.index(delete_name):
            name = int(name_levels[i][0:-4])
            os.replace('levels/' + name_levels[i], 'levels/' + str(name) + '.map')
            os.remove('levels/' + delete_name)
    levels()


def create_level():
    global create_element_x, create_element_y, type, name_level
    screen.fill(pygame.Color(37, 9, 54))
    flag_spawn = False
    flag_finish = False
    flag_btn = False
    for filename in os.walk("levels"):
        if len(filename[-1]) < 8:
            name_level = str(len(filename[-1]) + 1)
        else:
            levels()
    new_level = open(name_level + '.map', "w")
    for y in range(20):
        if y == 0:
            new_level.write('.' * 34 + '\n')
        elif y == 19:
            new_level.write('.' * 33 + '\n')
            new_level.write('.')
        else:
            new_level.write('.' * 33 + '\n')
    new_level.close()
    while True:
        pygame.display.update()
        with open(name_level + '.map', 'r') as f:
            level = f.read()
        x, y = 0, 0
        level = level.split()
        for element in level:
            for elem in element:
                if elem == '#':
                    pygame.draw.rect(screen, (255, 251, 22), (x * 30, y * 30, 30, 30), 1)
                if elem == '.':
                    pygame.draw.rect(screen, (32, 33, 79), (x * 30, y * 30, 30, 30), 1)
                    pygame.draw.rect(screen, (37, 9, 54), ((x * 30) + 2, (y * 30) + 2, 26, 26), 1)
                if elem == '@':
                    pygame.draw.rect(screen, (139, 0, 255), (x * 30, y * 30, 30, 30), 1)
                    flag_spawn = True
                if elem == '*':
                    pygame.draw.rect(screen, (0, 127, 255), (x * 30, y * 30, 30, 30), 1)
                    flag_finish = True
                x += 1
            x = 0
            y += 1
        if flag_btn:
            button = Button(990, 600)
            button.draw(0, 0, 'Внимание! Добавьте старт и финиш', levels, 45, 220, 270)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    x, y = pygame.mouse.get_pos()
                    type = '@'
                    create_element_x = x // 30
                    create_element_y = y // 30
                    create_element()
                elif event.key == pygame.K_f:
                    x, y = pygame.mouse.get_pos()
                    type = '*'
                    create_element_x = x // 30
                    create_element_y = y // 30
                    create_element()
                elif event.key == pygame.K_ESCAPE:
                    new_level.close()
                    if flag_spawn and flag_finish:
                        os.replace(name_level + '.map', "levels/" + name_level + '.map')
                        levels()
                    else:
                        flag_btn = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                type = '#'
                create_element_x = x // 30
                create_element_y = y // 30
                create_element()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    screen.fill(pygame.Color(37, 9, 54))
    button = Button(400, 60)
    font = pygame.font.Font(None, 70)
    message = font.render("Лабиринт", True, pygame.Color(255, 251, 22))
    screen.blit(message, (370, 150))
    while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                button.draw(280, 320, 'Начать игру', levels, 35, 125, 20)
            pygame.display.flip()
            clock.tick(FPS)


def selected_level():
    global hero, max_x, max_y, name_map, level_map
    level_map = load_level(name_map)
    screen.fill(pygame.Color(37, 9, 54))
    hero, max_x, max_y = generate_level(level_map)
    start_game()


def check_element(sp, element):
    flag = False
    for elem in sp:
        if element not in elem or element == '#':
            flag = True
            if element == '#':
                flag = delete_element()
                return flag
        else:
            delete_element()
            flag = False
            return flag
    return flag


def create_element():
    new_data = []
    sp = []
    with open(name_level + '.map', 'r') as f:
        old_data = f.read()
        old_data = old_data.split('\n')
        for element in old_data:
            for elem in element:
                sp.append(elem)
            new_data.append(sp)
            sp = []
    if check_element(new_data, type):
        del new_data[create_element_y][create_element_x]
        new_data[create_element_y].insert(create_element_x, type)
        with open(name_level + '.map', 'w+') as f:
            for element in new_data:
                element = ''.join(element)
                f.write(element + '\n')


def delete_element():
    new_data = []
    sp = []
    with open(name_level + '.map', 'r') as f:
        old_data = f.read()
        old_data = old_data.split('\n')
        for element in old_data:
            for elem in element:
                sp.append(elem)
            new_data.append(sp)
            sp = []
    flag = True
    if new_data[create_element_y][create_element_x] != '.':
        del new_data[create_element_y][create_element_x]
        new_data[create_element_y].insert(create_element_x, '.')
        flag = False
    with open(name_level + '.map', 'w+') as f:
        for element in new_data:
            element = ''.join(element)
            f.write(element + '\n')
    return flag


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (37, 9, 54)
        self.active_color = (32, 33, 79)
        self.border_color = (255, 251, 22)

    def draw(self, x, y, message, action, size, text_offset_x, text_offset_y):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            if click[0] == 1 and action is not None:
                action()
            pygame.draw.rect(screen, self.border_color, (x, y, self.width, self.height))
            pygame.draw.rect(screen, self.active_color, (x + 5, y + 5, self.width - 10, self.height - 10))

        else:
            pygame.draw.rect(screen, self.border_color, (x, y, self.width, self.height))
            pygame.draw.rect(screen, self.inactive_color, (x + 5, y + 5, self.width - 10, self.height - 10))

        font = pygame.font.Font(None, size)
        message = font.render(message, True, pygame.Color(255, 251, 22))
        screen.blit(message, (x + text_offset_x, y + text_offset_y))


start_screen()
pygame.quit()
