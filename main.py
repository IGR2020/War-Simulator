import pygame as pg
from EPT import load_sprite_sheets
from time import time
from random import randint

WIDTH, HEIGHT = 900, 500
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("War Simulator")

run = True
clock = pg.time.Clock()
fps = 60

assets = {"Soldier": load_sprite_sheets("assets\Soldier", 100, 100, resize=(200, 200))}

class Soldier:
    def __init__(self, x, y, health, speed, attack, defence, defence_faulter, critical_hit_chance) -> None:

        self.name = "Soldier"

        # stats
        self.health = health
        self.speed = speed
        self.attack = attack
        self.defence = defence
        self.faulter_rate = defence_faulter
        self.critical_hit_chance = critical_hit_chance

        self.direction = "_left"

        # core elements
        self.x_vel = 0
        self.y_vel = 0
        self.rect = pg.Rect(x, y, assets["Soldier"]["Soldier-Idle" + self.direction][0].get_width(), assets["Soldier"]["Soldier-Idle" + self.direction][0].get_height())
        self.mask = pg.mask.from_surface(assets["Soldier"]["Soldier-Idle" + self.direction][0])

        # animating elements
        self.animation_count = 0
        self.animation_speed = 3
        self.is_hit = False
        self.timeSinceLastHit = time()
        self.hit_time = 2

        # path finding
        self.target = None

    def display(self, window, x_offset=0, y_offset=0):
        if time() - self.timeSinceLastHit > self.hit_time:
            self.is_hit = False

        if self.x_vel > 0: self.direction = "_right"
        elif self.x_vel < 0: self.direction = "_left"

        sprite_sheet_name = "Soldier-Idle"
        if self.is_hit:
            sprite_sheet_name = "Soldier-Hurt"
        elif self.x_vel != 0 or self.y_vel != 0:
            sprite_sheet_name = "Soldier-Walk"

        sprites = assets[self.name][sprite_sheet_name + self.direction]
        sprite_index = (self.animation_count // self.animation_speed) % len(sprites)

        self.animation_count += 1

        window.blit(sprites[sprite_index], (self.rect.x - x_offset, self.rect.y - y_offset))

    def script(self):


        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        self.x_vel = 0
        self.y_vel = 0
        
        if self.target is None: return

        if self.target[0] > self.rect.x: self.x_vel = self.speed
        elif self.target[0] < self.rect.x: self.x_vel = -self.speed
        if self.target[1] > self.rect.y: self.y_vel = self.speed
        elif self.target[1] < self.rect.y: self.y_vel = -self.speed





class Army:
    def __init__(self, warriors) -> None:
        self.warriors = warriors

    def display(self, window, x_offset=0, y_offset=0):
        for warrior in self.warriors:
            warrior.display(window, x_offset, y_offset)

    def target(self, target):
        for warrior in self.warriors:
            warrior.target = target

    def halt(self):
        for warrior in self.warriors:
            warrior.target = None

    def script(self):
        for warrior in self.warriors:
            warrior.script()


bulk = []
for i in range(6, 9):
    for j in range(1, 7):
        bulk.append(Soldier(i*50 + randint(-10, 10), j*50 + randint(-10, 10), 10, 2, 10, 10, 10, 10))
test = Army(bulk)

def display():
    window.fill((200, 130, 10))
    test.display(window)
    pg.display.update()


while run:

    clock.tick(fps)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            test.target(pg.mouse.get_pos())

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                test.halt()

    test.script()

    display()

pg.quit()
quit()
