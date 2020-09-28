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
    github_obj = main.BrowserLink()
    done = False
    title_font = pg.font.Font('font/notalot35.ttf', 50)
    font = title_font
    esc_lbl = font.render('press -ESC- to go back', 1, (255, 255, 255))
    username_lbl = title_font.render('Enter your username:', 1, (255, 255, 255))
    rec_box = pg.Rect(100, 200, WIDTH - 200, HEIGHT - 250)
    feedback_txt = ''
    data = []

    bg = main.MainMenu()

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
                if github_obj.rect.collidepoint(event.pos):
                    click_snd.play()
                    time.sleep(0.1)
                    github_obj.clicked()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    back_snd.play()
                    time.sleep(0.2)
                    return True, 'NO_NAME_ERROR'

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
                            confirm_snd.play()
                            time.sleep(0.3)
                            # set the input to the players name
                            main.ship.name = txt_box.text

                            return False, txt_box.text

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
        # screen.fill((30, 30, 30))
        bg.draw_menu_bg()
        github_obj.draw()
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


def records_screen():
    github_obj = main.BrowserLink()
    records_on_screen = True
    font = pg.font.Font('font/notalot35.ttf', 40)
    sub_font = pg.font.Font('font/notalot35.ttf', 30)
    title_font = pg.font.Font('font/notalot35.ttf', 120)
    subtitle_label = sub_font.render('all the people who played', 1, (255, 255, 255))
    rec_title = title_font.render('Records', 1, (255, 255, 255))
    esc_label = font.render('press -ESC- to go back', 1, (255, 255, 255))
    rect_rec = pg.Rect(50, 200, WIDTH - 100, HEIGHT - 250)

    data = []
    with open('records.csv', 'r') as fr:
        rec_csv = csv.DictReader(fr)
        for item in rec_csv:
            data.append(item)
    scoreboard_x = rect_rec.x + 5

    rec_bg = main.MainMenu()
    while records_on_screen:
        rec_bg.draw_menu_bg()
        github_obj.draw()
        pg.draw.rect(screen, (60, 60, 60), rect_rec)
        screen.blit(rec_title, (WIDTH / 2 - rec_title.get_width() / 2, 40))
        screen.blit(subtitle_label, (WIDTH / 2 - subtitle_label.get_width() / 2, 40 + rec_title.get_height() + 5))
        screen.blit(esc_label, (WIDTH - esc_label.get_width() - 5, HEIGHT - esc_label.get_height() - 5))
        scoreboard_y = rect_rec.y + 5
        pg.time.Clock().tick(FPS)
        count = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit('records forced quit')
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    records_on_screen = False
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if github_obj.rect.collidepoint(event.pos):
                    click_snd.play()
                    time.sleep(0.1)
                    github_obj.clicked()

        for plr in data:
            count += 1
            plr_name_lbl = font.render(plr['username'], 1, (200, 255, 205))
            plr_score_lbl = font.render(plr['highest_score'], 1, (200, 255, 205))

            screen.blit(plr_name_lbl, (scoreboard_x, scoreboard_y))
            screen.blit(plr_score_lbl, (WIDTH - scoreboard_x - plr_score_lbl.get_width(), scoreboard_y))
            scoreboard_y += plr_score_lbl.get_height() + 10
            print(scoreboard_x, scoreboard_y)

        pg.display.update()


if __name__ == '__main__':
    obj = main.TextBox()
    player_char(obj)
