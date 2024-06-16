import pygame as pg
from EPT import load_sprite_sheets
from time import time
from random import randint
from pygame.image import load
from pygame.transform import scale_by

WIDTH, HEIGHT = 900, 500
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("War Simulator")

run = True
clock = pg.time.Clock()
fps = 60

banner_size = 32

assets = {"Soldier": load_sprite_sheets(r"assets\Soldier", 100, 100, autocrop=True)}
assets["Soldier Banner"] = scale_by(load(r"assets\Soilder Banner.png"), 2)


class Soldier:
    def __init__(
        self, x, y, health, speed, attack, defence, defence_faulter, critical_hit_chance
    ) -> None:

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
        self.rect = pg.Rect(
            x,
            y,
            assets["Soldier"]["Soldier-Idle" + self.direction][0].get_width(),
            assets["Soldier"]["Soldier-Idle" + self.direction][0].get_height(),
        )
        self.mask = pg.mask.from_surface(
            assets["Soldier"]["Soldier-Idle" + self.direction][0]
        )

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

        if self.x_vel > 0:
            self.direction = "_right"
        elif self.x_vel < 0:
            self.direction = "_left"

        sprite_sheet_name = "Soldier-Idle"
        if self.is_hit:
            sprite_sheet_name = "Soldier-Hurt"
        elif self.x_vel != 0 or self.y_vel != 0:
            sprite_sheet_name = "Soldier-Walk"

        sprites = assets[self.name][sprite_sheet_name + self.direction]
        sprite_index = (self.animation_count // self.animation_speed) % len(sprites)

        self.animation_count += 1

        window.blit(
            sprites[sprite_index], (self.rect.x - x_offset, self.rect.y - y_offset)
        )

    def script(self):

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        self.x_vel = 0
        self.y_vel = 0

        if self.target is None:
            return

        if (
            abs(self.rect.centerx - self.target[0]) < 10
            and abs(self.rect.centery - self.target[1]) < 10
        ):
            self.target = None
            return

        if self.target[0] > self.rect.centerx:
            self.x_vel = self.speed
        elif self.target[0] < self.rect.centerx:
            self.x_vel = -self.speed
        if self.target[1] > self.rect.centery:
            self.y_vel = self.speed
        elif self.target[1] < self.rect.centery:
            self.y_vel = -self.speed


class Banner:
    def __init__(self, name, pos):
        self.name = name
        self.rect = assets[self.name].get_rect(center=pos)

    def display(self, window, x_offset=0, y_offset=0):
        window.blit(assets[self.name], (self.rect.x - x_offset, self.rect.y - y_offset))


class Army:
    def __init__(self, warriors, formation: tuple[int, int], leader=None) -> None:
        self.warriors = warriors
        self.leader = leader  # index of leader warrior
        if leader is None:
            self.leader = len(self.warriors) // 2
        self.banner = Banner(
            "Soldier Banner",
            (
                self.warriors[self.leader].rect.x,
                self.warriors[self.leader].rect.y - banner_size * 1.2,
            ),
        )
        self.formation = []
        for x in range(formation[0]):
            for y in range(formation[1]):
                self.formation.append((x * 50, y * 50))

    def display(self, window, x_offset=0, y_offset=0):
        for i, warrior in enumerate(self.warriors):
            if i == self.leader:
                self.banner.display(window, x_offset, y_offset)
            warrior.display(window, x_offset, y_offset)

    def target(self, target, space=False):
        for i, warrior in enumerate(self.warriors):
            if space:
                warrior.target = target[0] + self.formation[i][0] + randint(
                    -10, 10
                ), target[1] + self.formation[i][1] + randint(-10, 10)
                continue
            warrior.target = target

    def halt(self):
        for warrior in self.warriors:
            warrior.target = None

    def script(self):
        for warrior in self.warriors:
            warrior.script()
            self.banner.rect.center = (
                self.warriors[self.leader].rect.x,
                self.warriors[self.leader].rect.y - banner_size * 1.2,
            )


bulk = []
for i in range(6, 9):
    for j in range(1, 7):
        bulk.append(
            Soldier(
                i * 50 + randint(-10, 10),
                j * 50 + randint(-10, 10),
                10,
                2,
                10,
                10,
                10,
                10,
            )
        )
test = Army(bulk, (9 - 6, 7 - 1))
bulk = []
for i in range(1, 4):
    for j in range(1, 7):
        bulk.append(
            Soldier(
                i * 50 + randint(-10, 10),
                j * 50 + randint(-10, 10),
                10,
                2,
                10,
                10,
                10,
                10,
            )
        )
test2 = Army(bulk, (4 - 1, 7 - 1))
armyies = [test, test2]

def display():
    window.fill((200, 130, 10))
    test.display(window)
    test2.display(window)
    if mouse_down:
        pg.draw.line(window, (255, 0, 0), initial_mouse_pos, pg.mouse.get_pos())
    pg.display.update()


mouse_down = False
selected_army = None

while run:

    clock.tick(fps)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_down = True
            initial_mouse_pos = pg.mouse.get_pos()
            for i, army in enumerate(armyies):
                if army.banner.rect.collidepoint(pg.mouse.get_pos()):
                    selected_army = i
        
        if event.type == pg.MOUSEBUTTONUP:
            mouse_down = False
            if selected_army is not None:
                armyies[selected_army].target(pg.mouse.get_pos(), True)
            selected_army = None

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                for army in armyies:
                    army.halt()

    test.script()
    test2.script()

    display()

pg.quit()
quit()
