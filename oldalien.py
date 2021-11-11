#!/usr/bin/env python

"""This is a much simpler version of the aliens.py
example. It makes a good place for beginners to get
used to the way pygame works. Gameplay is pretty similar,
but there are a lot less object types to worry about,
and it makes no attempt at using the optional pygame
modules.
It does provide a good method for using the updaterects
to only update the changed parts of the screen, instead of
the entire screen surface. This has large speed benefits
and should be used whenever the fullscreen isn't being changed."""

# import
import random, os.path, sys
import pygame
import math
from pygame.locals import *

if not pygame.image.get_extended():
    raise SystemExit("Requires the extended ima ge loading from SDL_image")

# constants
FRAMES_PER_SEC = 40
PLAYER_SPEED = 12
MAX_SHOTS = 2
SHOT_SPEED = 10
ALIEN_SPEED = 12
ALIEN_ODDS = 45
EXPLODE_TIME = 6
SCORE = 0
SCREENRECT = Rect(0, 0, 640, 480)
ANGLE_DIFF = 10
IMAGES = []

# some globals for friendly access
dirtyrects = []  # list of update_rects
next_tick = 0  # used for timing


class Img: pass  # container for images


main_dir = os.path.split(os.path.abspath(__file__))[0]  # Program's diretory


# first, we define some utility functions

def load_image(file, transparent):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)
    return surface.convert()

class dummysound:
    def play(self): pass

def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()


# The logic for all the different sprite types

class Actor:
    "An enhanced sort of sprite class"

    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    def update(self):
        "update the sprite state for this frame"
        pass

    def draw(self, screen):
        "draws the sprite into the screen"
        r = screen.blit(self.image, self.rect)
        dirtyrects.append(r)

    def erase(self, screen, background):
        "gets the sprite off of the screen"
        r = screen.blit(background, self.rect, self.rect)
        dirtyrects.append(r)


class Player(Actor):
    "Cheer for our hero"

    def __init__(self):
        Actor.__init__(self, Img.player)
        self.alive = 1
        self.reloading = 0
        self.rect.centerx = SCREENRECT.centerx
        self.rect.bottom = SCREENRECT.bottom - 10

    def move(self, direction):
        self.rect = self.rect.move(direction * PLAYER_SPEED, 0).clamp(SCREENRECT)


class Alien(Actor):
    "Destroy him or suffer"

    def __init__(self):
        Actor.__init__(self, Img.alien)
        self.facing = random.choice((-1, 1)) * ALIEN_SPEED
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        global SCREENRECT
        self.rect[0] = self.rect[0] + self.facing
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing;
            self.rect.top = self.rect.bottom + 3
            self.rect = self.rect.clamp(SCREENRECT)


class Explosion(Actor):
    "Beware the fury"

    def __init__(self, actor):
        Actor.__init__(self, Img.explosion)
        self.life = EXPLODE_TIME
        self.rect.center = actor.rect.center

    def update(self):
        self.life = self.life - 1


