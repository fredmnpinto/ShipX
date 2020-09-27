# testing game running protocols:
import json
import random
from pprint import pprint
import new_game_screen as NewGame
import pygame as pg
from pygame import mixer
import time
from render_func import render
import math
import csv


pg.init()
pg.font.init()

# SETTING WINDOW
WIDTH, HEIGHT = 800, 600
FONT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (0, 0, 0)
# SOUNDS
bullet_sound = mixer.Sound('sounds/small_laser.wav')
bullet_sound.set_volume(0.02)
close_snd = mixer.Sound('sounds/close.ogg')
click_snd = mixer.Sound('sounds/click.ogg')
bong_snd = mixer.Sound('sounds/bong.ogg')


# IMAGE SETTING:
icon = pg.image.load('img/spaceship.png')

# spaceship
ship = pg.image.load('img/spaceship.png')
ship_img = pg.transform.scale(ship, (64, 64))
ship_img = pg.transform.rotate(ship_img, 270)

bullet_img = pg.image.load('img/bullet.png')
bullet_img = pg.transform.scale(bullet_img, (32, 32))
big_laser_arr = [pg.image.load('img/n_laser/sprite_0.png'),
                 pg.image.load('img/n_laser/sprite_1.png'),
                 pg.image.load('img/n_laser/sprite_2.png'),
                 pg.image.load('img/n_laser/sprite_3.png'),
                 pg.image.load('img/n_laser/sprite_4.png'),
                 pg.image.load('img/n_laser/sprite_5.png')]

# asteroins
small_astoroid = pg.image.load('img/asteroid(2).png')
small_astoroid = pg.transform.scale(small_astoroid, (64, 64))
medium_astoroid = pg.image.load('img/asteroid(1).png')
medium_astoroid = pg.transform.scale(medium_astoroid, (80, 80))
large_astoroid = pg.image.load('img/asteroid(0).png')
large_astoroid = pg.transform.scale(large_astoroid, (128, 128))

# background
in_game_bg = pg.image.load('img/background.png')


# main menu
# arrow_img = pg.image.load('img/arrow.png')
# arrow_img = pg.transform.scale(arrow_img, (64, 64))
arrow_img = pg.transform.rotate(ship_img, 90)

pg.display.set_icon(icon)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ShipX")

comet_img = pg.image.load('img/comet.png')

# CLASSES
class MainMenu:
    sprites =[
    pg.image.load('img/main_menu/Frame001.png'),
    pg.image.load('img/main_menu/Frame002.png'),
    pg.image.load('img/main_menu/Frame003.png'),
    pg.image.load('img/main_menu/Frame004.png'),
    pg.image.load('img/main_menu/Frame005.png'),
    pg.image.load('img/main_menu/Frame006.png'),
    pg.image.load('img/main_menu/Frame007.png')
]

    def __init__(self):
        self.img = self.sprites[0]
        self.count = 0
        self.sub_count = 0
    def update_img(self):
        self.img = self.sprites[self.count]
    def up_count(self):
        self.sub_count += 1
        if self.sub_count >= 8:
            if self.count < 6:
                self.count += 1
            else:
                self.count = 0
            self.sub_count = 0
        self.update_img()
    def draw_menu_bg(self):
        self.up_count()
        screen.blit(self.img, (0, 0))

