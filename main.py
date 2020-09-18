# testing game running protocols:
import random
from pygame import mixer
import pygame as pg
import json
from pprint import pprint



pg.init()
pg.font.init()

# SETTING WINDOW
WIDTH, HEIGHT = 800, 600



# IMAGE SETTING:
icon = pg.image.load('img/spaceship.png')

# spaceship
ship = pg.image.load('img/spaceship.png')
ship = pg.transform.scale(ship, (64, 64))
bullet = pg.image.load('img/bullet.png')
bullet = pg.transform.scale(bullet, (32, 32))

bullet_sound = mixer.Sound('sounds/small_laser.wav')
bullet_sound.set_volume(0.02)

# asteroins
small_astoroid = pg.image.load('img/asteroid(2).png')
small_astoroid = pg.transform.scale(small_astoroid, (64, 64))
medium_astoroid = pg.image.load('img/asteroid(1).png')
medium_astoroid = pg.transform.scale(medium_astoroid, (80, 80))
large_astoroid = pg.image.load('img/asteroid(0).png')
large_astoroid = pg.transform.scale(large_astoroid, (128, 128))

# background
bg = pg.image.load('img/background.png')
bg = pg.transform.scale(bg, (WIDTH, HEIGHT))

# main menu
arrow_img = pg.image.load('img/arrow.png')
arrow_img = pg.transform.scale(arrow_img, (64, 64))

pg.display.set_icon(icon)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ShipX")


# CLASSES
class Spritesheet():
    def __init__(self, obj):
        json_path = f'img/{obj}/{obj}.json'
        try:
            img_path = f'img/{obj}/{obj}.png'
        except:
            img_path = f'img/{obj}/{obj}.jpg'
        self.spritesheet = pg.image.load(img_path)
        self.json_file = json_path
        self.SPRITES = None
        self.frames = []
        self.read_json()

    def read_json(self):
        with open(self.json_file, 'r') as data:
            self.SPRITES = json.load(data)
            print('Printing json data as:')
            pprint(self.SPRITES)
            for i in self.SPRITES['frames']:
                print(i)
                frame_values = []
                
                for x in self.SPRITES['frames'][i]['frame'].values():
                    print(x)
                    frame_values.append(x)
                
                self.frames.append(self.get_image(frame_values[0], frame_values[1], frame_values[2], frame_values[3]))
                frame_values.clear()
            pprint(self.frames)

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image # TODO: Change the bullet sprites to these OR: Make new type of bullet

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 15
        self.img = bullet
        self.mask = pg.mask.from_surface(self.img)

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

class BigLaser(Bullet): # TODO: ANIMATION NOT WORKING
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprites = Spritesheet('laser')
        self.img = self.sprites.frames[0]
        self.vel = 10
        self.sprite_count = 0
        self.mask = pg.mask.from_surface(self.img)

    def spawn_laser(self):
        screen.blit(self.img, (self.x, self.y))
        if self.sprite_count < 4:
            self.sprite_count += 1
        else:
            self.sprite_count = 0
        self.img = self.sprites.frames[self.sprite_count]

    def move_laser(self):
        self.y -= self.vel

