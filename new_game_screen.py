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
    click_snd = mixer.Sound('sounds/click.ogg')


def player_char(txt_box):
    done = False
    font = pg.font.SysFont('comicsans', 25)
    esc_lbl = font.render('press -ESC- to go back', 1, (255, 255, 255))
    username_lbl = pg.font.SysFont('comicsans', 40).render('Enter your username:', 1, (255, 255, 255))
    rec_box = pg.Rect(100, 200, WIDTH - 200, HEIGHT - 250)
    feedback_txt = ''
    data = []
    with open('records.csv', 'r') as rf:
        csv_r = csv.DictReader(rf)
        for item in csv_r:
            data.append(item)
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
                    click_snd.play()
                    time.sleep(0.1)
                    txt_box.clicked()
                elif txt_box.active:
                    txt_box.clicked()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    back_snd.play()
                    time.sleep(0.2)

                    done = True
                    return

                if txt_box.active:
                    if event.key == pg.K_RETURN:
                        already_exists = False
                        for name in data:
                            if name['username'] == txt_box.text:
                                print('username: ', name['username'])
                                print('name already exists')
                                print(txt_box.text)
                                feedback_txt = 'Already Exists'
                                already_exists = True
                                back_snd.play()
                                time.sleep(0.2)
                                break
                            else:
                                feedback_txt = ''
                        if not already_exists and len(txt_box.text) > 3:
                            feedback_txt = ''
                            confirm_snd.play()
                            time.sleep(0.3)
                            return # game
                        if len(txt_box.text) <= 3:
                            feedback_txt = 'Too Short'
                            back_snd.play()
                            time.sleep(0.2)
                        txt_box.text = ''
                    elif event.key == pg.K_BACKSPACE:
                        txt_box.text = txt_box.text[:-1]
                    elif len(txt_box.text) < 10:
                        txt_box.text += event.unicode
                        txt_box.text = txt_box.text.upper()
        scoreboard_y = rec_box.y + 20
        scoreboard_x = rec_box.x + 50
        screen.fill((30, 30, 30))
        pg.draw.rect(screen, (60, 60, 60), rec_box)
        feedback_lbl = font.render(feedback_txt, 1, (255, 255, 255))
        screen.blit(username_lbl, (WIDTH / 2 - username_lbl.get_width() / 2, username_lbl.get_height() / 2 + 50))
        screen.blit(esc_lbl, (WIDTH - esc_lbl.get_width() - 5, HEIGHT - esc_lbl.get_height() - 5))
        txt_box.draw()
        screen.blit(feedback_lbl, (WIDTH / 2 - feedback_lbl.get_width() / 2, txt_box.y + txt_box.h + 5))
        for plr in data:
            # print(player['username'], '\t', player['highest_score'])
            plr_name_lbl = font.render(plr['username'], 1, (200, 255, 205))
            plr_score_lbl = font.render(plr['highest_score'], 1, (200, 255, 205))
            screen.blit(plr_name_lbl, (scoreboard_x, scoreboard_y))
            screen.blit(plr_score_lbl, (WIDTH - scoreboard_x - plr_score_lbl.get_width(), scoreboard_y))
            scoreboard_y += plr_score_lbl.get_height() + 10
        pg.display.update()


if __name__ == '__main__':
    obj = main.TextBox()
    player_char(obj)
