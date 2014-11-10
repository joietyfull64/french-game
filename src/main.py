#!/usr/bin/env python2
# vim: set fileencoding=utf-8

import os.path
import sys
import math

#TODO:   - create_frame methods

#I suggest that we declare all instance variables in the constructor

import pygame


class Player:

    def __init__(self, x=Game.bounds[2], y=Game.instance.screen().get_height//2):
        """Initializes the Player instance. Arguments:
        x     = The initial x coordinate of the Player
        y     = The initial y coordinate of the Player
        img   = The player's image
        """
        self.x = x
        self.y = y
        self.speed_x = Game.instance.height()//Game.second
        self.speed_y = (Game.instance.width() // 2)//Game.second #I made it double as fast as before
        self.boost = False #mehr dazu: unterer Kommentar
        self.boost_factor = 2.0 #when space is pressed, the movement will be faster by this factor

    def hitbox(self):
        return Game.instance.player_img.get_rect().move(self.x, self.y)
    
    def up(self):
        """Moves the Player up."""
        if self.hitbox().top > Game.instance.screen().top+self.bounds[0]:
            self.y -= self.speed_y if not self.boost else self.speed_y*self.boost_factor

    def down(self):
        """Moves the Player down."""
        if self.hitbox().bottom < Game.instance.screen().bottom+self.bounds[1]:
            Game.instance.car_speed += self.speed_y if not self.boost else self.speed_y*self.boost_factor
            self.x += Game.instance.car_speed

    def accelerate(self):
        """Accelerates the Player."""
        if self.hitbox().right < Game.instance.screen().right+self.bounds[3]:
#            print "ACC"
            self.x += self.speed_x if not self.boost else self.speed_x*self.boost_factor
#        else:
#            print self.hitbox().right, Game.instance.screen().right

    def decelerate(self):
        """Decelerates the Player."""
        if self.hitbox().left > Game.instance.screen().left+self.bounds[2]:
#            print "DEC"
            Game.instance.car_speed -= self.speed_x if not self.boost else self.speed_x*self.boost_factor
            self.x -= Game.instance.car_speed

#Obsolete - use set_player_image() instead
#    def set_img(self, img):
#        """Sets the image (and hitbox) of the Player. Argument:
#        img = pygame.Surface containing the image for the Enity.
#        """
#        Game.instance.player_img = img
#        self.hitbox() = Game.instance.player_img.get_rect().move(self.x, self.y)

    def render(self, surface):
        """Blits the Player on 'surface'."""
        surface.blit(Game.instance.player_img, self.hitbox())


class Deer:

    #the x and y coordinate will be set randomly
    def __init__(self, move_type):
        """Initializes the Deer instance. Arguments:
        move_type = The movement type. See Deer.move().
        imgs = a tuple of images whose elementary images are switched
        """
        self.move_type = move_type
        self.__img = -1 #animation index, -1 weil wir vor jedem Anzeigen zuerst diese Variable erhöhen
        self.__key_frame = -1 #wir sind dann mal doch nicht zu faul eine neue Variable zu erstellen
                   #die Frame-Nummer der Animation
        self.__angle = 0 # the angle after which the, by default vertical, image is rotated counterclockwise
        
        self.x = 0
        self.y = 0
        self.__speed_x = 0 #we need it for movment_type 8 & 9
        self.__speed_y = 0 #we need it for movement_type 4 & 5
        #self.hitbox = self.hitbox() #instead of self.hitbox use self.hitbox()
        self.__longest_img_width = Game.instance.deer_imgs[0].get_width() #benutzt in is_away() und hier drunter
        self.__longest_img_height = Game.instance.deer_imgs[0].get_height()
        if not self.move_type == 0:
            for i in Game.instance.deer_imgs:
                if i.get_width() > self.__longest_img_width:
                    self.__longest_img_width = i.get_width()
                if i.get_height() > self.__longest_img_height:
                    self.__longest_img_height = i.get_height()

        #start positions of the move_types and picture angle calculations
        g = Game.instance
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
            self.__angle += math.tan(g.game_speed // self.__speed_y) # self.__speed_y is always positive
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
        else: #0 & 1 & 10 & 11
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
        img = Game.instance.deer_imgs[self.img]
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
        #position changes for move_types
        g = Game.instance
        #if self.move_type == 0 is at the end of the function
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
                self.__angle -= 90 #if running towards car: = 90 - self.__angle
                self.__angle *= 2
            else:
                self.y += self.__speed_y
        else: # 0 & others
            self.x -= g.game_speed
#       print "MOVED %s" % self.hitbox

    #obsolete - use set_deer_image instead
    #def set_imgs(self, imgs, x = self.x, y = self.y):
    #    """Sets the image of the Deer. Argument:
    #        imgs = List of 'pygame.Surface's containing the image for the Enity.
    #        x    = the new x coordinate of the upper left corner
    #        y    = the new y coordinate of the upper right corner
    #    """
    #    Game.instance.deer_imgs = imgs
    #    self.x = x
    #    self.y = y

    def next_img(self):
        """Returns the next image in the animation"""
        if not Game.playAsEmail:
            self.__img = 0 if self.__img >= len(Game.instance.deer_imgs)-1 else self.__img+1
            if move_type < 1 or move_type > 11:
                if not self.__angle == 0: return pygame.transform.rotate(Game.instance.deer_imgs[0], self.__angle)
                else: return Game.instance.deer_imgs[0]
            else:
                img = Game.instance.deer_imgs[self.__img]
                if not self.__angle == 0: return pygame.transform.rotate(img, self.__angle)
                else: return img
        else:
            #possibility 1 (easy):
            #if randint(0,1): return Game.instance.logo_imgs[self.__img]
            #else: return Game.instance.instance.virus_imgs[self.__img]
            
            #possibility 2 (advanced - with compound animation):
            ##both images
            #logo = Game.instance.logo_imgs[self.__img]
            #virus = pygame.transform.rotate(Game.instance.virus_imgs[self.__img], self.__angle)
            ##variables
            #anim_len = Game.second*2
            #width = logo.get_width()
            #if self.__key_frame == -1: self.__key_frame = randint(0,anim_len-1)
            #frame_unit = 2*width // anim_len
            #offset = self.__key_frame*frame_unit
            ##layers
            #img = pygame.transform.flip(logo, False, True).move(width-offset,0)
            #img.blit(virus,(0,0))
            #img.blit(logo, ((width+offset)%(2*width)-width,0))
            ##update non-temporary variables
            #self.__angle += int(round(360 // anim_len))
            #self.__key_frame += 1
            #self.__key_frame %= anim_len
            #return img
            
            #possibility 3 (advanced - creates a realistic cylindric rotation around the y-axis (mathemtical z-axis)):
            logo = Game.instance.logo_imgs[self.__img]
            virus = pygame.transform.rotate(Game.instance.virus_imgs[self.__img], self.__angle)
            #variables
            anim_len = Game.second*2
            width = logo.get_width()
            radius = math.sqrt((width//2)**2 + (width//2)**2)
            if self.__key_frame == -1: self.__key_frame = randint(0,anim_len-1)
            frame_unit = radius*2*Math.PI // anim_len
            offset = self.__key_frame*frame_unit #Bogenmaß
            offset2 = offset+radius*(math.asin(0.5)//90*Math.PI) #angle*2//360*Math.PI*2; width//2//width = 0.5
            #logo_angled_width = math.sqrt(width**2 - ((math.sin(float(offset)/radius)-math.sin(float(offset2)/radius))*radius)**2) #even simpler:
            x_distance = math.cos(float(offset)/radius)*radius
            x_distance2 = math.cos(float(offset2)/radius)*radius
            logo_angled_width = x_distance-x_distance2
            #layers
            img = Surface((width, logo.get_height()))
            logo = pygame.transform.scale(logo, (abs(logo_angled_width), logo.get_height()))
            if logo_angled_width < 0:
                img.blit(pygame.transform.flip(logo, False, True), (x_distance2,0))
                img.blit(virus,(img.get_width//2-virus.get_width//2,img.get_height()//2-virus.get_height()//2))
            else:
                img.blit(virus,(img.get_width//2-virus.get_width//2,img.get_height()//2-virus.get_height()//2))
                img.blit(logo, (x_distance,0))
            #update non-temporary variables
            self.__angle += 360 // anim_len
            self.__key_frame += 1
            self.__key_frame %= anim_len
            return img

    def render(self, surface):
        #habe next_img() gleich hier benutzt
        """Blits the Deer on 'surface'."""
        surface.blit(self.next_img(), self.hitbox())

    def is_away(self):
        screen = Game.instance.screen()
        return self.x < -self.__longest_img_width or self.x > screen.get_width() or \
               self.y < -self.__longest_img_height or self.y > screen.get_height()


class Game(object):

    """Weitere optionale Ideen zum Einbauen:
        - eine besondere Farbe für Rehe verschiedener move_typen
        - Autos auf der Gegenspur"""
    # is needed to call instance variables with other classes' methods
    instance = Game()
    second = 30
    playAsEmail = True
    img_path = "C:\Users\ChristophEhmendörfer\Documents\Schule\Anderes für die Schule\video game frz"
    
    def __init__(self, width=1200, height=400):
        """
        Initializes the Game instance. Arguments:
        width      = window width
        height     = window height
        """
        # Initialisierung
        self.__width = width
        self.__height = height

        self.__startmenu = True
        self.__pause = False
        self.__game_over = False
        self.__restart = False
        self.__survived_deer = 0
        self.__pos = 0 #street offset
        self.bounds = (0,-0,0,-0) #up, down, left, right; determines the smallest possible distance from the player to the street edge
        self.deer_vertical_speed = (self.__height+self.bounds[0]+self.bounds[1])/(Game.second*2) #used for Deer.move()

        pygame.init()
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption("Passée")
        pygame.mouse.set_visible(1)
        
        self.game_speed = 300//Game.second
        self.car_speed = 0
        self.player = Player()

        self.deer = []
        self.__next_deer = Game.second
        self.__next_deer_max = Game.second*3
        self.__next_deer_min = Game.second*7/3
        
        #I think, this creates a better overview
        self.scaled_street = None
        self.scaled_street2 = None
        self.player_img = None
        self.deer_imgs = None
        self.virus_imgs = None
        self.logo_imgs = None
        self.graphics = None

        self.__time = 0.0
        self.__clock = pygame.time.Clock()
        self.__running = False
        
        # Tastendruck wiederholt senden, falls nicht losgelassen
        delay = int(round(1000.0/Game.second))
        pygame.key.set_repeat(delay, delay)
    
    def height(self):
        return self.__height
    
    def width(self):
        return self.__width
    
    def screen(self):
        return self.__screen
    
    def reset_game_scene(self):
        """Resets all options and restarts the game."""
        #Game.instance = Game() #this only works, if this method and run() are staticmethods; begins always with startmenu
        self.player = Player()
        self.deer = []
        self.__survived_deer = 0
        self.__startmenu = False
        self.__pause = False
        self.__game_over = False
        self.game_speed = 300//Game.second
        self.car_speed = 0
        self.__pos = 0
        self.__next_deer = Game.second
        self.__next_deer_max = Game.second*3
        self.__next_deer_min = Game.second*7/3
        self.__time = 0.0
        self.__running = False
        self.__restart = True #will restart run()
        #self.__clock = pygame.time.Clock()
    
    def create_frame(self, surface):
        """Draws onto the given Surface object."""
        #draw background
        surface.fill(pygame.Color(0,0,0,255))
        self.__pos += self.game_speed
        self.__pos %= self.scaled_street.get_width()
        surface.blit(self.get_street_img(self.__pos), (0, 0))
        #draw player
        self.player.render(surface)
        #draw deer
        for deer in self.deer:
            deer.render(self.__screen)
        #draw stats (score, time (with tenth seconds))
            #spawned_deer
            #time
            #start or pause sign (optional)
            speed = int(round((self.game_speed + self.car_speed)*Game.second//(self.player_img.get_width()/4.5)*3.6)) #speed
    
    def create_pause_frame(self, surface):
        """Displays the pause menu on the given Surface object."""
        self.create_frame(surface)
    
    def create_game_over_frame(self, surface):
        """Draws the Game Over screen on the given Surface object."""
        surface.fill(pygame.Color(0,0,0,255))
    
    def create_start_menu_frame(self, surface):
        """Paints the starting screen on the Surface object."""
        surface.fill(pygame.Color(0,0,0,255))
    
    def render_controls(self, surface):
        """Displays controls on a start menu of a Surface object."""
        surface.blit(None, (0,0))

    @staticmethod
    def load_graphics(): #we use it because you don't want global variables as I understood
        """Gets all needed graphics and puts them in one variable."""
        Game.instance.set_street_img(Game.path("rue_n_clip.png"), Game.path("rue_matrix_clip.png"))
        Game.instance.set_player_img(Game.path("img", "voiture_r2.png"))
        Game.instance.set_deer_img([Game.path("img", "chevreuil_m_gif%i.png" % i) for i in (1, 2, 3, 2)])
        service_colours = ["b", "r", "v", "vi"]
        service_lexicon = dict(zip(service_colours, ["NSA", "GCHQ", "BND", "DGSE"]))
        Game.instance.set_secret_service_imgs(service_colours, [Game.path("virus_%s" % i) for i in service_colours],
                                              [Game.path("%s_%s" % (service_lexicon[k], k)) for k in service_lexicon])
        #the toggled code could enable a maximum size for all images, given by the imgHeights list
        #maxHeights = [Game.instance.height//3*2]
        #imgHeights = [636]
        #bools = [imgHeights[i] > maxHeights[i] for i in range(len(imgHeights))]
        #Game.instance.set_images([(imgHeights[i] if bools[i] else maxHeights[i]) for i in range(len(bools))], Game.path("allez.png"))
        Game.instance.set_images([Game.instance.height//3*2], Game.path("allez.png"))
    
    #Road Adjustment
    def set_street_img(self, path, path2=None):
        if not path2: path2 = path
        img = pygame.image.load(path).convert()
        img2 = pygame.image.load(path2).convert()
        #self.street_img # we don't need it anymore
        self.scaled_street = self.scale(img, img.get_height())
        self.scaled_street2 = self.scale(img2, img2.get_height())

#Obsolete - use scale() instead
#    def scale_street_img(self, street_img):
#        width = street_img.get_width()
#        height = street_img.get_height()
#        scale = height // self.__height #self.__height // height
#        img = pygame.transform.scale(street_img, (width // scale, self.__height)) #scale * width
#        return img

    def get_street_img(self, offset, matrix_style = True): 
        surf = pygame.Surface((self.__width, self.__height))
        street = self.scaled_street if not matrix_style else self.scaled_street2
        for x in range(-offset, self.__width, street.get_width()):
            surf.blit(street, (x, 0))
        return surf

    #player presentation
    def set_player_img(self, path):
        img = pygame.image.load(path).convert_alpha()
        self.player_img, width = self.scale(img, self.__height / 5)

    #obstacle presentation
    def set_deer_img(self, paths):
        imgs = [pygame.image.load(path).convert_alpha() for path in paths]
        self.deer_imgs, width = self.scale(imgs, self.__height / 5)
    
    def set_secret_service_imgs(self, keys, logo_paths, virus_paths):
        """Arg0 = key names for the images from both path lists
           Arg1 = the list of paths for the secret service images
           Arg2 = the list of paths for the virus images"""
        logo_imgs = dict(zip(keys, [pygame.image.load(path).convert_alpha() for path in logo_paths]))
        self.logo_imgs, width = self.scale(logo_imgs.itervalues(), self.__height/5)
        virus_imgs = dict(zip(keys, [pygame.image.load(path).convert_alpha() for path in virus_paths]))
        self.virus_imgs, width = self.scale(virus_imgs.itervalues(), self.__height/5)
    
    #other graphical presentation
    def scale(self, imgs, rel_height=self.__height):
        """Takes one or multiple images and one or multiple target heights and
        returns the corresponding resized Surface object(s) and the width(s)."""
        if len(imgs) > 1:
            if len(rel_height) > 1:
                lst = imgs if not len(imgs) > len(rel_height) else rel_height
                widths = [int(round(imgs[i].get_width() * rel_height[i] //
                                    imgs[i].get_height())) for i in range(len(lst))]
                return [pygame.transform.scale(imgs[i], (widths[i], rel_height[i])) for i in range(len(lst))], widths
            else:
                widths = [int(round(imgs[i].get_width() * rel_height // img[i].get_height())) for i in range(len(imgs))]
                return [pygame.transform.scale(imgs[i], (widths[i], rel_height)) for i in range(len(imgs))], widths
        else:
            if len(rel_height) > 1: rel_height = rel_height[0]
            width = int(round(imgs.get_width() * rel_height // imgs.get_height()))
            return pygame.transform.scale(imgs, (width, rel_height)), width
    
    def set_images(self, heights, *paths):
        imgs = dict(zip(paths, [pygame.image.load(path).convert_alpha() for path in paths]))
        widths = self.scale(imgs.itervalues(), heights)
        self.graphics = [pygame.transform.scale(imgs.itervalues()[i], widths[i], heights[i]) for i in range(len(imgs))]

    def spawn_deer(self):
        #if randint(0, 1): #we already have a random spawn time in run() and a spawn limit
        move_type = 0
        #I think, this solution is a bit too complicated:
        #if self.game_speed < 20:
        #    move_type = randint(0, 2)
        #elif self.game_speed < 30:
        #    move_type = randint(0, 4)
        #else:
        #    move_type = randint(0, 11)
        #I would do it like this:
        n = 23
        mt = randint(0, n)
        p = [3, 3, 2, 2, 1, 1] #probabilites, repeated to 12 elements, all elements' sum must be n+1
        for i in range(1,12):
            n -= p[i%len(p)]
            if mt > n:
                move_type = 1
        self.deer.append(Deer(move_type))

    #core function
    def run(self):
        render_controls = False
        intro = True
        #pos = 0 #it's easier to use an instance variable because I want to use it in dispatched functions
        tick = 0
        spawn_count = 0 #number of spawned deer
        maximum_count = 4 #more than 4 deer aren't allowed on the road
        maximum_speed = 50
        new_game = True
        self.__time = 0.0
        self.car_speed = 0
        self.__running = True
        while self.__running:
            self.__clock.tick(Game.second)
            self.__time += 100.0/Game.second
            if round(self.__time, 2) - round(self.__time) == -0.01: self.__time = round(self.__time)
            #tick fits rather in the active gameplay section
            
            #EXIT CONDITION
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
            #PREPARE USER INPUT
            keys = pygame.key.get_pressed()

            #MODES
            if self.__startmenu:
                self.create_start_menu_frame(self.__screen)
                if render_controls:
                    #USER input
                    if len(keys):
                        render_controls = False
                    else: self.render_controls(self.__screen)
                else:
                    #USER input
                    if keys[pygame.K_SPACE]: render_controls = True
                    elif keys[pygame.K_ESCAPE]:
                        self.__running = False
                        break
                    elif len(keys):
                        self.reset_game_scene() #sets self.__startmenu = False
            
            elif self.__game_over:
                #USER input
                if len(keys):
                    if keys[pygame.K_ESCAPE]: startmenu = True
                    else: self.reset_game_scene() #sets self.__game_over = False
                else: self.create_game_over_frame(self.__screen)
            
            elif self.__pause:
                if render_controls:
                    #USER input
                    if len(keys):
                        render_controls = False
                    else: self.render_controls(self.__screen)
                else:
                    #USER input
                    if len(keys):
                        if keys[pygame.K_SPACE]: render_controls = True
                        elif keys[pygame.K_ESCAPE]:
                            self.__running = False
                            break
                        else: self.__pause = False
                    else: self.create_pause_frame(self.__screen)

            else:
                tick += 1
                self.car_speed = 0
                if not new_game:
                    #USER INPUT:
                    if keys[pygame.K_RIGHT]:
                        Game.instance.player.accelerate()
                    else:
                        Game.instance.player.decelerate()
                    if keys[pygame.K_LEFT]: #brake
                        Game.instance.player.decelerate()
                    if keys[pygame.K_UP]:
                        Game.instance.player.up()
                    if keys[pygame.K_DOWN]:
                        Game.instance.player.down()
                    if keys[pygame.K_SPACE]:
                        Game.instance.player.boost = True # self.boost ist schon in accelerate() und decelerate() eingebaut
                    else: Game.instance.player.boost = False # WICHTIG
                    if keys[pygame.K_ESCAPE]:
                        pause = True #fänd ich gut, vielleicht kann man dann von dort beenden

                    #GAME routine
                    if tick % (Game.second*2) == 0:
                        if self.__next_deer_max > Game.second*2:
                            self.__next_deer_max -= 1
                        if self.__next_deer_min > Game.second//4:
                            self.__next_deer_min -= 1
                    if tick % int(Game.second*2.5) == 0 and self.game_speed < self.maximum_speed:
                        self.game_speed += 1
                        #for deer in self.deer: #we don't need it anymore
                            #deer.game_speed = self.game_speed
                            #self.player.game_speed = self.game_speed
                
                    #SPAWN
                    if self.__next_deer == 0 and spawn_count < maximum_count:
                        self.spawn_deer()
                        spawn_count += 1
                        self.__next_deer = randint(self.__next_deer_min, self.__next_deer_max)
                    else:
                        self.__next_deer -= 1
                
                    #self.__game_over = Game.instance.player.hasCrashed()
                    self.__game_over = self.player.hitbox().collidelist(self.deer)
                    for i in range(len(Game.instance.deer)):
                        deer = Game.instance.deer[i]
                        deer.move()
                        if deer.is_away():
                            Game.instance.deer.remove(i)
                            self.__survived_deer += 1
                            spawn_count -= 1
                
                #SETUP IMAGE BUFFER
                self.create_frame(self.__screen)
                
                #INTRO
                if new_game:
                    allez = self.graphics[Game.path("allez.png")]
                    self.__screen.blit(allez, (self.__width//2-allez.get_width//2,
                                               self.__height//2-allez.get_height()//2))
                    if tick % (Game.second*2) == 0:
                        new_game = False

            #SHOW CONTENT
            pygame.display.flip()

        if not self.__restart:
            #FINISH IT!
            sys.exit()
        else: self.__restart = False

    @staticmethod
    def path(self, path):
        return os.path.join(img_path+"img", path)
        #return os.path.join("img", path))

if __name__ == "__main__":
    #game = Game() #we don't need it anymore
    Game.load_graphics()
    while True: #will leave run() and execute it again, if self.__restart == True
        Game.instance.run()
