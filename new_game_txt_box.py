import pygame as pg
import main

WIDTH = 800
HEIGHT = 600

screen = pg.display.set_mode((WIDTH, HEIGHT))

FPS = 60

clock = pg.time.Clock()


def player_char(txt_box):
    done = False
    while not done:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit('Forced_Quit')

            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if txt_box.rect.collidepoint(event.pos):
                    txt_box.clicked()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True

                if txt_box.active:
                    if event.key == pg.K_RETURN:
                        print(txt_box.text)
                        txt_box.text = ''
                    elif event.key == pg.K_BACKSPACE:
                        txt_box.text = txt_box.text[:-1]
                    else:
                        txt_box.text += event.unicode
        screen.fill((30, 30, 30))
        txt_box.draw()
        pg.display.update()
