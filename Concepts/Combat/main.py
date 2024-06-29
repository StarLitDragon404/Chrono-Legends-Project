import pygame as pg
import random
import counter

WIDTH = 1200
HEIGHT = 800
FPS = 60

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

font = pg.font.SysFont('Arial', 30)

class Note(pg.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.level = level
        self.image = pg.transform.scale_by(pg.image.load('assets/note.png'), 4)
        self.rect = self.image.get_rect()
        if self.level == 1:
            self.rect.center = (250+(WIDTH-350), HEIGHT-240+15)
        elif self.level == 2:
            self.rect.center = (250+(WIDTH-350), HEIGHT-200+15)
        elif self.level == 3:
            self.rect.center = (250+(WIDTH-350), HEIGHT-160+15)
        elif self.level == 4:
            self.rect.center = (250+(WIDTH-350), HEIGHT-120+15)
    def update(self):
        self.rect.x -= 4
        if self.rect.left <= 250:
            self.kill()
            pg.mixer.Sound(f'assets/note{self.level}.wav').play()

notes = pg.sprite.Group()
counter_manager = counter.CounterManager()

pattern = [(1, 1), (2, 0.5), (3, 2), (4, 1)]
pattern.append((4, 0))
pattern.append((3, 0))
index = 0

def add_note():
    global index
    notes.add(Note(pattern[index][0]))
    
    index += 1
    if index < len(pattern):

        counter_manager.add(counter.Counter(round(FPS*pattern[index-1][1]), add_note))
enemy_turn = False

def init_enemy_turn():
    global enemy_turn, index, pattern
    counter_manager.add(counter.Counter(FPS*1, add_note))
    enemy_turn = True
    pattern = [(1, 1), (2, 0.5), (3, 2), (4, 1)]
    pattern.append((4, 0))
    pattern.append((3, 0))
    index = 0


def draw():
    global enemy_turn

    keys = pg.key.get_pressed()
    if enemy_turn:
        pg.draw.rect(screen, (255, 255, 255), pg.Rect(250, HEIGHT-250, WIDTH-350, 200), 3)

        surf_num1 = font.render("1", False, (0, 255, 0) if keys[pg.K_1] else (255, 255, 255))
        surf_num2 = font.render("2", False, (0, 255, 0) if keys[pg.K_2] else (255, 255, 255))
        surf_num3 = font.render("3", False, (0, 255, 0) if keys[pg.K_3] else (255, 255, 255))
        surf_num4 = font.render("4", False, (0, 255, 0) if keys[pg.K_4] else (255, 255, 255))

        screen.blit(surf_num1, (220, HEIGHT-240))
        screen.blit(surf_num2, (220, HEIGHT-200))
        screen.blit(surf_num3, (220, HEIGHT-160))
        screen.blit(surf_num4, (220, HEIGHT-120))
        notes.draw(screen)
        notes.update()



run = True

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    screen.fill((0, 0, 0))
    clock.tick(FPS)
    draw()
    counter_manager.update()
    pg.display.flip()