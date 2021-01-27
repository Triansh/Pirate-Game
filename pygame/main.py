import pygame
import random
import configparser

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
pygame.init()

var = configparser.RawConfigParser()
var.read('./config_file.ini')

ftype = var.get('font', 'type')
fsize = int(var.get('font', 'size'))
c1 = eval(var.get('color', 'black'))
c2 = eval(var.get('color', 'yellow'))
c3 = eval(var.get('color', 'blue'))
c4 = eval(var.get('color', 'white'))
m1 = var.get('message', 'win')
m2 = var.get('message', 'lose')
m3 = var.get('message', 'p1')
m4 = var.get('message', 'p2')
m5 = var.get('message', 'timi')
m6 = var.get('message', 'wp1')
m7 = var.get('message', 'wp2')
m8 = var.get('message', 'wp3')
m9 = var.get('message', 'ranout')
m10 = var.get('message', 'pause')

scrwidth = 1000
scrheight = 750
win = pygame.display.set_mode((scrwidth, scrheight))
pygame.display.set_caption("River Pirate Game")
font = pygame.font.SysFont(ftype, fsize)
text1 = font.render(m2, True, (255, 128, 0))
text2 = font.render(m1, True, (255, 128, 0))
music = pygame.mixer.music.load('the-buccaneers-haul.wav')
pygame.mixer.music.play(-1)
explode_sound = pygame.mixer.Sound('Explosion+5.wav')
evil_laugh = pygame.mixer.Sound('SF-laughter1.wav')
clock = pygame.time.Clock()
no_of_partitions = 6
partition_width = scrwidth
partition_height = 50
river_height = (scrheight - no_of_partitions * partition_height) / (
        no_of_partitions - 1)
