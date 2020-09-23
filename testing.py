import pygame as pg

pg.init()

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)

screen = pg.display.set_mode((WIDTH, HEIGHT))

run = True
while run:

    screen.fill(BLACK)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