class TextBox():
    font = pg.font.Font(None, 32)
    colors_dict = {
        'active': pg.Color('dodgerblue2'),
        'inactive': pg.Color('lightskyblue3')
    }

    def __init__(self, x = WIDTH/2 - 70, y = 100, w = 140, h = 32):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = ''
        self.active = False
        self.color = self.colors_dict['inactive']
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.surface = self.font.render(self.text, True, self.color)

    def clicked(self):
        if self.active:
            self.active = False
            self.color = self.colors_dict['inactive']
        else:
            self.active = True
            self.color = self.colors_dict['active']

    def draw(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.w = max(200, self.surface.get_width() + 10)
        # screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        screen.blit(self.surface, (self.x + 1, self.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 15
        self.img = bullet_img
        self.mask = pg.mask.from_surface(self.img)
        self.dmg = 1

    def spawn_bullet(self):
        screen.blit(self.img, (self.x, self.y))

    def get_height(self):
        return self.img.get_height()

    def get_width(self):
        return self.img.get_width()

    def move_bullet(self):
        self.y -= self.vel

    def collision(self, obj):
        return collide(self, obj)

    def off_screen(self):
        if self.y <= HEIGHT and self.y >= 0:
            return False
        else:
            print(f'bullet {self} went offscreen')
            return True


class BigLaser(Bullet):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprites = big_laser_arr
        self.img = self.sprites[0]
        self.vel = 6
        self.sprite_count = 0
        self.sub_count = 0
        self.mask = pg.mask.from_surface(self.img)
        self.dmg = 5

    def spawn_laser(self):
        screen.blit(self.img, (self.x, self.y))
        if self.sub_count <= 5:
            self.sub_count += 1
        else:
            self.sprite_count += 1
            self.sub_count = 0
            self.img = self.sprites[self.sprite_count]

    def move_laser(self):
        self.y -= self.vel


class Ship:
    def __init__(self):
        self.x, self.y = 336, 300
        self.hp = 100
        # self.sprite_count = 0
        # self.sub_count = 0
        # self.ship_img = ship_arr[self.sprite_count]
        self.ship_img = ship_img
        self.bullets = []
        self.cool_down = 0
        self.mask = pg.mask.from_surface(self.ship_img)
        self.max_hp = 100
        self.vel = 5
        self.dead = False
        self.shooting_count = 0
        self.name = ''
    def shoot(self):
        self.shooting_count += 1
        if self.shooting_count >= 5:
            b = BigLaser(self.x, self.y)
            self.shooting_count = 0
        else:
            b = Bullet(self.x + self.get_width() / 2 - 16, self.y)
        if len(self.bullets) >= 10:  # WORKING: if the list of bullets gets too long
            self.bullets.reverse()  # it deletes the oldest bullet
            self.bullets.pop()
            print('just popped a bullet')
        self.bullets.append(b)
        print(f'shooting {b} number {len(self.bullets)}')
        bullet_sound.play()

    def draw(self, screen):
        # self.sub_count += 1
        # if self.sub_count == 8:
        #     self.ship_img = ship_arr[self.sprite_count]
        #     self.sub_count = 0
        #     if self.sprite_count < 3:
        #         self.sprite_count += 1
        #     else:
        #         self.sprite_count = 0
        screen.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def move_bullets(self, objs):
        for b in self.bullets[:]:
            if b == BigLaser:
                b.move_laser()
            else:
                b.move_bullet()
            if b.off_screen():
                self.bullets.remove(b)
            else:
                for obj in objs:
                    if b.collision(obj):
                        obj.health -= b.dmg
                        try:
                            self.bullets.remove(
                                b)  # find and fix this error self.bullets.remove(x) -- x not in list [erro que ocorreu mas nao houve repeticao]
                        except:  # UPDATE: Error still there, but with try and except it is possible to ignore it
                            print('suposto crash')
                        print('bullet collided')
                        print(f'asteroid {obj}\nsupposedly took 1 damage and has {obj.health} hp')


class Asteroid:
    ASTEROID_DIC = {
        2: (small_astoroid, 3, 1, 1),
        1: (medium_astoroid, 2, 2, 3),
        0: (large_astoroid, 1, 5, 10)
    }

    def __init__(self, size, velocity=3):
        self.img, self.vel, self.health, self.score = self.ASTEROID_DIC[size]
        self.mask = pg.mask.from_surface(self.img)
        self.x = random.randrange(0, 800 - self.img.get_width())
        self.y = -(self.img.get_height())
        # self.spin_degree = 0
        # self.spin_side = random.choice([1, -1])
        self.size = size

    def move(self):
        self.y += self.vel
    #     self.rotate()
    #
    # def rotate(self):
    #     self.img = pg.transform.rotate(self.img, self.spin_degree)
    #     self.spin_degree += self.size * self.spin_side
class Comet():
    def __init__(self):
        self.x = HEIGHT
        self.y = WIDTH
        self.angle = math.pi/6 # 30 degrees
        self.img = pg.transform.rotate(comet_img, self.angle * 180/math.pi)
        self.sin = math.sin(self.angle)
        self.cos = math.cos(self.angle)

    def move_comet(self):
        self.y += self.sin
        self.x -= self.cos
        if self.off_screen():
            del self

    def off_screen(self):
        return self.x < 0 or self.y > HEIGHT + self.img.get_height()

    def spawn_comet(self):
        screen.blit(self.img, (self.x, self.y))

# SETTING GAME MECHANICS
txt_box = TextBox(y= 120)
def new_game():
    return NewGame.player_char(txt_box)


def collide(obj1, obj2):
    offset = (int(obj2.x - obj1.x), int(obj2.y - obj1.y))
    result = obj1.mask.overlap(obj2.mask, offset) != None  # WORKING: It returns
    return result  # true if the two objs
    # overlap

# GLOBALS
main_menu = True
ship = Ship()

lvl_passing_time_active_g = 0
comet_arr = []

def save_progress(score = 0):
    with open('records.csv') as fr:  # working
        data = csv.DictReader(fr)
        data_copy = {}
        for row in data:
            data_copy[row['username']] = row['highest_score']

        pprint(data_copy)

        data_copy[ship.name] = score

        pprint(data_copy)

        with open('records.csv', 'w', newline='') as fw:  # working
            fieldnames = ['username', 'highest_score']
            writer = csv.writer(fw)
            writer.writerow(fieldnames)
            for key, value in data_copy.items():
                writer.writerow([key, value])

main_menu_obj = MainMenu()



def credits():
    credits_arr = [
        'General Fullstack Director:        Frederico Pinto',
        'Co-Creative Director:      Joao Pedro Ferronato',
        'Images:        Frederico Pinto together with flaticon',
        'SFX:       kenney.nl/assets'
    ]
    credits_font = pg.font.Font('font/notalot35.ttf', 30)
    credits_title_font = pg.font.Font('font/notalot35.ttf', 100)
    credits_title_lbl = render('Credits', credits_title_font, FONT_COLOR, OUTLINE_COLOR)
    esc_font = pg.font.Font('font/notalot35.ttf', 50)
    esc_lbl = esc_font.render('press -ESC- to go back', 1, FONT_COLOR)

    credits_on_screen = True

    while credits_on_screen:
        main_menu_obj.draw_menu_bg()
        credits_pos = 250
        screen.blit(credits_title_lbl, (WIDTH/2 - credits_title_lbl.get_width()/2, 100))
        screen.blit(esc_lbl, (HEIGHT - esc_lbl.get_height() - 5, WIDTH - esc_lbl.get_width() - 5))
        for txt in credits_arr:
            new_lbl = render(txt, credits_font, FONT_COLOR, OUTLINE_COLOR)
            screen.blit(new_lbl, (WIDTH/2 - new_lbl.get_width()/2, credits_pos))
            credits_pos += 50
        for event in pg.event.get():
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT:
                exit('credits_quit')
            if keys[pg.K_ESCAPE]:
                credits_on_screen = False
        pg.display.update()
    return True, 'NO_NAME_YET'

def game():
    running = True
    FPS = 60
    clock = pg.time.Clock()
    score = 0
    lives = 5



    asteroids = []
    asteroid_cd = 40
    bullets_cd = 20



    laser_lst = []

    # defining labels
    font = pg.font.Font('font/notalot35.ttf', 50)
    lost_font = pg.font.SysFont("comicsans", 70)

    hp_lbl = font.render(f"Lives: {lives}", 1, (255, 255, 255))
    scr_lbl = font.render(f"Score: {score}", 1, (255, 255, 255))
    game_title_font = pg.font.Font('font/notalot35.ttf', 150)



        # --MENU OPTIONS--
    menu_options_font = font


    game_title_lbl = render('ShipX', game_title_font, FONT_COLOR, OUTLINE_COLOR)
    # new_game_lbl = menu_options_font.render('New Game', 1, GREEN)
    new_game_lbl = render('New Game', menu_options_font, FONT_COLOR, OUTLINE_COLOR)
    records_lbl = render('Records', menu_options_font, FONT_COLOR, OUTLINE_COLOR)
    credits_lbl = render('Credits',menu_options_font, FONT_COLOR, OUTLINE_COLOR)
    quit_game_lbl = render('Quit Game', menu_options_font, FONT_COLOR, OUTLINE_COLOR)

    # game subfunctions
    def records_window(): # TODO finish records_window
        pass


    def draw_window():
        screen.blit(in_game_bg, (0,0)) # TODO in-game bg screen

        hp_lbl = font.render(f"Lives: {lives}", 1, (255, 255, 255))
        scr_lbl = font.render(f"Score: {score}", 1, (255, 255, 255))

        level = score % 250
        lvl_passing_time_active = lvl_passing_time_active_g

        if score == 250:
            level = 2
            lvl_passing_time_active += 120

        if lvl_passing_time_active > 0:
            lvl_passing_lbl = game_title_font.render(f'Level {level}', 1, (255, 255, 255))
            screen.blit(lvl_passing_lbl, (WIDTH/2 - lvl_passing_lbl.get_width()/2, HEIGHT/2 - lvl_passing_lbl.get_height()))
            lvl_passing_time_active -= 1


        spawn_nonplayers()
        ship.draw(screen)
        screen.blit(hp_lbl, (10, 10))
        screen.blit(scr_lbl, (WIDTH - scr_lbl.get_width(), 10))

        if ship.dead:
            player_death(score)

        pg.display.update()

    def new_asteroid():
        sizes = [0, 1, 2]  # large, medium, small
        size = random.choices(sizes, (20, 60, 20))[0]
        new = Asteroid(size=size)
        asteroids.append(new)

    def spawn_nonplayers():
        for asteroid in asteroids:
            screen.blit(asteroid.img, (asteroid.x, asteroid.y))
        for b in ship.bullets:
            b.spawn_bullet()

    def draw_menu_options():

        def new_game_opt(): # done
            exit('new_game_opt')
        def records_opt():
            print('still working on it')
            exit('records_opt')
        def credits_opt(): # done
            print('still working on it')
            exit('credits_opt')
        def quit_game_opt(): # done
            exit('quit_game_opt')

        MENU_OPTIONS_DICT = {
            0: new_game,
            -4: new_game,
            -3: records_opt,
            -2: credits,
            -1: quit_game_opt
        }


        def label_pos(label_obj):
            x_pos = WIDTH/2 - label_obj.get_width()/2
            y_pos = {
                new_game_lbl : 250,
                records_lbl : 300,
                credits_lbl : 350,
                quit_game_lbl : 400
            }
            return(x_pos, y_pos[label_obj])

        #SCREEN SELECTION ARROW
        def arrow_pos(label_x, label_y):
            obj_wid = WIDTH/2 - label_x
            arrow_x = label_x + obj_wid * 2 + 15
            arrow_y = label_y - 10
            return(arrow_x, arrow_y)

        arrow_pos_arr = [
            arrow_pos(label_pos(new_game_lbl)[0],label_pos(new_game_lbl)[1]),
            arrow_pos(label_pos(records_lbl)[0], label_pos(records_lbl)[1]),
                      arrow_pos(label_pos(credits_lbl)[0], label_pos(credits_lbl)[1]),
                      arrow_pos(label_pos(quit_game_lbl)[0], label_pos(quit_game_lbl)[1])
        ]
        arrow_current = 0



        def label_blit(label_obj):
            screen.blit(label_obj, (label_pos(label_obj)))
        main_menu = True

        main_menu_ani_count = 0
        menu_sub_count = 0



        comet_cd = 0

        while main_menu:

            if comet_cd <= 60:
                comet_cd += 1
            else:
                new_comet = Comet()
                comet_arr.append(new_comet)
                comet_cd = 0

            # for comet in comet_arr:
            #     comet.move_comet()
            #     comet.spawn_comet()
            #     print(comet) TODO CONSERTAR ESSA MERDA

            main_menu_obj.draw_menu_bg()
            # screen.blit(game_title_lbl, (WIDTH / 2 - game_title_lbl.get_width() / 2, 120))

            label_blit(new_game_lbl)
            label_blit(records_lbl)
            label_blit(credits_lbl)
            label_blit(quit_game_lbl)
            screen.blit(arrow_img, (arrow_pos_arr[arrow_current][0], arrow_pos_arr[arrow_current][1]))



            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                keys = pg.key.get_pressed()

                if keys[pg.K_UP] or keys[pg.K_w]:
                    if arrow_current > -4:
                        print(f'[W] antes :{arrow_current}')
                        arrow_current -= 1
                        print(f'[W] depois :{arrow_current}')
                    else:
                        arrow_current = 0
                    click_snd.play()
                    time.sleep(0.2)

                if keys[pg.K_DOWN] or keys[pg.K_s]:
                    if arrow_current < 0:
                        print(f'[S] antes :{arrow_current}')
                        arrow_current += 1
                        print(f'[S] depois :{arrow_current}')
                    else:
                        arrow_current = -3
                    click_snd.play()
                    time.sleep(0.2)

                if keys[pg.K_e] or keys[pg.K_RETURN]:
                    print(f'going for MENU_OPTIONS_DICT[{arrow_current}]')
                    bong_snd.play()
                    time.sleep(0.3)
                    main_menu, ship.name = MENU_OPTIONS_DICT[arrow_current]()
                    print(ship.name)
                    print(main_menu)

                if keys[pg.K_F1]:
                    print('-DEBUG MODE-')
                    main_menu = False
            screen.blit(game_title_lbl, (WIDTH/2 - game_title_lbl.get_width()/2, 100))
            pg.display.update()



    # main menu
    draw_menu_options()
    print(main_menu)
    # SOUNDS
    mixer.music.load('sounds/bg_music.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(0.3)


    # gameloop
    while running:

        if ship.dead:

            if FPS >= 15:
                FPS -= 1
        clock.tick(FPS)
        if lives <= 0 or ship.hp <= 0:
            ship.dead = True
        asteroid_cd -= 1
        if asteroid_cd <= 0:
            new_asteroid()
            asteroid_cd = 40
        ship.move_bullets(asteroids)
        for asteroid in asteroids[:]:
            asteroid.move()
            if asteroid.health <= 0:
                print('and was destroyed')
                asteroids.remove(asteroid)
                score += asteroid.score

            elif asteroid.y >= HEIGHT:
                print(f'asteroid {asteroid} passed through')
                asteroids.remove(asteroid)
                if lives > 0:
                    lives -= 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if bullets_cd > 0:
            bullets_cd -= 1
        if not ship.dead:
            keys = pg.key.get_pressed()
            if keys[pg.K_a] and ship.x - ship.vel > 0:
                ship.x -= ship.vel
            if keys[pg.K_d] and ship.x + ship.vel + ship.get_width() < WIDTH:
                ship.x += ship.vel
            if keys[pg.K_w] and ship.y - ship.vel > 0:
                ship.y -= ship.vel
            if keys[pg.K_s] and ship.y + ship.vel + ship.get_height() < HEIGHT:
                ship.y += ship.vel
            if keys[pg.K_SPACE] and bullets_cd == 0:
                ship.shoot()
                bullets_cd = 10
            if keys[pg.K_i]:
                FPS = 180
            if keys[pg.K_o]:
                FPS = 60
        draw_window()

first_time = True  # complement variable to player_death() to only be played once

def player_death(score):
    mixer.music.fadeout(1500)
    game_title_font = pg.font.Font('font/notalot35.ttf', 150)
    lost_label = render("You lost", game_title_font, (FONT_COLOR), (OUTLINE_COLOR))
    screen.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 200))
    global first_time
    if first_time: # working
        first_time = False
        save_progress(score)

if __name__ == '__main__':
    game()
