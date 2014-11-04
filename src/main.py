#!/usr/bin/env python2
# vim: set fileencoding=utf-8

import os.path
import sys
from math import ceil

import pygame

class Entity(object):
    def __init__(self, x, y, max_x, max_y, img = None):
        """
        Initializes the Entity instance. Arguments:
        x     = The initial x coordinate of the Entity
        y     = The initial y coordinate of the Entity
        max_x = The maximum x coordinate the Entity can go to
        max_y = The maximum y coordinate the Entity can go to
        img   = A pygame.Surface containing the image for the Entity.
                Defaults to None. Can be changed later.
        """
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        self.img = img

    def up(self):
        """Moves the Entity up."""
        if self.y == 0:
            return
        self.y -= 10

    def down(self):
        """Moves the Entity down."""
        if self.y == self.max_y:
            return
        self.y += 10

    def render(self, surface):
        """Blits the Entity on `surface`."""
        surface.blit(self.img, (self.x, self.y))

class Player(Entity):

    def __init__(self, *args):
        """
        Initializes the Player instance. Arguments:
        x     = The initial x coordinate of the Player
        y     = The initial y coordinate of the Player
        max_x = The maximum x coordinate the Player can go to
        max_y = The maximum y coordinate the Player can go to
        img   = A pygame.Surface containing the image for the Player.
                Defaults to None. Can be changed later.
        """
        super(Player, self).__init__(*args)

    def accelerate(self):
        """Accelerates the Player."""
        if self.x == self.max_x:
            return
        self.x += 5

    def decelerate(self):
        """Decelerates the Player."""
        if self.x == 0:
            return
        self.x -= 5

class Deer(Entity):
    def __init__(self, move_type, *args):
        """
        Initializes the Deer instance. Arguments:
        move_type = The movement type. See Deer.move().
        x         = The initial x coordinate of the Deer
        y         = The initial y coordinate of the Deer
        max_x     = The maximum x coordinate the Deer can go to
        max_y     = The maximum y coordinate the Deer can go to
        img       = A pygame.Surface containing the image for the Deer.
                    Defaults to None. Can be changed later.
        """
        self.move_type = move_type
        super(Deer, self).__init(*args)

    def move(self):
        """
        Moves the Deer according to its move_type. The movements are:
        0 = No movement
        1 = walks continually up
        2 = Walks continually down
        3 = Like 1, but aims for player's car at spawn time
        4 = Like 2, but aims for player's car at spawn time

        """
        pass

class Game(object):
    def __init__(self, width=800, height=600):
        """
        Initializes the Game instance. Arguments:
        width      = window width
        height     = window height
        """
        # Initialisierung
        self.width = width
        self.height = height

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Passée")
        pygame.mouse.set_visible(1)

        self.player = Player(0, self.height // 2, self.width, self.height)
        self.deer = []

        # Tastendruck wiederholt senden, falls nicht losgelassen
        pygame.key.set_repeat(1, 30)
        self.clock = pygame.time.Clock()
        self.running = False
        self.speed = 10

    def set_street_img(self, path):
        img = pygame.image.load(path)
        img = img.convert()
        self.street_img = img

        self.scaled_street = self.scale_street_img()

    def scale_street_img(self):
        width = self.street_img.get_width()
        height = self.street_img.get_height()
        scale = height // self.height
        img = pygame.transform.scale(self.street_img,
                (width // scale, self.height))
        return img

    def get_street_img(self, pos):
        surf = pygame.Surface((self.width, self.height))
        for x in range(-pos, self.width, self.scaled_street.get_width()):
            surf.blit(self.scaled_street, (x, 0))
        return surf

    def set_player_img(self, path):
        img = pygame.image.load(path)
        img = img.convert_alpha()
        scale = img.get_height() / (self.height / 5.0)
        img = pygame.transform.scale(img, (int(round(img.get_width() / scale)),
            int(round(img.get_height() / scale))))
        self.player.img = img

    def set_deer_img(self, path):
        img = pygame.image.load(path)
        img = img.convert_alpha()
        self.deer_img = img
        for i in self.deer:
            i.img = self.deer_img

    def run(self):
        self.running = True
        pos = 0
        while self.running:
            self.clock.tick(30)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.player.accelerate()
            else:
                self.player.decelerate()
            if keys[pygame.K_LEFT]:
                self.player.decelerate()
            if keys[pygame.K_UP]:
                self.player.up()
            if keys[pygame.K_DOWN]:
                self.player.down()
            if keys[pygame.K_ESCAPE]:
                sys.exit()

            pos += self.speed
            pos %= self.scaled_street.get_width()
            self.screen.blit(self.get_street_img(pos), (0, 0))

            self.player.render(self.screen)

            #pygame.draw.polygon(self.screen, (120, 120, 120), self.street)

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.set_player_img(os.path.join("img", "voiture_r2.png"))
    game.set_street_img(os.path.join("img", "rue_n_clip.png"))
    game.run()
