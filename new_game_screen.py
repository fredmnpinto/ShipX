import pygame as pg
import main
import csv
import time
from pygame import mixer

WIDTH = 800
HEIGHT = 600

screen = pg.display.set_mode((WIDTH, HEIGHT))

FPS = 60

clock = pg.time.Clock()

mixer.init()
if mixer.get_init():
    back_snd = mixer.Sound('sounds/back.ogg')
    confirm_snd = mixer.Sound('sounds/confirmation.ogg')
    close_snd = mixer.Sound('sounds/close.ogg')


def player_char(txt_box):
    done = False
    font = pg.font.SysFont('comicsans', 30)
    esc_lbl = font.render('press -ESC- to go back', 1, (255, 255, 255))

    rec_box = pg.Rect(100, 200, WIDTH - 200, HEIGHT - 250)
    csv_r = {}
    with open('records.csv', 'r') as rf:
        csv_r = csv.DictReader(rf)

    while not done:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                close_snd.play()
                time.sleep(0.2)
                exit('Forced_Quit')

            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if txt_box.rect.collidepoint(event.pos):
                    txt_box.clicked()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    back_snd.play()
                    time.sleep(0.2)

                    done = True

                if txt_box.active:
                    if event.key == pg.K_RETURN:
                        for name in csv_r:
                            print('username: ', name)
                            if name['username'] == txt_box.text:
                                print('name already exists')
                                confirm_snd.play()
                                time.sleep(0.3)
                                print(txt_box.text)
                        txt_box.text = ''
                    elif event.key == pg.K_BACKSPACE:
                        txt_box.text = txt_box.text[:-1]
                    elif len(txt_box.text) < 10:
                        txt_box.text += event.unicode

        screen.fill((30, 30, 30))
        pg.draw.rect(screen, (60, 60, 60), rec_box)
        screen.blit(esc_lbl, (WIDTH - esc_lbl.get_width(), 10))
        txt_box.draw()
        pg.display.update()


if __name__ == '__main__':
    obj = main.TextBox()
    player_char(obj)
