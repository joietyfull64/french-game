# !/usr/bin/env python2
# vim: set fileencoding=utf-8

import os.path
import sys
import math
import webbrowser

# I suggest that we declare all instance variables in the constructor

import pygame


class GameData:

    second = 30
    playAsEmail = True
    
    width = 1200  # only for the gameplay
    height = 800
    bounds = (0,-0,0,-0)  # up, down, left, right; determines the smallest possible distance from the player to the street edge
    deer_vertical_speed = (height+bounds[0]+bounds[1])/(second*2)  # used for Deer.move()
    screen = pygame.display.set_mode((width, height))
    game_speed = 300//second
    car_speed = 0
    
    player = None
    deer = []
    
    scaled_street = None
    scaled_street2 = None
    startmenu_img = None
    startmenu2_img = None
    control_img = None
    player_img = None
    player_img2 = None
    deer_imgs = None
    virus_imgs = None
    logo_imgs = None
    graphics = None


class Player:

    def __init__(self, x=GameData.bounds[2], y=None):
        """Initializes the Player GameData. Arguments:
        x     = The initial x coordinate of the Player
        y     = The initial y coordinate of the Player
        img   = The player's image
        """
        self.x = x
        self.y = y
        if self.y is None: self.y = GameData.screen.get_height()//2
        self.speed_y = GameData.height//GameData.second
        self.speed_x = (GameData.width // 2)//GameData.second  # I made it double as fast as before
        self.boost = False  # mehr dazu: unterer Kommentar
        self.boost_factor = 2.0  # when space is pressed, the movement will be faster by this factor

    def hitbox(self):
        return GameData.player_img.get_rect().move(self.x, self.y)

    def up(self):
        """Moves the Player up."""
        if self.hitbox().top > GameData.screen.get_rect().top+GameData.bounds[0]:
            GameData.car_speed -= self.speed_y if not self.boost else self.speed_y*self.boost_factor
            self.y -= GameData.car_speed

    def down(self):
        """Moves the Player down."""
        if self.hitbox().bottom < GameData.screen.get_rect().bottom+GameData.bounds[1]:
            GameData.car_speed += self.speed_y if not self.boost else self.speed_y*self.boost_factor
            self.x += GameData.car_speed

    def accelerate(self):
        """Accelerates the Player."""
        if self.hitbox().right < GameData.screen.get_rect().right+GameData.bounds[3]:
            GameData.car_speed += self.speed_x if not self.boost else self.speed_y*self.boost_factor
            self.x += GameData.car_speed

    def decelerate(self):
        """Decelerates the Player."""
        if self.hitbox().left > GameData.screen.get_rect().left+GameData.bounds[2]:
            GameData.car_speed -= self.speed_x if not self.boost else self.speed_x*self.boost_factor
            self.x -= GameData.car_speed

    def render(self, surface):
        """Blits the Player on 'surface'."""
        img = GameData.player_img
        if GameData.playAsEmail: img = GameData.player_img2
        surface.blit(img, self.hitbox())


class Deer:

    # the x and y coordinate will be set randomly
    def __init__(self, move_type):
        """Initializes the Deer GameData. Arguments:
        move_type = The movement type. See Deer.move().
        imgs = a tuple of images whose elementary images are switched
        """
        self.move_type = move_type
        self.__img = -1  # animation index, -1 weil wir vor jedem Anzeigen zuerst diese Variable erhöhen
        self.__key_frame = -1  # wir sind dann mal doch nicht zu faul eine neue Variable zu erstellen
                   # die Frame-Nummer der Animation
        self.__angle = 0  # the angle after which the, by default vertical, image is rotated counterclockwise

        self.x = 0
        self.y = 0
        self.__speed_x = 0  # we need it for movment_type 8 & 9
        self.__speed_y = 0  # we need it for movement_type 4 & 5
        # self.hitbox = self.hitbox()  # instead of self.hitbox use self.hitbox()
        self.__longest_img_width = GameData.deer_imgs[0].get_width()  # benutzt in is_away() und hier drunter
        self.__longest_img_height = GameData.deer_imgs[0].get_height()
        if not self.move_type == 0:
            for i in GameData.deer_imgs:
                if i.get_width() > self.__longest_img_width:
                    self.__longest_img_width = i.get_width()
                if i.get_height() > self.__longest_img_height:
                    self.__longest_img_height = i.get_height()

        # start positions of the move_types and picture angle calculations
        g = instance
        self.__angle = -90
        if self.move_type == 2:
            self.x = g.width()
            self.y = randint(g.height()//2, g.height()+g.bounds[1]-self.__longest_img_height)
            self.__angle += math.tan(g.game_speed // g.vertical_deer_speed)
        elif self.move_type == 3:
            self.x = g.width()
            self.y = randint(g.bounds[0], g.screen()//2-self.__longest_img_height)
            self.__angle -= math.tan(g.game_speed // g.vertical_deer_speed)
        elif self.move_type == 4:
            self.x = g.width()
            self.y = randint(g.player.y,g.height()-self.__longest_img_height+g.bounds[1])
            hitbox = self.hitbox()
            self.__speed_y = ((g.player.y+g.player.hitbox().height//2)-(self.y+hitbox.height//2)) // \
                           ((g.player.x+g.player.hitbox().width//2)-(self.x+hitbox.width//2))*g.game_speed
            self.__angle += math.tan(g.game_speed // self.__speed_y)  # self.__speed_y is always positive
        elif self.move_type == 5:
            self.x = g.width()
            self.y = randint(g.bounds[0], g.player.y+g.player.height-self.__longest_img_height)
            hitbox = self.hitbox()
            self.__speed_y = ((g.player.y+g.player.hitbox().height//2)-(self.y+hitbox.height//2)) // \
                           ((g.player.x+g.player.hitbox().width//2)-(self.x+hitbox.width//2))*g.game_speed
            self.__angle -= math.tan(g.game_speed // -self.__speed_y)
        elif self.move_type == 6:
            self.x = randint(g.bounds[2], g.width()+g.bounds[3]-self.__longest_img_width)
            self.y = -imgs[0].get_height()
            self.__angle = 0
        elif self.move_type == 8:
            self.x = randint(g.bounds[2], g.width()+g.bounds[3]-self.__longest_img_width)
            self.y = -imgs[0].get_height()
            hitbox = self.hitbox()
            self.__speed_x = ((g.player.x+g.player.hitbox().width//2)-(self.x+hitbox.width//2)) // \
                           ((g.player.y+g.player.hitbox().height//2)-(self.y+hitbox.height//2))*g.vertical_deer_speed
            self.__angle = (((self.__speed_x >> -1)^-1)|1)*math.tan(g.vertical_deer_speed // self.__speed_x)
        elif self.move_type == 7:
            self.x = randint(g.bounds[2], g.width()+g.bounds[3]-self.__longest_img_width)
            self.y = g.height()
            self.__angle = 180
        elif self.move_type == 9:
            self.x = randint(g.bounds[2], g.width()+g.bounds[3]-self.__longest_img_width)
            self.y = g.height()
            hitbox = self.hitbox()
            self.__speed_x = ((g.player.x+g.player.hitbox().width//2)-(self.x+hitbox.width//2)) // \
                           ((g.player.y+g.player.hitbox().height//2)-(self.y+hitbox.height//2))*g.vertical_deer_speed
            self.__angle = 180 + ((self.__speed_x >> -1)|1)*math.tan(g.vertical_deer_speed // self.__speed_x)
        else:  # 0 & 1 & 10 & 11
            gs = g.game_speed//2
            if self.move_type == 10:
                self.__speed_y = -g.vertical_deer_speed
                self.__angle += math.tan(gs // self.__speed_y)
            elif self.move_type == 11:
                self.__speed_y = g.vertical_deer_speed
                self.__angle -= math.tan(gs // self.__speed_y)
            elif not self.move_type == 1: self.__angle = 90
            self.x = g.width()
            self.y = randint(g.bounds[0], g.height()-self.__longest_img_height+g.bounds[1])

    def hitbox(self):
        """Returns the current hitbox for the current image"""
        img = GameData.deer_imgs[self.img]
        if not self.__angle == 0: img = pygame.transform.rotate(img, self.__angle)
        return img.get_rect().move(self.x, self.y)

    def move(self):
        """Moves the Deer according to its move_type. The movements are:
        0 = Moves to the left at Game.speed
        1 = Moves to the left at half Game.speed
        2 = Walks to the left and up
        3 = Walks to the left and down
        4 = Like 2, but aims for player's car at spawn time
        5 = Like 3, but aims for player's car at spawn time

        6 = moves up
        7 = moves down
        8 = moves up to the player
        9 = moves down to the player
        10 = moves left and meanwhile up and down
        11 = moves left and meanwhile down and up
        """
        # position changes for move_types
        g = instance
        # if self.move_type == 0 is at the end of the function
        if self.move_type == 1:
            self.x -= g.game_speed//2
        elif self.move_type == 2:
            self.x -= g.game_speed,
            self.y -= g.vertical_deer_speed
        elif self.move_type == 3:
            self.x -= g.game_speed,
            self.y += g.vertical_deer_speed
        elif self.move_type == 4:
            self.x -= g.game_speed,
            self.y += self.__speed_y
        elif self.move_type == 5:
            self.x -= g.game_speed,
            self.y += self.__speed_y
        elif self.move_type == 6:
            self.y -= g.vertical_deer_speed
        elif self.move_type == 7:
            self.y += g.vertical_deer_speed
        elif self.move_type == 8:
            self.x += self.__speed_x
            self.y -= g.vertical_deer_speed
        elif self.move_type == 9:
            self.x += self.__speed_x
            self.y += g.vertical_deer_speed
        elif self.move_type == 10 or self.move_type == 11:
            self.x += g.game_speed//2
            if (self.__speed_y < 0 and self.y <= g.bounds[0]) or \
               (self.__speed_y > 0 and self.y >= g.height()-g.bounds[1]-self.hitbox().height):
                self.__speed_y *= -1
                self.__angle -= 90  # if running towards car: = 90 - self.__angle
                self.__angle *= 2
            else:
                self.y += self.__speed_y
        else: # 0 & others
            self.x -= g.game_speed
#       print "MOVED %s" % self.hitbox

    # obsolete - use set_deer_image instead
    # def set_imgs(self, imgs, x = self.x, y = self.y):
    #    """Sets the image of the Deer. Argument:
    #        imgs = List of 'pygame.Surface's containing the image for the Enity.
    #        x    = the new x coordinate of the upper left corner
    #        y    = the new y coordinate of the upper right corner
    #    """
    #    GameData.deer_imgs = imgs
    #    self.x = x
    #    self.y = y

    def next_img(self):
        """Returns the next image in the animation"""
        if not GameData.playAsEmail:
            self.__img = 0 if self.__img >= len(GameData.deer_imgs)-1 else self.__img+1
            if move_type < 1 or move_type > 11:
                if not self.__angle == 0: return pygame.transform.rotate(GameData.deer_imgs[0], self.__angle)
                else: return GameData.deer_imgs[0]
            else:
                img = GameData.deer_imgs[self.__img]
                if not self.__angle == 0: return pygame.transform.rotate(img, self.__angle)
                else: return img
        else:
            # possibility 1 (easy):
            # if randint(0,1): return GameData.logo_imgs[self.__img]
            # else: return GameData.GameData.virus_imgs[self.__img]

            # possibility 2 (advanced - with compound animation):
            # #both images
            # logo = GameData.logo_imgs[self.__img]
            # virus = pygame.transform.rotate(GameData.virus_imgs[self.__img], self.__angle)
            # #variables
            # anim_len = GameData.second*2
            # width = logo.get_width()
            # if self.__key_frame == -1: self.__key_frame = randint(0,anim_len-1)
            # frame_unit = 2*width // anim_len
            # offset = self.__key_frame*frame_unit
            # #layers
            # img = pygame.transform.flip(logo, False, True).move(width-offset,0)
            # img.blit(virus,(0,0))
            # img.blit(logo, ((width+offset)%(2*width)-width,0))
            # #update non-temporary variables
            # self.__angle += int(round(360 // anim_len))
            # self.__key_frame += 1
            # self.__key_frame %= anim_len
            # return img

            # possibility 3 (advanced - creates a realistic cylindric rotation around the y-axis (mathemtical z-axis)):
            logo = GameData.logo_imgs[self.__img]
            virus = pygame.transform.rotate(GameData.virus_imgs[self.__img], self.__angle)
            # variables
            anim_len = GameData.second*2
            width = logo.get_width()
            radius = math.sqrt((width//2)**2 + (width//2)**2)
            if self.__key_frame == -1: self.__key_frame = randint(0,anim_len-1)
            frame_unit = radius*2*math.pi // anim_len
            offset = self.__key_frame*frame_unit  # Bogenmaß
            offset2 = offset+radius*(math.asin(0.5)//90*math.pi)  # angle*2//360*math.pi*2; width//2//width = 0.5
            # logo_angled_width = math.sqrt(width**2 - ((math.sin(float(offset)/radius)-math.sin(float(offset2)/radius))*radius)**2)  # even simpler:
            x_distance = math.cos(float(offset)/radius)*radius
            x_distance2 = math.cos(float(offset2)/radius)*radius
            logo_angled_width = x_distance-x_distance2
            # layers
            img = pygame.Surface((width, logo.get_height()))
            logo = pygame.transform.scale(logo, (abs(logo_angled_width), logo.get_height()))
            if logo_angled_width < 0:
                img.blit(pygame.transform.flip(logo, False, True), (x_distance2,0))
                img.blit(virus,(img.get_width()//2-virus.get_width()//2,img.get_height()//2-virus.get_height()//2))
            else:
                img.blit(virus,(img.get_width()//2-virus.get_width()//2,img.get_height()//2-virus.get_height()//2))
                img.blit(logo, (x_distance,0))
            # update non-temporary variables
            self.__angle += 360 // anim_len
            self.__key_frame += 1
            self.__key_frame %= anim_len
            return img

    def render(self, surface):
        # habe next_img() gleich hier benutzt
        """Blits the Deer on 'surface'."""
        surface.blit(self.next_img(), self.hitbox())

    def is_away(self):
        screen = GameData.screen
        return self.x < -self.__longest_img_width or self.x > screen.get_width() or \
               self.y < -self.__longest_img_height or self.y > screen.get_height()


class Game:
    """Weitere optionale Ideen zum Einbauen:
        - eine besondere Farbe für Rehe verschiedener move_typen
        - Autos auf der Gegenspur"""

    # is needed to call instance variables with other classes' methods
    #second = 30
    #playAsEmail = True
    img_path = "C:\\Users\\ChristophEhmendörfer\\Documents\\Schule\\Anderes für die Schule\\video game frz\\"  # only for debug

    def __init__(self, width=1200, height=800):
        """
        Initializes the Game GameData. Arguments:
        width      = window width
        height     = window height
        """
        # Initialisierung
        GameData.width = width
        GameData.height = height
        self.__startmenu = False
        self.__pause = False
        self.__game_over = False
        self.__restart = False
        self.__survived_deer = 0
        self.__pos = 0  # street offset

        pygame.init()
        pygame.display.set_caption("Passée")
        pygame.mouse.set_visible(1)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION,
                                  pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
        GameData.player = Player()

        self.__next_deer = GameData.second
        self.__next_deer_max = GameData.second*3
        self.__next_deer_min = GameData.second*7/3

        # I think, this creates a better overview

        self.__time = 0.0
        self.__clock = pygame.time.Clock()
        self.__running = False

        # Tastendruck wiederholt senden, falls nicht losgelassen
        delay = int(round(1000.0/GameData.second))
        pygame.key.set_repeat(delay, delay)

    # def height(self):
    #     """Returns the gameplay screen height"""
    #     return self.__height
    # 
    # def width(self):
    #     """Returns the gameplay screen width"""
    #     return self.__width
    # 
    # def screen(self):
    #     """Returns the currently shown image"""
    #     return self.__screen

    def reset_game_scene(self):
        """Resets all options and restarts the game."""
        # instance = Game()  # this only works, if this method and run() are staticmethods; begins always with startmenu
        GameData.player = Player()
        GameData.deer = []
        self.__survived_deer = 0
        self.__startmenu = False
        self.__pause = False
        self.__game_over = False
        GameData.game_speed = 300//GameData.second
        GameData.car_speed = 0
        self.__pos = 0
        self.__next_deer = GameData.second
        self.__next_deer_max = GameData.second*3
        self.__next_deer_min = GameData.second*7/3
        self.__time = 0.0
        self.__running = False
        self.__restart = True  # will restart run()
        GameData.screen = pygame.display.set_mode((GameData.width, GameData.height))
        # self.__clock = pygame.time.Clock()

    def return_to_menu(self):
        self.__startmenu = True
        self.__pause = False
        self.__game_over = False
        img = GameData.startmenu_img
        if GameData.playAsEmail: img = GameData.startmenu2_img
        GameData.screen = pygame.display.set_mode((img.get_width(), img.get_height()))

    def create_frame(self, surface):
        """Draws onto the given Surface object."""
        # draw background
        surface.fill(pygame.Color(0, 0, 0, 255))
        self.__pos += GameData.game_speed
        self.__pos %= GameData.scaled_street.get_width()
        surface.blit(Game.get_street_img(self.__pos), (0, 0))
        # draw player
        GameData.player.render(surface)
        # draw deer
        for deer in GameData.deer:
            deer.render(GameData.screen)
        # draw stats (score, time (with tenth seconds))
            # spawned_deer
            # time
            # start or pause sign (optional)
            speed = int(round((GameData.game_speed + GameData.car_speed)*GameData.second//(GameData.player_img.get_width()/4.5)*3.6))  # speed

    def create_pause_frame(self, surface):
        """Displays the pause menu on the given Surface object."""
        self.create_frame(surface)
        surface.blit(surface.fill(pygame.Color(0,0,0,255)).set_alpha(102), (0,0))
        img = GameData.graphics["pause_vi.png"]
        surface.blit(img, (GameData.width//2 - img.get_width()//2, GameData.height//2 - img.get_height()//2))

    def create_game_over_frame(self, surface):
        """Draws the Game Over screen on the given Surface object."""
        self.create_frame(surface)
        surface.blit(surface.fill(pygame.Color(0,0,0,255)).set_alpha(102), (0,0))
        img = GameData.graphics["termine.png"]
        surface.blit(img, (GameData.width//2 - img.get_width()//2, GameData.height//2 - img.get_height()//2))

    def create_start_menu_frame(self, surface):
        """Paints the starting screen on the Surface object."""
        img = GameData.startmenu_img
        if GameData.playAsEmail: img = GameData.startmenu2_img
        surface.blit(img, (0,0))

    def render_controls(self, surface, clicked_checkbox=False):
        """Displays controls on a start menu of a Surface object."""
        vec2d = (GameData.width//2 - GameData.control_img.get_width()//2,
                                        GameData.height//2 - GameData.control_img.get_height()//2)
        surface.blit(GameData.control_img, vec2d)
        if clicked_checkbox: GameData.playAsEmail = not GameData.playAsEmail
        if not GameData.playAsEmail: surface.blit(GameData.graphics["checkbox_checked.png"], (650+vec2d[0], 223+vec2d[1]))  # quite unprofessional yet

    @staticmethod
    def load_graphics():
        """Gets all needed graphics and puts them in one variable."""
        Game.set_street_img(Game.path("rue_n_clip.png"), Game.path("rue_matrix_clip.png"))
        Game.set_player_img(Game.path("voiture_r2.png"), Game.path("email_g.png"))
        Game.set_deer_img([Game.path("chevreuil_m_gif%i.png" % i) for i in (1, 2, 3, 2)])
        service_colours = ["b", "r", "v", "vi"]
        service_lexicon = dict(zip(service_colours, ["NSA", "BND", "GCHQ", "DGSE"]))
        Game.set_secret_service_imgs(service_colours, [Game.path("virus_%s.png" % i) for i in service_colours],
                                            [Game.path("%s_%s.png" % (service_lexicon[k], k)) for k in service_lexicon])
        Game.set_images([int(round(GameData.height//3*2)), int(round(float(226/4)*3)), None, None],
                            "allez.png", "termine.png", "checkbox_checked.png", "pause_vi.png")
        bar_height = 200
        bar = [[pygame.Surface((320, bar_height)), pygame.Surface((340, bar_height)),
                pygame.Surface((117, bar_height))] for i in range(2)]
        for b in range(len(bar)):
            lastwidth = 0
            for part in range(len(bar[b])):
                pathname = Game.path("barre_d'etat_%s.png" % ("g" if b % 2 == 0 else "n")) # removed accent aigue because files are encoded with Unicode
                bar[b][part].blit(pygame.image.load(pathname).convert_alpha(), (-lastwidth,0))
                lastwidth += bar[b][part].get_width()
                GameData.graphics.update(dict(zip(pathname[:-4]+("%d.png" % part),
                                                  [Game.scale(bar[b][part], GameData.height//8)])) )
        GameData.startmenu_img = Game.scale(pygame.image.load(Game.path("chevreuil_morte.jpg")).convert(),
                                                GameData.height)
        GameData.startmenu2_img = Game.scale(pygame.image.load(Game.path("premier_ecran.jpg")).convert(), GameData.height) # with unicode file name image open problem
        GameData.control_img = pygame.image.load(Game.path("tableau_de_controle.png")).convert_alpha() # hello unicode!

    # Road Adjustment
    @staticmethod
    def set_street_img(path, path2=None):
        if not path2: path2 = path
        img = pygame.image.load(path).convert()
        img2 = pygame.image.load(path2).convert()
        # self.street_img # we don't need it anymore
        GameData.scaled_street = Game.scale(img, GameData.height)
        GameData.scaled_street2 = Game.scale(img2, GameData.height)

    @staticmethod
    def get_street_img(offset, matrix_style = True):
        surf = pygame.Surface((GameData.width, GameData.height))
        street = GameData.scaled_street if not matrix_style else GameData.scaled_street2
        for x in range(-offset, GameData.width, street.get_width()):
            surf.blit(street, (x, 0))
        return surf

    # player presentation
    @staticmethod
    def set_player_img(path, path2=None):
        if path2 is None: path2 = path
        img = pygame.image.load(path).convert_alpha()
        img2 = pygame.image.load(path2).convert_alpha()
        GameData.player_img = Game.scale(img, GameData.height // 5)
        GameData.player_img2 = Game.scale(img2, GameData.height // 5)

    # obstacle presentation
    @staticmethod
    def set_deer_img(paths):
        imgs = [pygame.image.load(path).convert_alpha() for path in paths]
        GameData.deer_imgs = Game.scale_list(imgs, GameData.height // 5)

    @staticmethod
    def set_secret_service_imgs(keys, logo_paths, virus_paths):
        """Arg0 = key names for the images from both path lists
           Arg1 = the list of paths for the secret service images
           Arg2 = the list of paths for the virus images"""
        imgs = [pygame.image.load(path).convert_alpha() for path in logo_paths]
        logo_imgs = dict(zip(keys, imgs))
        GameData.logo_imgs = Game.scale_list(imgs, GameData.height//5)
        imgs = [pygame.image.load(path).convert_alpha() for path in virus_paths]
        virus_imgs = dict(zip(keys, imgs))
        GameData.virus_imgs = Game.scale_list(imgs, GameData.height//5)

    # other graphical presentation
    @staticmethod
    def scale(img, rel_height):
        return pygame.transform.scale(img, (int(round(float(img.get_width()) / img.get_height() * rel_height)),
                                            rel_height))

    @staticmethod
    def scale_list(imgs, rel_heights=-1):
        """Takes a list/tuple of images and a list/tuple of target heights and
        returns the corresponding resized Surface objects and the widths."""
        if imgs is None or rel_heights is None: return None
        if rel_heights < 0 or (not isinstance(rel_heights, list) and not isinstance(rel_heights, tuple)):
            rel_heights = [GameData.height for i in range(len(imgs))]
        lst = len(imgs) if not len(imgs) > len(rel_heights) else len(rel_heights)
        widths = [int(round(float(imgs[i].get_width()) * (rel_heights[i] if not rel_heights[i] is None
                                else imgs[i].get_height()) / imgs[i].get_height())) for i in range(lst)]
        return [(imgs[i] if rel_heights[i] is None else pygame.transform.scale(imgs[i], (widths[i],
                        (rel_heights[i] if not rel_heights[i] < 0 else GameData.height) ))) for i in range(lst)]

    @staticmethod
    def scale_width(img, height):
        return img.get_width()//img.get_height()*height

    @staticmethod
    def scale_height(img, width):
        return img.get_height()//img.get_width()*width

    @staticmethod
    def set_images(heights, *paths):
        path_s = [Game.path(path) for path in paths]
        imgs = [pygame.image.load(path).convert_alpha() for path in path_s]
        imgs = Game.scale_list(imgs, heights)
        GameData.graphics = dict(zip(paths, imgs))

    @staticmethod
    def spawn_deer(self):
        # if randint(0, 1):  # we already have a random spawn time in run() and a spawn limit
        move_type = 0
        # I think, this solution is a bit too complicated:
        # if GameData.game_speed < 20:
        #    move_type = randint(0, 2)
        # elif GameData.game_speed < 30:
        #    move_type = randint(0, 4)
        # else:
        #    move_type = randint(0, 11)
        # I would do it like this:
        n = 23
        mt = randint(0, n)
        p = [3, 3, 2, 2, 1, 1]  # probabilites, repeated to 12 elements, all elements' sum must be n+1
        for i in range(1,12):
            n -= p[i%len(p)]
            if mt > n:
                move_type = 1
        GameData.deer.append(Deer(move_type))

    # core function
    def run(self):
        render_controls = False
        intro = True
        # pos = 0  # it's easier to use an instance variable because I want to use it in dispatched functions
        tick = 0
        spawn_count = 0  # number of spawned deer
        maximum_count = 4  # more than 4 deer aren't allowed on the road
        maximum_speed = 50
        new_game = True
        self.__startmenu = False
        self.__time = 0.0
        GameData.car_speed = 0
        self.__running = True
        mouse_click = False
        while self.__running:
            self.__clock.tick(GameData.second)
            self.__time += 100.0/GameData.second
            #if round(self.__time, 2) - round(self.__time) == -0.01: self.__time = round(self.__time)
            mouse_click = False

            # EXIT CONDITION
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONUP:
                    mouse_click = True
            
            # PREPARE USER INPUT
            keys = pygame.key.get_pressed()  # I don't know if this was a good idea
            input_sum = sum(keys)-1

            # incomplete pygame.event code
            # pygame.event.pump()
            # input_sum = pygame.event.peek(pygame.event.get())

            # MODES
            if self.__startmenu:
                if render_controls:
                    # USER input
                    if mouse_click: GameData.playAsEmail = not GameData.playAsEmail
                    if input_sum:
                        render_controls = False
                    else: self.render_controls(GameData.screen)
                elif input_sum:
                    # USER input
                    if mouse_click: webbrowser.open_new_tab("http://goo.gl/yuXawT")
                    if keys[pygame.K_SPACE]:
                        render_controls = True
                    elif keys[pygame.K_ESCAPE]:
                        self.__running = False
                        break
                    else:
                        self.reset_game_scene()  # sets self.__startmenu = False
                self.create_start_menu_frame(GameData.screen)

            elif self.__game_over:
                # USER input
                if input_sum:
                    if keys[pygame.K_ESCAPE]: self.return_to_menu()
                    else: self.reset_game_scene()  # sets self.__game_over = False
                self.create_game_over_frame(GameData.screen)

            elif self.__pause:
                if render_controls:
                    # USER input
                    if mouse_click: GameData.playAsEmail = not GameData.playAsEmail
                    if input_sum:
                        render_controls = False
                    self.render_controls(GameData.screen)
                else:
                    self.create_pause_frame(GameData.screen)
                    # USER input
                    if input_sum:
                        if keys[pygame.K_SPACE]: render_controls = True
                        elif keys[pygame.K_KP_ENTER]: self.reset_game_scene()
                        else:
                            self.__pause = False
                            if keys[pygame.K_ESCAPE]:
                                self.return_to_menu()

            else:
                tick += 1
                GameData.car_speed = 0
                if not new_game:
                    # USER INPUT:
                    if keys[pygame.K_RIGHT]:
                        GameData.player.accelerate()
                    #else:
                        #GameData.player.decelerate()
                    if keys[pygame.K_LEFT]:  # brake
                        GameData.player.decelerate()
                    if keys[pygame.K_UP]:
                        GameData.player.up()
                    if keys[pygame.K_DOWN]:
                        GameData.player.down()
                    if keys[pygame.K_SPACE]:
                        GameData.player.boost = True # self.boost ist schon in accelerate() und decelerate() eingebaut
                    else: GameData.player.boost = False # WICHTIG
                    if keys[pygame.K_ESCAPE]:
                        self.__pause = True  # fänd ich gut, vielleicht kann man dann von dort beenden

                    # GAME routine
                    if tick % (GameData.second*2) == 0:
                        if self.__next_deer_max > GameData.second*2:
                            self.__next_deer_max -= 1
                        if self.__next_deer_min > GameData.second//4:
                            self.__next_deer_min -= 1
                    if tick % int(GameData.second*2.5) == 0 and GameData.game_speed < self.maximum_speed:
                        GameData.game_speed += 1
                        # for deer in GameData.deer:  # we don't need it anymore
                            # deer.game_speed = GameData.game_speed
                            # GameData.player.game_speed = GameData.game_speed

                    # SPAWN
                    if self.__next_deer == 0 and spawn_count < maximum_count:
                        Game.spawn_deer()
                        spawn_count += 1
                        self.__next_deer = randint(self.__next_deer_min, self.__next_deer_max)
                    else:
                        self.__next_deer -= 1

                    # self.__game_over = GameData.player.hasCrashed()
                    self.__game_over = GameData.player.hitbox().collidelist(GameData.deer)
                    for i in range(len(GameData.deer)):
                        deer = GameData.deer[i]
                        deer.move()
                        if deer.is_away():
                            GameData.deer.remove(i)
                            self.__survived_deer += 1
                            spawn_count -= 1

                # SETUP IMAGE BUFFER
                self.create_frame(GameData.screen)

                # INTRO
                if new_game:
                    allez = GameData.graphics["allez.png"]
                    GameData.screen.blit(allez, (GameData.width//2-allez.get_width()//2,
                                               GameData.height//2-allez.get_height()//2))
                    if tick % (GameData.second*2) == 0:
                        new_game = False

            # SHOW CONTENT
            pygame.display.flip()

        if not self.__restart:
            # FINISH IT!
            sys.exit()
        else: self.__restart = False

    @staticmethod
    def path(path):
        return os.path.join("img", path)
        # return os.path.join("img", path))

#instance = Game()  # we only can achieve this with a global variable


def main():
    game = Game()
    Game.load_graphics()
    while True:  # will leave run() and execute it again, if self.__restart == True
        game.run()

if __name__ == "__main__":
    main()