class Shot(Actor):
    "The big payload"

    def __init__(self, player, angle):
        Actor.__init__(self, Img.shot)
        global IMAGES
        self.image = IMAGES[angle//ANGLE_DIFF]
        self.rect = self.image.get_rect()

        self.velocity_x = math.cos(math.radians(-angle)) * SHOT_SPEED
        self.velocity_y = math.sin(math.radians(-angle)) * SHOT_SPEED

        self.pos = list(player.rect.center)
        self.rect.centerx = player.rect.centerx
        self.rect.top = player.rect.top - 10


    def update(self):
        self.pos[0] += self.velocity_x
        self.pos[1] += self.velocity_y

        self.rect.center = self.pos
        self.rect.top = self.rect.top-SHOT_SPEED

class Score(Actor):
    def __init__(self, screen, background):
        self.font = pygame.font.Font(None, 20)
        self.text = self.font.render(str(SCORE),1,(255,255,255))
        Actor.__init__(self, self.text)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        self.rect = self.image.get_rect().move(10, 450)
        self.update(screen, background)

    def update(self, screen, background):
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            textRect = self.rect
            if (self.lastscore%4 == 0):
                textRect.center = (SCREENRECT[2] + 18, SCREENRECT[1] + 18)
            elif (self.lastscore%4 == 1):
                textRect.center = (SCREENRECT[0] + 18, SCREENRECT[1] + 18)
            elif (self.lastscore%4== 2):
                textRect.center = (SCREENRECT[0] + 18, SCREENRECT[3] - 30)
            else:
                textRect.center = (SCREENRECT[2] - 30, SCREENRECT[3] - 30)
            self.image = self.font.render(msg, 0, self.color)
            self.rect = textRect
            self.erase(screen, background)
            r = screen.blit(self.image, self.rect)
            dirtyrects.append(r)
#
# class Score(Actor):
#     def __init__(self,score,font):
#         self.score = score
#         self.font = font
#         self.text = font.render(str(score),1,(255,255,255))
#         Actor.__init__(self, self.text)
#
#     def update(self, screen):
#         self.score+=1
#         self.text = self.font.render(str(self.score), True, (255, 255, 255))
#         textRect = self.rect
#         res =self.score%4
#         if(res == 0):
#             textRect.center = (18, 18)
#         elif(res == 1):
#             textRect.center = (18, SCREENRECT[3]-18)
#         elif(res == 2):
#             textRect.center = (SCREENRECT[2] - 18, SCREENRECT[3] - 18)
#         else:
#             textRect.center = (SCREENRECT[2] - 18, 18)
#         t = screen.blit(self.text, textRect)
#         self.rect = self.rect.clamp(SCREENRECT)
#         dirtyrects.append(t)

def crash():
    crash_sound = pygame.mixer.Sound("crash.wav")
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

def main():
    "Run me for adrenaline"
    global dirtyrects
    global ANGLE_DIFF
    global IMAGES
    global SCORE

    # Initialize SDL components
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size, 0)
    clock = pygame.time.Clock()

    # Load the Resources
    Img.background = load_image('background.gif', 0)
    Img.shot = load_image('shot.gif', 1)
    Img.bomb = load_image('bomb.gif', 1)
    Img.danger = load_image('danger.gif', 1)
    Img.alien = load_image('alien1.gif', 1)
    Img.player = load_image('oldplayer.gif', 1)
    Img.explosion = load_image('explosion1.gif', 1)

    for i in range(180//ANGLE_DIFF + 2):
       IMAGES.append(pygame.transform.rotate(Img.shot, i*ANGLE_DIFF - 90))

    # Create the background
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, Img.background.get_width()):
        background.blit(Img.background, (x, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialize Game Actors
    player = Player()
    aliens = [Alien()]
    shots = []
    explosions = []
    score = 0
    angle = 90
    boom_sound = load_sound('boom.wav')
    score_obj = Score(screen, background)

    # Main loop
    while player.alive or explosions:
        clock.tick(FRAMES_PER_SEC)

        # Gather Events
        pygame.event.pump()
        keystate = pygame.key.get_pressed()
        if keystate[K_ESCAPE] or pygame.event.peek(QUIT):
            break

        # Clear screen and update actors
        for actor in [player] + aliens + shots + explosions:
            actor.erase(screen, background)
            actor.update()

        # Clean Dead Explosions and Bullets
        for e in explosions:
            if e.life <= 0:
                explosions.remove(e)
        for s in shots:
            if s.rect.top <= 0:
                shots.remove(s)

        # Move the player
        direction = keystate[K_r] - keystate[K_l]
        player.move(direction)

        # Move the angle
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT and ANGLE_DIFF+angle<=180:  angle += ANGLE_DIFF
                if event.key == K_RIGHT and 0<=angle-ANGLE_DIFF: angle -= ANGLE_DIFF

        # Create new shots
        if not player.reloading and keystate[K_SPACE] and len(shots) < MAX_SHOTS:
            shots.append(Shot(player, angle))
        player.reloading = keystate[K_SPACE]

        # Create new alien
        if not int(random.random() * ALIEN_ODDS):
            aliens.append(Alien())

        # Detect collisions
        alienrects = []
        for a in aliens:
            alienrects.append(a.rect)

        hit = player.rect.collidelist(alienrects)
        if hit != -1:
            alien = aliens[hit]
            explosions.append(Explosion(alien))
            explosions.append(Explosion(player))
            aliens.remove(alien)
            player.alive = 0

        pygame.display.update(dirtyrects)
        for shot in shots:
            hit = shot.rect.collidelist(alienrects)
            if hit != -1:
                boom_sound.play()
                alien = aliens[hit]
                explosions.append(Explosion(alien))
                shots.remove(shot)
                aliens.remove(alien)
                SCORE += 1
                score_obj.update(screen, background)
                break

        # Draw everybody
        for actor in [player] + aliens + shots + explosions:
            actor.draw(screen)

        pygame.display.update(dirtyrects)
        dirtyrects = []

    pygame.time.wait(50)


# if python says run, let's run!
if __name__ == '__main__':
    main()