fps = 20
timing = 60 * fps
no_of_trees = 5
no_of_obstacles = 4 * no_of_trees
run = True
pause = False
tile_img = pygame.image.load('Tile.png')
tile_img = pygame.transform.scale(tile_img, (scrwidth // 5, partition_height))
canx = 100


class Player(object):

    def __init__(self, playerx, playery, playerwidth, playerheight):
        self.playerx = playerx
        self.playery = playery
        self.playerwidth = playerwidth
        self.playerheight = playerheight
        self.velsprite = 6
        self.walkcount = 0
        self.left = False
        self.right = False
        self.up = True
        self.down = False
        self.standing = False
        self.p1 = True
        self.p2 = False
        self.score = [0, 0]
        self.passp2 = self.passp1 = [False for i in range(9)]
        self.walk_right = [0 for i in range(12)]
        self.walk_up = [0 for i in range(12)]
        self.walk_down = [0 for i in range(12)]
        self.walk_left = [0 for i in range(12)]
        self.wright = [0 for i in range(4)]
        self.wup = [0 for i in range(4)]
        self.wdown = [0 for i in range(4)]
        self.wleft = [0 for i in range(4)]
        self.playerhb = (self.playerx + 10, self.playery +
                         20, self.playerwidth - 15,
                         self.playerheight - 25)

    def load_image(self):
        for i in range(4):
            self.walk_up[i] = pygame.image.load(
                'player1/tile00' + str(i) + '.png')
            self.walk_left[i] = pygame.image.load(
                'player1/tile0' + str(i + 15) + '.png')
            self.walk_right[i] = pygame.image.load(
                'player1/tile0' + str(i + 10) + '.png')
            self.walk_down[i] = pygame.image.load(
                'player1/tile00' + str(i + 5) + '.png')
        for i in range(4):
            self.wup[i] = pygame.image.load(
                'player2/tile0' + str(i + 12) + '.png')
            self.wleft[i] = pygame.image.load(
                'player2/tile00' + str(i + 4) + '.png')
            self.wright[i] = pygame.image.load(
                'player2/tile0' + ('0' if i + 8 <= 9 else '') + str(
                    i + 8) + '.png')
            self.wdown[i] = pygame.image.load(
                'player2/tile00' + str(i) + '.png')

    def do_false(self):
        self.standing = self.left = self.right = self.up = self.down = False

    def player_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.playerx > self.velsprite:
            self.playerx -= self.velsprite
            self.do_false()
            self.left = True
        elif keys[pygame.K_RIGHT] and \
                self.playerx < scrwidth - self.velsprite - self.playerwidth:
            self.playerx += self.velsprite
            self.do_false()
            self.right = True
        elif keys[pygame.K_UP] and self.playery > self.velsprite:
            self.playery -= self.velsprite
            self.do_false()
            self.up = True
        elif keys[
            pygame.K_DOWN] and \
                boy.playery < scrheight - self.velsprite - self.playerheight:
            self.playery += self.velsprite
            self.do_false()
            self.down = True
        else:
            self.standing = True

    def draw(self, win):
        if self.walkcount + 1 > fps:
            self.walkcount = 0
        self.playerhb = (self.playerx + 10, self.playery +
                         20, self.playerwidth - 15,
                         self.playerheight - 25)
        if not self.check_hit(win):
            if self.p1:
                if not self.standing:
                    if self.left:
                        win.blit(pygame.transform.scale(
                            self.walk_left[self.walkcount // 5],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.right:
                        win.blit(pygame.transform.scale(
                            self.walk_right[self.walkcount // 5],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.up:
                        win.blit(pygame.transform.scale(
                            self.walk_up[self.walkcount // 5],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.down:
                        win.blit(pygame.transform.scale(
                            self.walk_down[self.walkcount // 5],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    self.walkcount += 1
                else:
                    if self.left:
                        win.blit(pygame.transform.scale(
                            self.walk_left[3],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.right:
                        win.blit(pygame.transform.scale(
                            self.walk_right[0],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.up:
                        win.blit(pygame.transform.scale(
                            self.walk_up[3],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.down:
                        win.blit(pygame.transform.scale(
                            self.walk_down[2],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
            else:
                if not self.standing:
                    if self.left:
                        win.blit(pygame.transform.scale(
                            self.wleft[self.walkcount // 5],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.right:
                        win.blit(pygame.transform.scale(
                            self.wright[self.walkcount // 5],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.up:
                        win.blit(pygame.transform.scale(
                            self.wup[self.walkcount // 5],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.down:
                        win.blit(pygame.transform.scale(
                            self.wdown[self.walkcount // 5],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    self.walkcount += 1
                else:
                    if self.left:
                        win.blit(pygame.transform.scale(
                            self.wleft[0],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.right:
                        win.blit(pygame.transform.scale(
                            self.wright[0],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.up:
                        win.blit(pygame.transform.scale(
                            self.wup[0],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))
                    elif self.down:
                        win.blit(pygame.transform.scale(
                            self.wdown[0],
                            (self.playerwidth, self.playerheight)),
                            (self.playerx, self.playery))

    def is_hit(self, win):
        win.fill((0, 0, 0))
        win.blit(text1, (scrwidth / 2 - text1.get_width() /
                         2, scrheight / 2 - text1.get_height() / 2))
        evil_laugh.play()
        self.change_player(win)

    def check_hit(self, win):
        for j in range(no_of_obstacles // no_of_trees):
            for k in range(no_of_trees):
                mx = (monster.obsx[j][k] -
                      monster.image_width / 2) + monster.randx[j]
                my = partitionlist[j % 4] - monster.img_height / 2
                tree_hitbox = (
                    mx + 40, my + 90, monster.image_width / 2 - 10, 20)
                if self.playerhb[0] + self.playerhb[2] >= tree_hitbox[
                    0] and self.playerhb[0] <= tree_hitbox[0] + tree_hitbox[
                            2]:
                    if self.playerhb[1] <= tree_hitbox[1] + tree_hitbox[
                        3] and self.playerhb[1] + self.playerhb[3] >= \
                            tree_hitbox[1]:
                        self.is_hit(win)
                        return True

        for i in range(5):
            if self.playerhb[0] + self.playerhb[2] >= \
                    ships[i].hitbox[0] and self.playerhb[0] <= \
                    ships[i].hitbox[0] + ships[i].hitbox[2]:
                if self.playerhb[1] <= ships[i].hitbox[1] + \
                        ships[i].hitbox[3] and self.playerhb[1] + \
                        self.playerhb[3] >= ships[i].hitbox[1]:
                    self.is_hit(win)
                    return True

        for i in range(4):
            if self.playerhb[0] + self.playerhb[2] >= \
                    cannon[i].ball_hitbox[0] and self.playerhb[0] <= \
                    cannon[i].ball_hitbox[0] + cannon[i].ball_hitbox[2]:
                if self.playerhb[1] <= cannon[i].ball_hitbox[1] + \
                        cannon[i].ball_hitbox[3] and self.playerhb[1] + \
                        self.playerhb[3] >= cannon[i].ball_hitbox[1]:
                    self.is_hit(win)
                    return True
            if self.playerhb[0] + self.playerhb[2] >= \
                    cannon[i].cannon_hitbox[0] and self.playerhb[0] <= \
                    cannon[i].cannon_hitbox[0] + cannon[i].cannon_hitbox[2]:
                if self.playerhb[1] <= cannon[i].cannon_hitbox[1] + \
                        cannon[i].cannon_hitbox[3] and self.playerhb[1] + \
                        self.playerhb[3] >= cannon[i].cannon_hitbox[1]:
                    self.is_hit(win)
                    return True

        return False

    def change_player(self, win):
        global timing
        pygame.display.update()
        pygame.time.wait(2000)
        evil_laugh.stop()
        self.do_false()
        self.playerx = scrwidth / 2
        self.passp2 = self.passp1 = [False for i in range(9)]
        monster.change_obs()
        if self.p1:
            self.playery = 0
            self.p1 = False
            self.p2 = True
            self.down = True
        else:
            self.playery = scrheight - self.playerheight - self.velsprite
            self.p2 = False
            self.p1 = True
            self.up = True
        timing = 60 * fps

    def go_to_win(self, win):
        win.fill((0, 0, 0))
        win.blit(text2, (scrwidth / 2 - text2.get_width() /
                         2, scrheight / 2 - text2.get_height() / 2))
        self.change_player(win)

    def change_score(self):

        if self.p2:
            sums = partition_height
            for i in range(9):
                if i % 2:
                    sums += partition_height
                else:
                    sums += river_height
                if self.playery + self.playerheight / 2 > sums and self.passp1[
                        i] is False:
                    self.passp1[i] = True
                    self.score[1] += (fps * 10) if i % 2 == 0 else 5 * fps
        else:
            sums = scrheight - partition_height
            for i in range(9):
                if i % 2:
                    sums -= partition_height
                else:
                    sums -= river_height
                if self.playery + self.playerheight / 2 < sums \
                        and self.passp1[i] is False:
                    self.passp1[i] = True
                    self.score[0] += fps * 10 if i % 2 == 0 else 5 * fps


class Projectile(object):

    def __init__(self, cannonx, cannony, acc, rad, cany):
        self.cannonx = cannonx
        self.cannony = cannony
        self.velx = random.randint(10, 15)
        self.vely = -random.randint(15, 20)
        self.acc = acc
        self.rad = rad
        self.canImg = [0 for i in range(6)]
        self.image_width = self.img_height = 100
        self.img_count = 0
        self.which_one = 1
        self.explode = [0 for i in range(15)]
        self.ball_img = 0
        self.visible = False
        self.cany = cany
        self.cannon_hitbox = (canx, self.cany + self.img_height / 4,
                              3 * self.image_width // 5 + 5,
                              3 * self.img_height // 5)
        self.ball_hitbox = (self.cannonx + self.rad,
                            self.cannony - self.rad, self.rad * 2,
                            self.rad * 2)

    def image_load(self):
        for i in range(6):
            self.canImg[i] = pygame.image.load(
                'cannon-frame/tile00' + str(i) + '.png')
            self.canImg[i] = pygame.transform.scale(
                self.canImg[i], (self.image_width, self.img_height))
        for i in range(15):
            self.explode[i] = pygame.image.load(
                'explosion-frame/tile0' + ('0' if i <= 9 else '') + str(
                    i) + '.png')
            self.explode[i] = pygame.transform.scale(
                self.explode[i],
                (3 * self.image_width // 4, 3 * self.img_height // 4))
        self.ball_img = pygame.image.load('cannonball.png')
        self.ball_img = pygame.transform.scale(
            self.ball_img, (2 * self.rad, 2 * self.rad))

    def move(self):

        if self.which_one == 2 or self.visible:
            if self.cannony <= self.cany + self.img_height / 2:
                self.cannonx += int(0.75 * self.velx)
                self.cannony += int(0.75 * (self.vely + 0.5 * self.acc))
                self.vely += 0.75 * self.acc
            else:
                explode_sound.play()
                self.which_one = 3
                self.img_count = 0
                self.visible = False
        self.ball_hitbox = (self.cannonx + self.rad,
                            self.cannony - self.rad, self.rad * 2,
                            self.rad * 2)

    def draw(self, win):
        self.move()
        self.img_count += 1
        win.blit(self.canImg[0], (canx, self.cany))
        if self.which_one == 1:
            if (self.img_count * 2 // 7) <= 5:
                win.blit(self.canImg[self.img_count * 2 // 7],
                         (canx, self.cany))
                if self.img_count * 2 // 7 >= 4:
                    self.visible = True
            else:
                self.which_one = 2

        if self.which_one == 3:
            if (2 * self.img_count // 3) % 15 < 14:
                win.blit(self.explode[(2 * self.img_count // 3) % 15],
                         (self.cannonx, self.cannony - self.img_height / 2))
            else:
                self.which_one = 1
                explode_sound.stop()
                self.img_count = 0
                self.velx = random.randint(10, 15)
                self.vely = -random.randint(15, 20)
                self.cannonx = canx + 85
                self.cannony = self.cany + 32

        if self.visible:
            win.blit(self.ball_img, (self.cannonx +
                                     self.rad, self.cannony - self.rad))


class MovingObj(object):
    ship_left = pygame.image.load('1stshipL.png')
    ship_right = pygame.image.load('1stshipR.png')

    def __init__(self, x, y, width, height, end, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = [vel, vel]
        self.swim = 0
        self.path = [0, self.end]
        self.hitbox = (self.x, self.y + self.height /
                       2, self.width, 2 * self.height // 5)

    def move(self):
        p = 0 if boy.p1 else 1
        if self.vel[p] > 0:
            if self.x + self.vel[p] + self.width < self.path[1]:
                self.x += self.vel[p]
            else:
                self.swim = 0
                self.vel[p] *= -1
        else:
            if self.x + self.vel[p] > self.path[0]:
                self.x += self.vel[p]
            else:
                self.vel[p] *= -1
                self.swim = 0
        self.hitbox = (self.x, self.y + self.height /
                       2, self.width, 2 * self.height // 5)

    def draw(self, win):
        self.move()
        if boy.p1:
            p = 0
        else:
            p = 1
        if self.swim + 1 >= fps:
            self.swim = 0

        if self.vel[p] > 0:
            win.blit(pygame.transform.scale(self.ship_right,
                                            (self.width, self.height)),
                     (self.x, self.y))
            self.swim += 1
        else:
            win.blit(pygame.transform.scale(self.ship_left,
                                            (self.width, self.height)),
                     (self.x, self.y))
            self.swim += 1


class FixObs(object):

    def __init__(self, image_width, img_height):
        self.image_width = image_width
        self.img_height = img_height
        self.mons_img = pygame.image.load('tree.png')
        self.randx = [0 for i in range(no_of_obstacles // no_of_trees)]
        self.obsx = [[0, 0, 0, 0] for i in range(no_of_obstacles)]
        self.img_no = [0 for j in range(no_of_obstacles)]
        self.img_count = 0

    def draw_fixed_obs(self, win):
        self.img_count += 1
        if self.img_count + 1 > 2 * fps:
            self.img_count = 0
        for j in range(no_of_obstacles // no_of_trees):
            for k in range(no_of_trees):
                mx = (self.obsx[j][k] - self.image_width / 2) + self.randx[j]
                my = partitionlist[j % 4] - self.img_height / 2

                win.blit(pygame.transform.scale(self.mons_img,
                                                (self.image_width,
                                                 self.img_height)), (mx, my))

    def change_obs(self):
        for i in range(no_of_obstacles // no_of_trees):
            x = random.randint(10 * i, 10 * (i + 1)) + 50
            self.randx[i] = random.randint(420, 600)
            y = []
            for j in range(no_of_trees):
                t = x + j * self.image_width / 2
                y.append(t)
            self.obsx[i] = y


def ship_formation():
    for j in range(5):
        x = 0
        if j % 2:
            x = scrwidth - 40
        any_ship = MovingObj(x, (j + 1) * partition_height + (2 * j + 1) *
                             river_height / 2 - 40, 80, 80, scrwidth, 8)
        ships[j] = any_ship


def build_background():
    win.fill(c3)
    for i in range(no_of_partitions):
        for j in range(5):
            win.blit(tile_img, (
                j * scrwidth // 5, i * (partition_height + river_height)))
    print_text()
    boy.draw(win)
    for i in range(5):
        ships[i].draw(win)
    boy.change_score()
    for i in range(4):
        cannon[i].draw(win)
    monster.draw_fixed_obs(win)
    pygame.display.update()


def print_text():
    score_p1 = font.render(m3 + ' ' + str(boy.score[0] // fps), True, c1)
    score_p2 = font.render(m4 + ' ' + str(boy.score[1] // fps), True, c1)
    tiime = font.render(m5 + ' ' + str(timing // fps), True, c1)
    win.blit(tiime, (scrwidth - tiime.get_width() -
                     5, scrheight - tiime.get_height() - 5))
    win.blit(score_p1, (0 + 5, scrheight - score_p1.get_height() - 5))
    win.blit(score_p2, (0 + 5, 0 + 10))


def paused():
    global pause
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.unpause()
                pause = False

        win.fill(c1)
        pase = font.render(m10, True, c4)
        win.blit(pase, (scrwidth / 2 - pase.get_width(),
                        scrheight / 2 - pase.get_height()))

        pygame.display.update()


partitionlist = []
for i in range(4):
    part = partition_height
    y = (i + 1) * (part + (scrheight - (no_of_partitions * part)) / 5) - 10
    partitionlist.append(y)

monster = FixObs(100, 120)
monster.change_obs()
monster.draw_fixed_obs(win)
cannon = []
boy = Player(scrwidth / 2, scrheight - 50 - 4, 50, 50)
boy.load_image()
ships = [MovingObj(0, 0, 0, 0, 0, 0) for i in range(5)]
ship_formation()
for i in range(4):
    cannon.append(
        Projectile(canx + 85, (i + 1) * (partition_height + river_height) -
                   10, 2, 10,
                   (i + 1) * (partition_height + river_height) - 50))
for i in range(4):
    cannon[i].image_load()

while run:
    timing -= 1
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pause = True
            pygame.mixer.pause()
            paused()

    boy.player_move()
    if (timing <= 0):
        win.fill(c1)
        tle = font.render(m9, True, c2)
        win.blit(tle, (scrwidth / 2 - tle.get_width() /
                       2, scrheight / 2 - tle.get_height() / 2))
        boy.change_player(win)

    if (
            boy.p2 and boy.playery + boy.playerheight / 2 > scrheight - 0.75 *
            partition_height) or (
            boy.p1 and boy.playery + boy.playerheight < partition_height + 10):
        if boy.p1:
            boy.score[0] += timing
            for i in range(5):
                ships[i].vel[0] = abs(ships[i].vel[0]) + 10
        else:
            boy.score[1] += timing
            for i in range(5):
                ships[i].vel[1] = abs(ships[i].vel[1]) + 10
        boy.go_to_win(win)
    build_background()

win.fill(c1)
if boy.score[0] > boy.score[1]:
    winnerr = font.render(m6, True, c2)
elif boy.score[1] > boy.score[0]:
    winnerr = font.render(m7, True, c2)
else:
    winnerr = font.render(m8, True, c2)

win.blit(winnerr, (scrwidth / 2 - winnerr.get_width() /
                   2, scrheight / 2 - winnerr.get_height() / 2))
pygame.display.update()
pygame.time.wait(1500)
pygame.quit()
