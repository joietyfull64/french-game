#!/usr/bin/env python2
# vim: set fileencoding=utf-8

import os.path
import sys
from math import ceil

#TODO:   - load pictures and createFrame methods
#        - use real names for used Math function menmonics (sqrt, sin, cos, tan, arcsin, arccos) and the pi constant

import pygame

class Player(object):

    def __init__(self, x, y, img):
        """Initializes the Player instance. Arguments:
        x     = The initial x coordinate of the Player
        y     = The initial y coordinate of the Player
        img   = The player's image
        """
        self.x = x
        self.y = y
        self.set_image(img)
        self.boost = False #mehr dazu: unterer Kommentar
        self.boostFactor = 2.0 #when space is pressed, the movement will be faster by this factor
    
    def up(self):
        """Moves the Player up."""
        if self.hitbox.top > Game.instance.screen.top+self.bounds[0]:
            self.hitbox = self.hitbox.move(0, ((-Game.instance.screen.get_height() // 30) if not self.boost else (-Game.instance.screen.get_height()//30*self.boostFactor)) )

    def down(self):
        """Moves the Player down."""
        if self.hitbox.bottom < Game.instance.screen.bottom+self.bounds[1]:
            self.hitbox = self.hitbox.move(0, ((Game.instance.screen.get_height() // 30) if not self.boost else (Game.instance.screen.get_height()//30*self.boostFactor)) )

    def accelerate(self):
        """Accelerates the Player."""
        if self.hitbox.right < Game.instance.screen.right+self.bounds[3]:
#            print "ACC"
            self.hitbox = self.hitbox.move( ((Game.instance.screen.get_width() // 120) if not self.boost else (Game.instance.screen.get_width()//120*self.boostFactor)), 0)
#        else:
#            print self.hitbox.right, Game.instance.screen.right
    def decelerate(self):
        """Decelerates the Player."""
        if self.hitbox.left > Game.instance.screen.left+self.bounds[2]:
#            print "DEC"
            self.hitbox = self.hitbox.move( ((-Game.instance.screen.get_width() // 120) if not self.boost else (-Game.instance.screen.get_width()//120*self.boostFactor)), 0)

    def set_img(self, img):
        """Sets the image (and hitbox) of the Player. Argument:
        img = pygame.Surface containing the image for the Enity.
        """
        self.img = img
        self.hitbox = self.img.get_rect().move(self.x, self.y)
    #Unused
    def get_img(self):
        """Returns: arg0 = self.img, arg1 = self.x, arg2 = self.y"""
        return self.img, self.x, self.y

    def render(self, surface):
        """Blits the Player on 'surface'."""
        surface.blit(self.img, self.hitbox)

class Deer(object):
    #the x and y coordinate will be set randomly
    def __init__(self, move_type, imgs):
        """Initializes the Deer instance. Arguments:
        move_type = The movement type. See Deer.move().
        imgs = a tuple of images whose elementary images are switched
        """
        self.move_type = move_type
        self.img = -1 #animation index, -1 weil wir vor jedem Anzeigen zuerst diese Variable erhöhen
        self.key_frame = -1 #wir sind dann mal doch nicht zu faul eine neue Variable zu erstellen
                   #die Frame-Nummer der Animation
        self.angle = 0 # the angle after which the, by default vertical, image is rotated counterclockwise
        
        self.x = x
        self.y = y
        self.speed_x = 0 #we need it for movment_type 8 & 9
        self.speed_y = 0 #we need it for movement_type 4 & 5
        #self.hitbox = self.hitbox() #instead of self.hitbox use self.hitbox()
        self.longestImgWidth = Game.instance.deer_imgs[0].get_width() #benutzt in isAway() und hier drunter
        self.longestImgHeight = Game.instance.deer_imgs[0].get_height()
        if not self.move_type == 0:
            for i in Game.instance.deer_imgs:
                if i.get_width() > self.longestImgWidth:
                    self.longestImgWidth = i.get_width()
                if i.get_height() > self.longestImgHeight:
                    self.longestImgHeight = i.get_height()

        #start positions of the move_types and picture angle calculations
        g = Game.instance
        self.angle = -90
        if self.move_type == 2:
            self.x = g.screen.get_width()
            self.y = randint(g.screen.get_height()//2, g.screen.get_height()+g.bounds[1]-self.longestImgHeight))
            self.angle += tan(g.game_speed // g.vertical_deer_speed)
        elif self.move_type == 3:
            self.x = g.screen.get_width()
            self.y = randint(g.bounds[0], g.screen//2-self.longestImgHeight)
            self.angle -= tan(g.game_speed // g.vertical_deer_speed)
        elif self.move_type == 4:
            self.x = g.screen.get_width()
            self.y = randint(g.player.y,g.screen.get_height()-self.longestImgheight+g.bounds[1])
            hitbox = self.hitbox()
            self.speed_y = ((g.player.y+g.player.hitbox.height//2)-(self.y+hitbox.height//2))//((g.player.x+g.player.hitbox.width//2)-(self.x+hitbox.width//2))*g.game_speed
            self.angle += tan(g.game_speed // self.speed_y) # self.speed_y is always positive
        elif self.move_type == 5:
            self.x = g.screen.get_width()
            self.y = randint(g.bounds[0], g.player.y+g.player.height-self.longestImgHeight)
            hitbox = self.hitbox()
            self.speed_y = ((g.player.y+g.player.hitbox.height//2)-(self.y+hitbox.height//2))//((g.player.x+g.player.hitbox.width//2)-(self.x+hitbox.width//2))*g.game_speed
            self.angle -= tan(g.game_speed // -self.speed_y)
        elif self.move_type == 6:
            self.x = randint(g.bounds[2], g.screen.get_width()+g.bounds[3]-self.longestImgWidth)
            self.y = -imgs[0].get_height()
            self.angle = 0
        elif self.move_type == 8:
            self.x = randint(g.bounds[2], g.screen.get_width()+g.bounds[3]-self.longestImgWidth)
            self.y = -imgs[0].get_height()
            hitbox = self.hitbox()
            self.speed_x = ((g.player.x+g.player.hitbox.width//2)-(self.x+hitbox.width//2))//((g.player.y+g.player.hitbox.height//2)-(self.y+hitbox.height//2))*g.vertical_deer_speed
            self.angle = (((self.speed_x >> -1)^-1)|1)*tan(g.vertical_deer_speed // self.speed_x)
        elif self.move_type == 7:
            self.x = randint(g.bounds[2], g.screen.get_width()+g.bounds[3]-self.longestImgWidth)
            self.y = g.screen.get_height()
            self.angle = 180
        elif self.move_type == 9:
            self.x = randint(g.bounds[2], g.screen.get_width()+g.bounds[3]-self.longestImgWidth)
            self.y = g.screen.get_height()
            hitbox = self.hitbox()
            self.speed_x = ((g.player.x+g.player.hitbox.width//2)-(self.x+hitbox.width//2))//((g.player.y+g.player.hitbox.height//2)-(self.y+hitbox.height//2))*g.vertical_deer_speed
            self.angle = 180 + ((self.speed_x >> -1)|1)*tan(g.vertical_deer_speed // self.speed_x)
        else: #0 & 1 & 10 & 11
            gs = g.game_speed//2
            if self.move_type == 10:
                self.speed_y = -g.vertical_deer_speed
                self.angle += tan(gs // self.speed_y))
            elif self.move_type == 11:
                self.speed_y = g.vertical_deer_speed
                self.angle -= tan(gs // self.speed_y))
            elif not self.move_type == 1: self.angle = 90
            self.x = g.screen.get_width()
            self.y = randint(g.bounds[0], g.screen.get_height()-self.longestImgHeight+g.bounds[1])

    def hitbox(self):
        """Returns the current hitbox for the current image"""
        img = Game.instance.deer_imgs[img]
        if not self.angle == 0: img = pygame.transform.rotate(img, self.angle)
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
            self.y += self.speed_y
        elif self.move_type == 5:
            self.x -= g.game_speed,
            self.y += self.speed_y
        elif self.move_type == 6:
            self.y -= g.vertical_deer_speed
        elif self.move_type == 7:
            self.y += g.vertical_deer_speed
        elif self.move_type == 8:
            self.x += self.speed_x
            self.y -= g.vertical_deer_speed
        elif self.move_type == 9:
            self.x += self.speed_x
            self.y += g.vertical_deer_speed
        elif self.move_type == 10 or self.move_type == 11:
            self.x += g.game_speed//2
            if (self.speed_y < 0 and self.y <= g.bounds[0]) or (self.speed_y > 0 and self.y >= g.screen.get_height()-g.bounds[1]-self.hitbox().height):
                self.speed_y *= -1
                self.angle -= 90 #if running towards car: = 90 - self.angle
                self.angle *= 2
            else:
                self.y += self.speed_y
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
            self.img = 0 if self.img >= len(Game.instance.deer_imgs)-1 else self.img+1
            if move_type < 1 or move_type > 11:
                if not self.angle == 0: return pygame.transform.rotate(Game.instance.deer_imgs[0], self.angle)
                else: return Game.instance.deer_imgs[0]
            else: img = Game.instance.deer_imgs[self.img]
                if not self.angle == 0: return pygame.transform.rotate(Game.instance.deer_imgs[self.img], self.angle)
                else: return Game.instance.deer_imgs[self.img]
        else:
            #possibility 1 (easy):
            #if randint(0,1): return Game.instance.logo_imgs[self.img]
            #else: return Game.instance.instance.virus_imgs[self.img]
            
            #possibility 2 (advanced - with compound animation):
            ##both images
            #logo = Game.instance.logo_imgs[self.img]
            #virus = pygame.transform.rotate(Game.instance.virus_imgs[self.img], self.angle)
            ##variables
            #anim_len = Game.second*2
            #width = logo.get_width()
            #if self.key_frame == -1: self.key_frame = randint(0,anim_len-1)
            #frame_unit = 2*width // anim_len
            #offset = self.key_frame*frame_unit
            ##layers
            #img = pygame.transform.flip(logo, False, True).move(width-offset,0)
            #img.blit(virus,(0,0))
            #img.blit(logo, ((width+offset)%(2*width)-width,0))
            ##update non-temporary variables
            #self.angle += int(round(360 // anim_len))
            #self.key_frame += 1
            #self.key_frame %= anim_len
            #return img
            
            #possibility 3 (advanced - creates a realistic cylindric rotation around the y-axis (mathemtical z-axis)):
            logo = Game.instance.logo_imgs[self.img]
            virus = pygame.transform.rotate(Game.instance.virus_imgs[self.img], self.angle)
            #variables
            anim_len = Game.second*2
            width = logo.get_width()
            radius = sqrt((width//2)**2 + (width//2)**2)
            if self.key_frame == -1: self.key_frame = randint(0,anim_len-1)
            frame_unit = radius*2*Math.PI // anim_len
            offset = self.key_frame*frame_unit #Bogenmaß
            offset2 = offset+radius*(arcsin(0.5)//90*Math.PI) #angle*2//360*Math.PI*2; width//2//width = 0.5
            #logo_angled_width = sqrt(width**2 - ((sin(float(offset)/radius)-sin(float(offset2)/radius))*radius)**2) #even simpler:
            x_distance = cos(float(offset)/radius)*radius
            x_distance2 = cos(float(offset2)/radius)*radius
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
            self.angle += 360 // anim_len
            self.key_frame += 1
            self.key_frame %= anim_len
            return img

    def render(self, surface):
        #habe next_img() gleich hier benutzt
        """Blits the Deer on 'surface'."""
        surface.blit(self.next_img(), self.hitbox())

    def isAway(self):
        return self.x < -self.longestImgWidth or self.x > Game.instance.screen.get_width() or self.y < -self.longestImgHeight or self.y > Game.instance.screen.get_height()

class Game(object):
    """Weitere optionale Ideen zum Einbauen:
        - eine besondere Farbe für Rehe verschiedener move_typen
        - Autos auf der Gegenspur"""
    # is needed to call instance variables with other classes' methods
    instance = Game()
    second = 30
    playAsEmail = True
    
    def __init__(self, width=1200, height=400):
        """
        Initializes the Game instance. Arguments:
        width      = window width
        height     = window height
        """
        # Initialisierung
        self.width = width
        self.height = height

        self.startmenu = True
        self.pause = False
        self.gameOver = False
        self.restart = False
        self.survivedDeer = 0
        self.pos = 0
        self.bounds = (0,-0,0,-0) #up, down, left, right; determines the smallest possible distance from the player to the street edge
        self.deer_vertical_speed = (self.height+self.bounds[0]+self.bounds[1])/(Game.second*2) #used for Deer.move()

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Passée")
        pygame.mouse.set_visible(1)
        
        self.game_speed = 10
        self.player = Player(self.bounds[2], self.height//2, self.player_img)

        self.deer = []
        self.next_deer = 30
        self.next_deer_max = 90
        self.next_deer_min = 70
        
        # Tastendruck wiederholt senden, falls nicht losgelassen
        pygame.key.set_repeat(1, 30)
        self.clock = pygame.time.Clock()
        self.running = False
        
    def resetGameScene(self):
        """Resets all options and restarts the game."""
        #Game.instance = Game() #this only works, if this method and run() are staticmethods; begins always with startmenu
        self.player = Player(self.bounds[2], self.height//2, self.player_img)
        self.deer = []
        self.survivedDeer = 0
        self.startmenu = False
        self.pause = False
        self.gameOver = False
        self.game_speed = 10
        self.next_deer = 30
        self.next_deer_max = 90
        self.next_deer_min = 70
        self.running = False
        self.restart = True #will restart run()
        #self.clock = pygame.time.Clock()
    
    def createFrame(self, surface):
        """Draws onto the given Surface object."""
        #draw background
        surface.fill(pygame.Color(0,0,0,255))
        self.pos += self.game_speed
        self.pos %= self.scaled_street.get_width()
        surface.blit(self.get_street_img(self.pos), (0, 0))
        #draw player
        self.player.render(surface)
        #draw deer
        for deer in self.deer:
            deer.render(self.screen)
        #draw stats (score, time (with tenth seconds))
    
    def createPauseFrame(self, surface):
        """Displays the pause menu on the given Surface object."""
        self.createFrame(surface)
    
    def createGameOverFrame(self, surface):
        """Draws the Game Over screen on the given Surface object."""
        surface.fill(pygame.Color(0,0,0,255))
    
    def createStartMenuFrame(self, surface):
        """Paints the starting screen on the Surface object."""
        surface.fill(pygame.Color(0,0,0,255))
    
    def renderControls(self, surface):
        """Displays controls on a start menu of a Surface object."""
        createStartMenuFrame(surface)

    @staticmethod
    def load_graphics(): #we use it because you don't want global variables as I understood
        Game.instance.set_street_img(self.path("rue_n_clip.png"), self.path("rue_matrix_clip.png"))
        Game.instance.set_player_img(self.path("img", "voiture_r2.png"))
        Game.instance.set_deer_img([self.path("img", "chevreuil_m_gif%i.png" % i) for i in (1, 2, 3, 2)])
        service_colours = ["b", "r", "v", "vi"]
        service_lexicon = dict(zip(service_colours, ["NSA", "GCHQ", "BND", "DGSE"]))
        Game.instance.set_secret_service_imgs(service_colours, [self.path("virus_%s" % i) for i in service_colours], [self.path("%s_%s" % (service_lexicon[k], k)) for k in service_lexicon])
        #the toggled code could enable a maximum size for all images, given by the imgHeights list
        #maxHeights = [Game.instance.height//3*2]
        #imgHeights = [636]
        #bools = [imgHeights[i] > maxHeights[i] for i in range(len(imgHeights))]
        #Game.instance.set_images([(imgHeights[i] if bools[i] else maxHeights[i]) for i in range(len(bools))], self.path("allez.png"))
        Game.instance.set_images([Game.instance.height//3*2], self.path("allez.png"))
    
    #Road Adjustment
    def set_street_img(self, path, path2 = None):
        if not path2: path2 = path
        img = pygame.image.load(path).convert()
        img2 = pygame.image.load(path2).convert()
        #self.street_img # we don't need it anymore
        self.scaled_street = self.scale_street_img(img)
        self.scaled_street2 = self.scale_street_img(img2)

    def scale_street_img(self, street_img):
        width = street_img.get_width()
        height = street_img.get_height()
        scale = height // self.height #self.height // height
        img = pygame.transform.scale(street_img, (width // scale, self.height)) #scale * width
        return img

    def get_street_img(self, offset, matrixStyle = True): 
        surf = pygame.Surface((self.width, self.height))
        street = self.scaled_street if not matrixStyle else self.scaled_street2
        for x in range(-offset, self.width, street.get_width()):
            surf.blit(street, (x, 0))
        return surf

    #player presentation
    def set_player_img(path):
        img = pygame.image.load(path).convert_alpha()
        width = self.scale(img, self.height / 5.0)
        self.player_img = pygame.transform.scale(img, width, int(self.height/5.0))

    #obstacle presentation
    def set_deer_img(paths):
        imgs = [pygame.image.load(path).convert_alpha() for path in paths]
        width = self.scale(imgs[0], self.height / 5.0)
        self.deer_imgs = [pygame.transform.scale(img, width, int(self.height/5.0)) for img in imgs]
    
    def set_secret_service_imgs(keys, logoPathes, virusPathes):
        """Arg0 = key names for the images from both path lists
           Arg1 = the list of pathes for the secret service images
           Arg2 = the list of pathes for the virus images"""
        logoImgs = dict(zip(keys, [pygame.image.load(path).convert_alpha() for path in logoPathes]))
        width = self.scale(logoImg.itervalues(), self.height/5.0)
        self.logo_imgs = [pygame.transform.scale(logoImgs.itervalues()[i], width[i], int(self.height/5.0)) for i in range(len(logoImgs))]
        virusImgs = dict(zip(keys, [pygame.image.load(path).convert_alpha() for path in virusPathes]))
        width = self.scale(virusImgs.itervalues(), self.height/5.0)
        self.virus_imgs = [pygame.transform.scale(virusImgs.itervalues()[i], width[i], int(self.height/5.0)) for i in range(len(virusImgs))]
    
    #other graphical presentation
    def scale(self, imgs, relHeight = self.height):
        """Takes one or multiple images and one or multiple target heights and returns the corresponding width(s) and the scale factor."""
        if len(imgs) > 1:
            if not len(relHeight) > 1:
                scale = [relHeight // img.get_height() for img in imgs]
                widths = [int(round(img.get_width() * scale) for img in imgs]
            else:
                lst = imgs if not len(imgs) > len(relHeight) else relHeight
                scale = [relHeight[i] // img[i].get_height() for i in range(len(lst))]
                widths = [int(round(imgs[i].get_width() * scale[i]) for i in range(len(lst))]
                return pygame.transform.scale(imgs, ), widths
        else:
            if len(relHeight) > 1: relHeight = relHeight[0]
            scale = relHeight // imgs.get_height()
            width = int(round(imgs.get_width() * scale))
            return pygame.transform.scale(img, (width, relHeight)), width
    
    def set_images(heights, *paths):
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
        mt = randint(0,n)
        p = [3, 3, 2, 2, 1, 1] #probabilites, repeated to 12 elements, all elements' sum must be n+1
        for i in range(1,12):
            n -= p[i%len(p)]
            if mt > n:
                move_type = 1
        self.deer.append(Deer(move_type))

    #core function
    def run(self):
        renderControls = False
        intro = True
        #pos = 0 #it's easier to use an instance variable because I want to use it in dispatched functions
        tick = 0
        spawnCount = 0 #number of spawned deer
        maximumCount = 4 #more than 4 deer aren't allowed on the road
        maximumSpeed = 50
        newGame = True
        self.running = True
        while self.running:
            self.clock.tick(Game.second)
            #tick fits rather in the active gameplay section
            
            #EXIT CONDITION
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
            #PREPARE USER INPUT
            keys = pygame.key.get_pressed()

            #MODES
            if self.startmenu:
                if renderControls:
                    #USER input
                    if not len(keys) == 0:
                        self.renderControls = False
                    else: self.renderControls(self.screen)
                else:
                    #USER input
                    if keys[pygame.K_SPACE]: self.renderControls = True
                    elif keys[pygame.K_ESCAPE]:
                        self.running = False
                        break
                    elif not len(keys) == 0:
                        self.resetGameScene() #sets self.startmenu = False
                    else: self.createStartMenuFrame(self.screen)
            
            elif self.gameOver:
                #USER input
                if not len(keys) == 0:
                    if keys[pygame.K_ESCAPE]: startmenu = True
                    else: self.resetGameScene() #sets self.gameOver = False
                else: self.createGameOverFrame(self.screen)
            
            elif self.pause:
                #USER input
                if not len(keys) == 0:
                    if keys[pygame.K_ESCAPE]:
                        self.running = False
                        break
                    else: self.pause = False
                else: self.createPauseFrame(self.screen)

            else:
                tick += 1
                if not newGame:
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
                        if self.next_deer_max > Game.second*2:
                            self.next_deer_max -= 1
                        if self.next_deer_min > Game.second//4:
                            self.next_deer_min -= 1
                    if tick % int(Game.second*2.5) == 0 and self.game_speed < self.maximumSpeed:
                        self.game_speed += 1
                        #for deer in self.deer: #we don't need it anymore
                            #deer.game_speed = self.game_speed
                            #self.player.game_speed = self.game_speed
                
                    #SPAWN
                    if self.next_deer == 0 and spawnCount < maximumCount:
                        self.spawn_deer()
                        spawnCount += 1
                        self.next_deer = randint(self.next_deer_min, self.next_deer_max)
                    else:
                        self.next_deer -= 1
                
                    #self.gameOver = Game.instance.player.hasCrashed()
                    self.gameOver = self.player.hitbox.collidelist(self.deer)
                    for i in range(len(Game.instance.deer)):
                        deer = Game.instance.deer[i]
                        deer.move()
                        if deer.isAway():
                            Game.instance.deer.remove(i)
                            self.survivedDeer += 1
                            spawnCount -= 1
                
                #SETUP IMAGE BUFFER
                self.createFrame(self.screen)
                
                #INTRO
                if newGame:
                    allez = self.graphics[self.path("allez.png")]
                    self.screen.blit(allez, (self.width//2-allez.get_width//2, self.height//2-allez.get_height()//2))
                    if tick % (Game.second*2) == 0:
                        newGame = False

            #SHOW CONTENT
            pygame.display.flip()

        if not self.restart:
            #FINISH IT!
            sys.exit()
        else: self.restart = False

    def path(self, path):
        return os.path.join("img", path)

if __name__ == "__main__":
    #game = Game() #we don't need it anymore
    Game.load_graphics()
    while True: #will leave run() and execute it again, if self.restart == True
        Game.instance.run()