class Ship:
    def __init__(self, x, y, hp=100):
        self.x = x
        self.y = y
        self.hp = hp
        self.ship_img = ship
        self.bullets = []
        self.cool_down = 0
        self.mask = pg.mask.from_surface(self.ship_img)
        self.max_hp = hp
        self.vel = 1
        self.dead = False
        self.shooting_count = 0

    def shoot(self):
        self.shooting_count += 1
        if self.shooting_count >= 3:
            b = BigLaser(self.x, self.y)
            self.shooting_count = 0
        else:
            b = Bullet(self.x + self.get_width()/2 - 16, self.y)
        if len(self.bullets) >= 10: # WORKING: if the list of bullets gets too long
            self.bullets.reverse()  #          it deletes the oldest bullet
            self.bullets.pop()
            print('just popped a bullet')
        self.bullets.append(b)
        print(f'shooting {b} number {len(self.bullets)}')
        bullet_sound.play()

    def draw(self, screen):
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
                        obj.health -= 1
                        try:
                            self.bullets.remove(b) # find and fix this error self.bullets.remove(x) -- x not in list [erro que ocorreu mas nao houve repeticao]
                        except:                    # UPDATE: Error still there, but with try and except it is possible to ignore it
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
# SETTING GAME MECHANICS
def collide(obj1, obj2):
    offset = (int(obj2.x - obj1.x), int(obj2.y - obj1.y))
    result = obj1.mask.overlap(obj2.mask, offset) != None # WORKING: It returns
    return result                                         # true if the two objs
                                                          # overlap
def game():
    running = True
    FPS = 12
    clock = pg.time.Clock()
    score = 0
    lives = 5
    font = pg.font.SysFont("comicsans", 50)
    lost_font = pg.font.SysFont("comicsans", 70)

    asteroids = []
    asteroid_cd = 40
    bullets_cd = 1
    level = 1


    laser_lst = []


    # game subfunctions
    def draw_window():
        screen.fill((255, 255, 255))
        screen.blit(bg, (0, 0))
        hp_lbl = font.render(f"Lives: {lives}", 1, (255, 255, 255))
        scr_lbl = font.render(f"Score: {score}", 1, (255, 255, 255))

        spawn_nonplayers()
        ship.draw(screen)
        screen.blit(hp_lbl, (10, 10))
        screen.blit(scr_lbl, (WIDTH - scr_lbl.get_width(), 10))

        if ship.dead:
            mixer.music.fadeout(1500)
            lost_label = lost_font.render("You lost", 1, (255, 255, 255))
            screen.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 200))

        pg.display.update()


    def new_asteroid():
        sizes = [0, 1, 2]   # large, medium, small
        size = random.choices(sizes, (20, 60, 20))[0]
        new = Asteroid(size=size)
        asteroids.append(new)

    def spawn_nonplayers():
        for asteroid in asteroids:
            screen.blit(asteroid.img, (asteroid.x, asteroid.y))
        for b in ship.bullets:
            b.spawn_bullet()

    def draw_menu_options():
        # MENU OPTIONS
        menu_options_font = pg.font.SysFont('comicsans', 50)

        new_game_lbl = menu_options_font.render('New Game', 1, (255, 255, 255))
        records_lbl = menu_options_font.render('Records', 1, (255, 255, 255))
        credits_lbl = menu_options_font.render('Credits', 1, (255, 255, 255))
        quit_game_lbl = menu_options_font.render('Quit Game', 1, (255, 255, 255))

        screen.blit(new_game_lbl, (WIDTH / 2 - new_game_lbl.get_width() / 2, 250))
        screen.blit(arrow_img, (WIDTH / 2 - new_game_lbl.get_width() + arrow_img.get_width(), 250))
        screen.blit(records_lbl, (WIDTH / 2 - records_lbl.get_width() / 2, 300))
        screen.blit(credits_lbl, (WIDTH / 2 - credits_lbl.get_width() / 2, 350))
        screen.blit(quit_game_lbl, (WIDTH / 2 - quit_game_lbl.get_width() / 2, 400))


    def draw_main_menu():
        game_title_font = pg.font.SysFont('comicsans', 100)
        game_title_lbl = game_title_font.render('ShipX', 1, (255, 255, 255))
        screen.blit(bg, (0, 0))
        screen.blit(game_title_lbl, (WIDTH / 2 - game_title_lbl.get_width() / 2, 120))

        draw_menu_options()

        pg.display.update()
        

    # subfunctions calls
    ship = Ship(336, 300)
    main_menu = True
    # main menu
    while main_menu:

        draw_main_menu()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                main_menu = False
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            main_menu = False

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




game()