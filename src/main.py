# !/usr/bin/env python2
# vim: set fileencoding=utf-8

import os.path
import sys
import webbrowser
import math
from random import randint

# I suggest that we declare all instance variables in the constructor

import pygame

#Bugs: return_to_start_menu(), bar_img, after texture change no obstacles will appear, Collisions of deer are too large


class GameData:

    second = 60
    tick = 0
    play_as_email = True
    
    width = 1200  # only for the gameplay
    height = 800
    bounds = (height//20,-height//20,width//20,-width//20)  # up, down, left, right; determines the smallest possible distance from the player to the street edge
    #deer_vertical_speed() = (height+bounds[0]+bounds[1])/(second*2)  # used for Deer.move()
    screen = None
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
    bar_img = None
    bar_img2 = None
    graphics = None

    @staticmethod
    def deer_vertical_speed():
        speed = GameData.game_speed//randint(2,8)
        return speed if speed < 30 else randint(10,20)  # if speed >= 3 else randint(5,10)



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
        img = GameData.player_img
        rect = img.get_rect()
        if GameData.play_as_email: rect = Game.scale(img, img.get_height()//5*(4 if GameData.play_as_email else 3)).get_rect()
        return rect.move(self.x+(img.get_width()-rect.width)//2, self.y+(img.get_height() - rect.height)//2)

    def up(self):
        """Moves the Player up."""
        if self.hitbox().top > GameData.screen.get_rect().top+GameData.bounds[0]:
            self.y -= self.speed_y if not self.boost else self.speed_y*self.boost_factor

    def down(self):
        """Moves the Player down."""
        if self.hitbox().bottom < GameData.screen.get_rect().bottom+GameData.bounds[1]:
            self.y += self.speed_y if not self.boost else self.speed_y*self.boost_factor

    def accelerate(self):
        """Accelerates the Player."""
        if self.hitbox().right < GameData.screen.get_rect().right+GameData.bounds[3]:
            GameData.car_speed += self.speed_x if not self.boost else self.speed_y*self.boost_factor
            self.x += GameData.car_speed

    def decelerate(self):
        """Decelerates the Player."""
        if self.hitbox().left > GameData.screen.get_rect().left+GameData.bounds[2]:
            GameData.car_speed -= self.speed_x if not self.boost else self.speed_x*self.boost_factor
            self.x += GameData.car_speed

    def render(self, surface):
        """Blits the Player on 'surface'."""
        img = GameData.player_img
        if GameData.play_as_email: img = GameData.player_img2
        surface.blit(img, self.hitbox())


class Deer:

    # the x and y coordinate will be set randomly
    def __init__(self, move_type):
        """Initializes the Deer GameData. Arguments:
        move_type = The movement type. See Deer.move().
        imgs = a tuple of images whose elementary images are switched
        """
        self.move_type = move_type
        #print move_type
        self.__img = 0  # animation index, -1 weil wir vor jedem Anzeigen zuerst diese Variable erhöhen
        if GameData.play_as_email: self.__img = randint(0,7)
        self.__key_frame = -1  # wir sind dann mal doch nicht zu faul eine neue Variable zu erstellen
                   # die Frame-Nummer der Animation

        self.x = 0
        self.y = 0
        self.__speed_x = 0
        self.__speed_y = 0

        self.__angle = 0  # the angle after which the, by default vertical, image is rotated counterclockwise
        self.setup_movement_type(move_type)

    def setup_movement_type(self, move_type):
        """start positions of the move_types and picture angle calculations"""
        #print GameData.width, GameData.height, GameData.bounds
        gs = GameData.game_speed
        gv = GameData.deer_vertical_speed()

        #speed and angle:
        hitbox = self.hitbox()
        if move_type == 1:
            self.__speed_x = gs//2
            self.__speed_y = 0
        elif move_type == 2 or move_type == 10:
            self.__speed_x = gs//2
            self.__speed_y = -gv
        elif move_type == 3 or move_type == 11:
            self.__speed_x = gs//2
            self.__speed_y = gv
        elif move_type <= 5:
            self.__speed_x = gs//2
            self.__speed_y = int(round(float((GameData.player.y+GameData.player.hitbox().height//2)-(self.y+hitbox.height//2)) /
                        ((GameData.player.x+GameData.player.hitbox().width//2)-(self.x+hitbox.width//2))*self.__speed_x))
            if move_type == 5: self.__speed_y *= -1
        elif move_type == 6:
            self.__speed_x = gs
            self.__speed_y = -gv
        elif move_type == 7:
            self.__speed_x = gs
            self.__speed_y = gv
        elif move_type <= 9:
            self.__speed_y = -gv if move_type == 8 else gv
            self.__speed_x = gs+int(round(float((GameData.player.x+GameData.player.hitbox().width//2)-(self.x+hitbox.width//2)) /
                    ((GameData.player.y+GameData.player.hitbox().height//2)-(self.y+hitbox.height//2))*self.__speed_y))
        else:
            self.__speed_x = 0
            self.__speed_y = 0
        if not GameData.play_as_email:
            if self.__speed_x or self.__speed_y:
                self.__angle = 90+int(round(math.acos(self.__speed_y / math.sqrt( # this avoids division by zero
                                        float(self.__speed_x)**2+float(self.__speed_y)**2))))
            else: self.__angle = 90
        else:
            self.__angle = 360
        self.__speed_x -= GameData.game_speed

        #start positions
        pl_img = GameData.player_img if not GameData.play_as_email else GameData.player_img2
        nt_img = self.next_img()
        if move_type == 2: # Moves to the left and up
            self.x = GameData.width
            self.y = randint(GameData.height//2, GameData.height+GameData.bounds[1]-nt_img.get_height())
        elif move_type == 3: # Moves to the left and down
            self.x = GameData.width
            rest = GameData.height//2-nt_img.get_height()
            bounds = GameData.bounds[0]
            self.y = randint(bounds, rest if rest >= bounds else bounds)
        elif move_type <= 5: # Moves to you from the left
            self.x = GameData.width
            rest = GameData.height-nt_img.get_height()+GameData.bounds[1]
            if move_type == 5: rest = GameData.player.y+pl_img.get_height()-nt_img.get_height()
            self.y = randint(GameData.player.y, rest if rest >= GameData.player.y else GameData.player.y)
        elif move_type <= 7: # Moves straight up
            if randint(0,1): self.x = GameData.player.x+pl_img.get_width()//2-nt_img.get_width()//2
            else:
                rest = GameData.width+GameData.bounds[3]-nt_img.get_width()
                bounds = GameData.bounds[2]
                self.x = randint(bounds, rest if rest >= bounds else bounds)
            self.y = GameData.height if move_type == 6 else -nt_img.get_height()
        elif move_type <= 9: # Moves to you from above
            rest = GameData.width+GameData.bounds[3]-nt_img.get_width()
            bounds = GameData.bounds[2]
            self.x = randint(bounds, rest if rest >= bounds else bounds)
            self.y = GameData.height if move_type == 8 else -nt_img.get_height()
        else: # stands relative to the road
            self.x = GameData.width
            if randint(0,1): self.y = GameData.player.y+pl_img.get_height()//2-nt_img.get_height()//2
            else:
                rest = GameData.height-nt_img.get_height()+GameData.bounds[1]
                bounds = GameData.bounds[0]
                self.y = randint(bounds, rest if rest >= bounds else bounds)

    def reset(self, move_type):
        self.move_type = move_type
        self.__img = 0  # animation index, -1 weil wir vor jedem Anzeigen zuerst diese Variable erhöhen
        if GameData.play_as_email: self.__img = randint(0,7)
        self.__key_frame = -1  # wir sind dann mal doch nicht zu faul eine neue Variable zu erstellen
                   # die Frame-Nummer der Animation
        self.setup_movement_type(move_type)

    def hitbox(self):
        """Returns the current hitbox for the current image"""
        img = self.next_img()
        if self.__angle: img = pygame.transform.rotate(img, self.__angle)
        rect = Game.scale(img, img.get_height()//5*3).get_rect()
        return rect.move(self.x+(img.get_width()-rect.width)//2, self.y+(img.get_height()-rect.height)//2)

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
        if self.move_type == 10 or self.move_type == 11:
            if not (self.__speed_y+self.y < 0 or self.__speed_y+self.y > GameData.height):
                self.y += self.__speed_y
            else:
                self.__speed_y = -self.__speed_y
                self.__angle = -self.__angle
        else:
            self.y += self.__speed_y
        self.x += self.__speed_x
        # # position changes for move_types
        # if self.move_type == 1:
        #     self.x -= GameData.game_speed//2
        # elif self.move_type == 2:
        #     self.x -= GameData.game_speed
        #     self.y -= GameData.deer_vertical_speed()
        # elif self.move_type == 3:
        #     self.x -= GameData.game_speed
        #     self.y += GameData.deer_vertical_speed()
        # elif self.move_type == 4:
        #     self.x -= GameData.game_speed
        #     self.y += self.__speed_y
        # elif self.move_type == 5:
        #     self.x -= GameData.game_speed
        #     self.y += self.__speed_y
        # elif self.move_type == 6:
        #     self.y -= GameData.deer_vertical_speed()
        # elif self.move_type == 7:
        #     self.y += GameData.deer_vertical_speed()
        # elif self.move_type == 8:
        #     self.x += self.__speed_x
        #     self.y -= GameData.deer_vertical_speed()
        # elif self.move_type == 9:
        #     self.x += self.__speed_x
        #     self.y += GameData.deer_vertical_speed()
        # elif self.move_type == 10 or self.move_type == 11:
        #     self.x += GameData.game_speed//2
        #     if (self.__speed_y < 0 and self.y <= GameData.bounds[0]) or \
        #        (self.__speed_y > 0 and self.y >= GameData.height-GameData.bounds[1]-self.hitbox().height):
        #         self.__speed_y *= -1
        #         if not GameData.play_as_email: self.__angle -= 90  # if running towards car: = 90 - self.__angle
        #         self.__angle *= 2
        #     else:
        #         self.y += self.__speed_y
        # else: # 0 & others
        #     self.x -= GameData.game_speed

    def next_img(self):
        """Returns the next image in the animation"""
        if not GameData.play_as_email:
            if GameData.tick % (GameData.second//6) == 0:
                if self.move_type < 1 or self.move_type > 11:
                    img = GameData.deer_imgs[self.__img%len(GameData.deer_imgs)]
                    if self.__angle: img = pygame.transform.rotate(img, self.__angle)
                    return img
                else:
                    self.__img += 1
                    return pygame.transform.rotate(GameData.deer_imgs[self.__img%len(GameData.deer_imgs)], self.__angle)
            else:
                img = GameData.deer_imgs[self.__img%len(GameData.deer_imgs)]  # in case we switch from matrix to street
                if self.__angle: img = pygame.transform.rotate(img, self.__angle)
                return img
        elif GameData.play_as_email:
            # possibility 1 (easy):
            img = GameData.virus_imgs[self.__img % 4]
            if self.__img / 4 == 0: img = GameData.logo_imgs[self.__img % 4]
            return pygame.transform.rotate(img, 5)
            #return img

            # # possibility 2 (advanced - with compound animation):
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
            # layer = pygame.transform.flip(logo, False, True)
            # img = pygame.Surface((layer.get_width(), layer.get_height()))
            # img.blit(layer, (width-offset, 0))
            # img.blit(virus,(0,0))
            # img.blit(logo, ((width+offset)%(2*width)-width,0))
            # #update non-temporary variables
            # self.__angle += int(round(360 // anim_len))
            # self.__key_frame += 1
            # self.__key_frame %= anim_len
            # return img

            # # possibility 3 (advanced - creates a realistic cylindric rotation around the y-axis (mathemtical z-axis)):
            # logo = GameData.logo_imgs[self.__img]
            # #virus = pygame.transform.rotate(GameData.virus_imgs[self.__img], self.__angle) # the rotation doesn't look good
            # virus = GameData.virus_imgs[self.__img]
            # # variables
            # anim_len = GameData.second*2
            # width = logo.get_width()
            # radius = math.sqrt((width//2)**2 * 2)
            # if self.__key_frame == -1: self.__key_frame = randint(0,anim_len-1)
            # frame_unit = radius*2*math.pi // anim_len
            # offset = self.__key_frame*frame_unit  # Bogenmaß
            # offset2 = offset+radius*(int(round(math.asin(0.5)/90*math.pi)))  # angle*2//360*math.pi*2; width//2//width = 0.5))
            # # logo_angled_width = math.sqrt(width**2 - ((int(round(math.sin(float(offset)/radius)-math.sin(float(offset2)/radius))*radius)**2)  # even simpler:))
            # x_distance = int(round(math.cos(float(offset)/radius)*radius))
            # x_distance2 = int(round(math.cos(float(offset2)/radius)*radius))
            # logo_angled_width = x_distance-x_distance2
            # # layers
            # img = pygame.Surface((width, logo.get_height()))
            # logo = pygame.transform.scale(logo, (int(abs(logo_angled_width)), logo.get_height()))
            # if logo_angled_width < 0:
            #     img.blit(pygame.transform.flip(logo, False, True), (x_distance2,0))
            #     img.blit(virus,(img.get_width()//2-virus.get_width()//2,img.get_height()//2-virus.get_height()//2))
            # else:
            #     img.blit(virus,(img.get_width()//2-virus.get_width()//2,img.get_height()//2-virus.get_height()//2))
            #     img.blit(logo, (x_distance,0))
            # # update non-temporary variables
            # #self.__angle += 360 // anim_len
            # self.__key_frame += 1
            # self.__key_frame %= anim_len
            # return img

    def render(self, surface):
        # habe next_img() gleich hier benutzt
        """Blits the Deer on 'surface'."""
        surface.blit(self.next_img(), self.hitbox())

    def is_away(self):
        screen = GameData.screen
        nt_img = self.next_img()
        return self.x < -nt_img.get_width() or self.x > screen.get_width() or \
               self.y < -nt_img.get_width() or self.y > screen.get_height()


class Game:
    """Weitere optionale Ideen zum Einbauen:
        - eine besondere Farbe für Rehe verschiedener move_typen
        - Autos auf der Gegenspur"""

    def __init__(self, width=1200, height=800):
        """
        Initializes the Game GameData. Arguments:
        width      = window width
        height     = window height
        """
        # Initialisierung
        GameData.width = width
        GameData.height = height
        self.__startmenu = True
        self.__pause = False
        self.__game_over = False
        self.__restart = False
        self.__survived_deer = 0
        self.__pos = 0  # street offset

        pygame.init()
        GameData.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Passée")
        pygame.mouse.set_visible(1)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION,
                                  pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])
        GameData.player = Player()

        self.__next_deer = GameData.second
        self.__next_deer_max = GameData.second*3
        self.__next_deer_min = GameData.second*7/3

        # I think, this creates a better overview

        GameData.tick = 0
        self.__clock = pygame.time.Clock()
        self.__running = False

        # Tastendruck wiederholt senden, falls nicht losgelassen
        delay = int(round(1000.0/GameData.second))
        pygame.key.set_repeat(delay, delay)

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
        self.__next_deer_max = GameData.second*2
        self.__next_deer_min = GameData.second*4/3
        GameData.tick = 0.0
        self.__running = False
        self.__restart = True  # will restart run()
        #GameData.screen = pygame.display.set_mode((GameData.width, GameData.height))
        # self.__clock = pygame.time.Clock()

    def return_to_menu(self):
        self.__startmenu = True
        self.__pause = False
        self.__game_over = False
        img = GameData.startmenu_img
        if GameData.play_as_email: img = GameData.startmenu2_img
        #GameData.screen = pygame.display.set_mode((img.get_width(), img.get_height()))
        GameData.screen = img

    def create_frame(self, surface):
        """Draws onto the given Surface object."""
        # draw background
        #surface.fill(pygame.Color(0, 0, 0, 255))
        if not (self.__pause or self.__startmenu or self.__game_over):
            self.__pos += GameData.game_speed
            self.__pos %= GameData.scaled_street.get_width()
        surface.blit(Game.get_street_img(self.__pos, GameData.play_as_email), (0,0))
        # draw deer
        for deer in GameData.deer:
            deer.render(surface)
        # draw player
        GameData.player.render(surface)
        # draw stats (score, time (with tenth seconds))
        if not self.__game_over: self.__render_stats(surface)


    def create_pause_frame(self, surface):
        """Displays the pause menu on the given Surface object."""
        self.create_frame(surface)
        layer = pygame.Surface((surface.get_width(), surface.get_height())).convert_alpha(surface)
        layer.fill(pygame.Color(0,0,0,102))
        surface.blit(layer, (0,0))
        img = GameData.graphics["pause_vi.png"]
        surface.blit(img, (GameData.width//2 - img.get_width()//2, GameData.height//2 - img.get_height()//2))

    def create_game_over_frame(self, surface):
        """Draws the Game Over screen on the given Surface object."""
        self.create_frame(surface)
        layer = pygame.Surface((surface.get_width(), surface.get_height())).convert_alpha(surface)
        layer.fill(pygame.Color(0,0,0,102))
        surface.blit(layer, (0,0))
        img = GameData.graphics["termine.png"]
        surface.blit(img, (GameData.width//2 - img.get_width()//2, GameData.height//2 - img.get_height()//2))
        self.__render_stats(surface)

    def create_start_menu_frame(self, surface):
        """Paints the starting screen on the Surface object."""
        img = GameData.startmenu_img
        if GameData.play_as_email:
            img = GameData.startmenu2_img
            surface.blit(img, (0,-60))
        else: surface.blit(img, (0,0))

    def render_controls(self, surface):
        """Displays controls on a start menu of a Surface object."""
        vec2d = (GameData.width//2 - GameData.control_img.get_width()//2,
                                        GameData.height//2 - GameData.control_img.get_height()//2)
        surface.blit(GameData.control_img, vec2d)
        if not GameData.play_as_email: surface.blit(GameData.graphics["checkbox_checked.png"], (650+vec2d[0], 223+vec2d[1]))  # quite unprofessional yet

    def __render_stats(self, surface):
        font = pygame.font.Font(pygame.font.match_font("couriernew", bold=True), 35)
        # spawned_deer
        bar = pygame.Rect(5, 32, GameData.bar_img.get_width(), GameData.bar_img.get_height())
        bar_1 = GameData.graphics["barre_d'etat_%s0.png" % ("n" if GameData.play_as_email else "g")]
        surface.blit((GameData.bar_img if GameData.play_as_email else GameData.bar_img2), (0, 0))
        text = font.render("Score: {} ".format(self.__survived_deer), True,
                                 ((255, 255, 255) if GameData.play_as_email else (0,0,0)))
        surface.blit(text,
                    #(255, 255, 255)),
                     (bar.left+bar_1.get_width(), bar.top))
        # time
        text2 = font.render("Temps: %d " % (GameData.tick // GameData.second), True,
                     ((255, 255, 255) if GameData.play_as_email else (0,0,0)))
        surface.blit(text2,
                     #(255, 255, 255)), (bar.left+bar_1.get_width()+40, bar.top+32))
                        (bar.left+bar_1.get_width()+text.get_width(), bar.top))
        # start or pause sign (optional)
        # speed
        surface.blit(font.render("Vitesse: %d km/h" %
            int(float(GameData.game_speed + GameData.car_speed)*GameData.second//(GameData.player_img.get_width()/4.5)*3.6), True,
                     ((255, 255, 255) if GameData.play_as_email else (0,0,0))), (bar.left+bar_1.get_width()+text.get_width()+text2.get_width(), bar.top))
                      #(255, 255, 255)), (bar.left+bar_1.get_width()+40, bar.top+62))

    @staticmethod
    def load_graphics():
        """Gets all needed graphics and puts them in one variable."""
        Game.set_street_img(Game.path("rue_n_clip.png"), Game.path("rue_matrix_clip.png"))
        Game.set_player_img(Game.path("voiture_r2.png"), Game.path("email_g.png"))
        Game.set_deer_img([Game.path("chevreuil_m_gif%i.png" % i) for i in (1, 2, 3, 2)])
        service_colours = ["b", "r", "v", "vi"]
        service_lexicon = dict(zip(service_colours, ["NSA", "BND", "GCHQ", "DGSE"]))
        Game.set_secret_service_imgs(service_colours, [Game.path("virus_%s.png" % service_colours[i])
                                                       for i in range(len(service_colours))],
                    [Game.path("%s_%s.png" % (service_lexicon[service_lexicon.keys()[k]], service_lexicon.keys()[k]))
                     for k in range(len(service_lexicon.keys()))])
        Game.set_images([int(round(GameData.height//3*2)), int(round(float(226/4)*3)), None, None],
                            "allez.png", "termine.png", "checkbox_checked.png", "pause_vi.png")
        bar_height = 200
        bar = [[pygame.Surface((320, bar_height)).convert_alpha(), pygame.Surface((340, bar_height)).convert_alpha(),
                pygame.Surface((117, bar_height)).convert_alpha()] for i in range(2)]
        name = []
        cont = []
        for b in range(len(bar)):
            lastwidth = 0
            for part in range(len(bar[b])):
                pathname = Game.path("barre_d'etat_%s.png" % ("g" if b % 2 == 0 else "n")) # removed accent aigue because files are encoded with Unicode
                bar[b][part].blit(pygame.image.load(pathname).convert_alpha(), (-lastwidth,0))
                lastwidth += bar[b][part].get_width()
                name.append(pathname[4:-4]+("%d.png" % part))
                cont.append(Game.scale(bar[b][part], GameData.height//8))
        # print dict(zip(name, cont))
        GameData.graphics.update(dict(zip(name, cont)))
        Game.set_status_bar_img()
        GameData.startmenu_img = Game.scale(pygame.image.load(Game.path("chevreuil_morte.jpg")).convert(),
                                                GameData.height)
        img = pygame.image.load(Game.path("premier_ecran.jpg")).convert()
        GameData.startmenu2_img = Game.scale(img, img.get_height()-105)  # with unicode file name image open problem
        GameData.control_img = pygame.image.load(Game.path("tableau_de_controle.png")).convert_alpha() # hello unicode!

    # Road Adjustment
    @staticmethod
    def set_street_img(path, path2=None):
        if not path2: path2 = path
        # self.street_img # we don't need it anymore
        GameData.scaled_street = Game.scale(pygame.image.load(path).convert(), GameData.height)
        GameData.scaled_street2 = Game.scale(pygame.image.load(path2).convert(), GameData.height)

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
        GameData.player_img = Game.scale(img, GameData.height // 6)
        GameData.player_img2 = Game.scale(img2, GameData.height // 6)

    # obstacle presentation
    @staticmethod
    def set_deer_img(paths):
        imgs = [pygame.image.load(path).convert_alpha() for path in paths]
        GameData.deer_imgs = Game.scale_list(imgs, GameData.height // 6)

    @staticmethod
    def set_secret_service_imgs(keys, virus_paths, logo_paths):
        """Arg0 = key names for the images from both path lists
           Arg1 = the list of paths for the secret service images
           Arg2 = the list of paths for the virus images"""
        imgs = [pygame.image.load(path).convert_alpha() for path in logo_paths]
        #logo_imgs = dict(zip(keys, imgs))
        GameData.logo_imgs = Game.scale_list(imgs, GameData.height//6)
        imgs = [pygame.image.load(path).convert_alpha() for path in virus_paths]
        #virus_imgs = dict(zip(keys, imgs))
        GameData.virus_imgs = Game.scale_list(imgs, GameData.height//6)

    # other graphical presentation
    @staticmethod
    def scale(img, rel_height):
        return pygame.transform.scale(img, (int(round(float(img.get_width()) / img.get_height() * rel_height)),
                                            rel_height))

    @staticmethod
    def scale_list(imgs, rel_heights=None):
        """Takes a list/tuple of images and a list/tuple of target heights and
        returns the corresponding resized Surface objects and the widths."""
        if not imgs or not rel_heights: return None
        elif not isinstance(rel_heights, list) and not isinstance(rel_heights, tuple):
            rel_heights = [rel_heights for i in range(len(imgs))]
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
    def set_status_bar_img():
        for i in range(2):
            fill = "n" if i%2==0 else "g"
            bar_1 = GameData.graphics["barre_d'etat_"+fill+"0.png"]
            bar_2 = pygame.transform.scale(GameData.graphics["barre_d'etat_"+fill+"1.png"], (GameData.width//5*3+80, bar_1.get_height()))
            bar_3 = GameData.graphics["barre_d'etat_"+fill+"2.png"]
            bar = pygame.Rect(0, 0, bar_1.get_width()+bar_2.get_width()+bar_3.get_width(), bar_1.get_height())
            sur = pygame.Surface((bar.width, bar.height), pygame.SRCALPHA)
            sur.fill(pygame.Color(0,0,0,0))
            sur.blit(bar_1, (bar.left,bar.top))
            sur.blit(bar_2, (bar.left+bar_1.get_width(), bar.top))
            sur.blit(bar_3, (bar.left+bar_1.get_width()+bar_2.get_width(), bar.top))
            if i%2==0:
                GameData.bar_img = sur
            else:
                GameData.bar_img2 = sur

    @staticmethod
    def set_deer(move_types):
        GameData.deer = [Deer(move_type) for move_type in move_types]

    @staticmethod
    def get_random_move_type():
        move_type = 0
        n = 23
        mt = randint(0, n)
        p = [3, 3, 2, 2, 1, 1]  # probabilites, repeated to 12 elements, all elements' sum must be n+1
        for i in range(1,12):
            n -= p[i%len(p)]
            if mt > n:
                move_type += 1
        return move_type

    @staticmethod
    def spawn_deer():
        GameData.deer.append(Deer(Game.get_random_move_type()))
        #GameData.deer.append(Deer(2))

    @staticmethod
    def reset_deer(instance):
        instance.reset(Game.get_random_move_type())

    # core function
    def run(self):
        render_controls = False
        GameData.tick = 0
        spawn_count = 0  # number of spawned deer
        last_spawned = 0  # manages the spawn rate by looking how long nothing has been spawned
        maximum_count = 5  # more than 4 deer aren't allowed on the road
        maximum_speed = 4000 // GameData.second
        new_game = True
        GameData.car_speed = 0
        self.__running = True
        keys = pygame.key.get_pressed()
        while self.__running:
            self.__clock.tick(GameData.second)
            mouse_click = False
            key_click = False

            # EXIT CONDITION
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
                if ev.type == pygame.KEYUP:
                    key_click = True
            
            # PREPARE USER INPUT
            keys2 = pygame.key.get_pressed()  # I don't know if this was a good idea
            input_sum = sum(keys)-1

            # incomplete pygame.event code
            # pygame.event.pump()
            # input_sum = pygame.event.peek(pygame.event.get())

            # MODES
            if self.__startmenu:
                self.create_start_menu_frame(GameData.screen)
                if render_controls:
                    # USER input
                    if mouse_click:
                        GameData.play_as_email = not GameData.play_as_email
                    if input_sum and key_click:
                        render_controls = False
                    else: self.render_controls(GameData.screen)
                elif mouse_click: webbrowser.open_new_tab("http://goo.gl/yuXawT")
                elif input_sum and key_click:
                    # USER input
                    if keys[pygame.K_SPACE]:
                        render_controls = True
                    elif keys[pygame.K_ESCAPE]:
                        self.__running = False
                        break
                    else:
                        self.reset_game_scene()  # sets self.__startmenu = False

            elif self.__game_over:
                self.create_game_over_frame(GameData.screen)
                # USER input
                if input_sum and key_click and not self.__pause:
                    if keys[pygame.K_ESCAPE]: self.return_to_menu()
                    else: self.reset_game_scene()  # sets self.__game_over = False
                if key_click: self.__pause = False

            elif self.__pause:
                self.create_pause_frame(GameData.screen)
                if render_controls:
                    # USER input
                    if mouse_click:
                        GameData.play_as_email = not GameData.play_as_email
                    if input_sum and key_click:
                        render_controls = False
                    self.render_controls(GameData.screen)
                else:
                    # USER input
                    if input_sum and key_click:
                        if keys[pygame.K_SPACE]: render_controls = True
                        elif keys[pygame.K_KP_ENTER]: self.reset_game_scene()
                        else:
                            self.__pause = False
                            if keys[pygame.K_ESCAPE]:
                                self.return_to_menu()

            else:
                GameData.tick += 1
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
                        GameData.player.boost = True
                    else: GameData.player.boost = False
                    if keys[pygame.K_ESCAPE] and key_click:
                        self.__pause = True  # fänd ich gut, vielleicht kann man dann von dort beenden

                    # GAME routine
                    if GameData.tick % (GameData.second*2) == 0:
                        if self.__next_deer_max > 60:
                            self.__next_deer_max -= 1
                        if self.__next_deer_min > 15:
                            self.__next_deer_min -= 1
                    if GameData.tick % int(GameData.second*2.0) == 0 and GameData.game_speed < maximum_speed:
                        GameData.game_speed += 1

                    # SPAWN
                    if self.__next_deer == 0 and spawn_count < maximum_count:
                        Game.spawn_deer()
                        spawn_count += 1
                        self.__next_deer = randint(self.__next_deer_min, self.__next_deer_max)
                    else:
                        self.__next_deer -= 1

                    deer_hitboxes = []
                    spawn_count_mirror = spawn_count
                    for deer in GameData.deer:
                        deer.move()
                        if deer.is_away():
                            GameData.deer.remove(deer)
                            self.__survived_deer += 1
                            spawn_count -= 1
                        else: deer_hitboxes.append(deer.hitbox())
                    if not spawn_count == spawn_count_mirror: last_spawned += 1
                    if last_spawned > self.__next_deer_max:
                        GameData.deer = []
                        Game.spawn_deer()
                        spawn_count = 1
                    self.__game_over = GameData.player.hitbox().collidelist(deer_hitboxes)
                    if self.__game_over < 0: self.__game_over = False
                    else:
                        self.__game_over = True
                        if input_sum: self.__pause = True
                        GameData.tick = 0

                # SETUP IMAGE BUFFER
                self.create_frame(GameData.screen)

                # INTRO
                if new_game:
                    allez = GameData.graphics["allez.png"]
                    GameData.screen.blit(allez, (GameData.width//2-allez.get_width()//2,
                                               GameData.height//2-allez.get_height()//2))
                    if GameData.tick % (GameData.second*1.5) == 0:
                        new_game = False

            keys = keys2

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


def main():
    game = Game()
    Game.load_graphics()
    while True:  # will leave run() and execute it again, if self.__restart == True; this prevents recursion stack overflow
        game.run()

if __name__ == "__main__":
    main()
