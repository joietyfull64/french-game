#!/usr/bin/env python2
# vim: set fileencoding=utf-8

import os.path
import sys
from math import ceil

#TODO:   - load pictures and createFrame methods
#        - display method for Deer
#        - animation components in spawn_deer()

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
            self.hitbox = self.hitbox.move(0, ((-Game.instance.screen.height / 30) if not self.boost else (-Game.instance.screen.height/30*self.boostFactor)) )

    def down(self):
        """Moves the Player down."""
        if self.hitbox.bottom < Game.instance.screen.bottom+self.bounds[1]:
            self.hitbox = self.hitbox.move(0, ((Game.instance.screen.height / 30) if not self.boost else (Game.instance.screen.height/30*self.boostFactor)) )

    def accelerate(self):
        """Accelerates the Player."""
        if self.hitbox.right < Game.instance.screen.right+self.bounds[3]:
#            print "ACC"
            self.hitbox = self.hitbox.move( ((Game.instance.screen.width / 120) if not self.boost else (Game.instance.screen.width/120*self.boostFactor)), 0)
#        else:
#            print self.hitbox.right, Game.instance.screen.right
    def decelerate(self):
        """Decelerates the Player."""
        if self.hitbox.left > Game.instance.screen.left+self.bounds[2]:
#            print "DEC"
            self.hitbox = self.hitbox.move( ((-Game.instance.screen.width / 120) if not self.boost else (-Game.instance.screen.width/120*self.boostFactor)), 0)

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
        self.imgs = imgs
        self.angle = 0 # the angle after which the, by default vertical, image is rotated counterclockwise
        
        self.x = x
        self.y = y
        self.speed_x = 0 #we need it for movment_type 8 & 9
        self.speed_y = 0 #we need it for movement_type 4 & 5
        #self.hitbox = self.hitbox() #instead of self.hitbox use self.hitbox()
        self.longestImgWidth = imgs[0].get_width() #benutzt in isAway() und hier drunter
        self.longestImgHeight = imgs[0].get_height()
        if len(imgs) > 1:
            for i in imgs:
                if i.get_width() > self.longestImgWidth:
                    self.longestImgWidth = i.get_width()
                if i.get_height() > self.longestImgHeight:
                    self.longestImgHeight = i.get_height()

        #start positions of the move_types and picture angle calculations
        g = Game.instance
        self.angle = -90
        if self.move_type == 2:
            self.x = g.screen.width
            self.y = randint(g.screen.height/2, g.screen.height+g.bounds[1]-self.longestImgHeight))
            self.angle += tan(g.game_speed / g.vertical_deer_speed)
        elif self.move_type == 3:
            self.x = g.screen.width
            self.y = randint(g.bounds[0], g.screen/2-self.longestImgHeight)
            self.angle -= tan(g.game_speed / g.vertical_deer_speed)
        elif self.move_type == 4:
            self.x = g.screen.width
            self.y = randint(g.player.y,g.screen.height-self.longestImgheight+g.bounds[1])
            hitbox = self.hitbox()
            self.speed_y = ((g.player.y+g.player.hitbox.height/2)-(self.y+hitbox.height/2))/((g.player.x+g.player.hitbox.width/2)-(self.x+hitbox.width/2))*g.game_speed
            self.angle += tan(g.game_speed / self.speed_y) # self.speed_y is always positive
        elif self.move_type == 5:
            self.x = g.screen.width
            self.y = randint(g.bounds[0], g.player.y+g.player.height-self.longestImgHeight)
            hitbox = self.hitbox()
            self.speed_y = ((g.player.y+g.player.hitbox.height/2)-(self.y+hitbox.height/2))/((g.player.x+g.player.hitbox.width/2)-(self.x+hitbox.width/2))*g.game_speed
            self.angle -= tan(g.game_speed / -self.speed_y)
        elif self.move_type == 6:
            self.x = randint(g.bounds[2], g.screen.width+g.bounds[3]-self.longestImgWidth)
            self.y = -imgs[0].height
            self.angle = 0
        elif self.move_type == 8:
            self.x = randint(g.bounds[2], g.screen.width+g.bounds[3]-self.longestImgWidth)
            self.y = -imgs[0].height
            hitbox = self.hitbox()
            self.speed_x = ((g.player.x+g.player.hitbox.width/2)-(self.x+hitbox.width/2))/((g.player.y+g.player.hitbox.height/2)-(self.y+hitbox.height/2))*(g.screen.height/120)
            self.angle = (((self.speed_x >> -1)^-1)|1)*tan(g.vertical_deer_speed / self.speed_x)
        elif self.move_type == 7:
            self.x = randint(g.bounds[2], g.screen.width+g.bounds[3]-self.longestImgWidth)
            self.y = g.screen.height
            self.angle = 180
        elif self.move_type == 9:
            self.x = randint(g.bounds[2], g.screen.width+g.bounds[3]-self.longestImgWidth)
            self.y = g.screen.height
            hitbox = self.hitbox()
            self.speed_x = ((g.player.x+g.player.hitbox.width/2)-(self.x+hitbox.width/2))/((g.player.y+g.player.hitbox.height/2)-(self.y+hitbox.height/2))*(g.screen.height/120)
            self.angle = 180 + ((self.speed_x >> -1)|1)*tan(g.vertical_deer_speed / self.speed_x)
        else: #0 & 1 & 10 & 11
            gs = g.game_speed/2
            if self.move_type == 10:
                self.speed_y = -g.vertical_deer_speed
                self.angle += tan(gs / self.speed_y))
            elif self.move_type == 11:
                self.speed_y = g.vertical_deer_speed
                self.angle -= tan(gs / self.speed_y))
            elif not self.move_type == 1: self.angle = 90
            self.x = g.screen.width
            self.y = randint(g.bounds[0], g.screen.height-self.longestImgHeight+g.bounds[1])
        if not self.angle == 0 and not Game.playAsEmail: set_angle(self.angle)
        else: self.angle = 0
    
    def set_angle(self, value):
        self.imgs = [pygame.transform.rotate(img, self.angle))) for img in self.imgs]

    def hitbox(self):
        """Returns the current hitbox for the current image"""
        return self.imgs[img].get_rect().move(self.x, self.y)

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
            self.x -= g.game_speed/2
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
            self.x += g.game_speed/2
            if (self.speed_y < 0 and self.y <= g.bounds[0]) or (self.speed_y > 0 and self.y >= g.screen.height-g.bounds[1]-self.hitbox().height):
                self.speed_y *= -1
                self.angle -= 90 #if running towards car: = 90 - self.angle
                self.angle *= 2
                self.imgs = [pygame.transform.rotate(img, self.angle) for img in self.imgs]
            else:
                self.y += self.speed_y
        else: # 0 & others
            self.x -= g.game_speed
#       print "MOVED %s" % self.hitbox

    def set_imgs(self, imgs, x = self.x, y = self.y):
        """Sets the image of the Deer. Argument:
            imgs = List of 'pygame.Surface's containing the image for the Enity.
            x    = the new x coordinate of the upper left corner
            y    = the new y coordinate of the upper right corner
        """
        self.imgs = imgs
        self.x = x
        self.y = y

#Christoph:
    def get_imgs(self):
        """Returns the image array as first argument, the x coordinate as second argument
        and the y coordinate as third argument."""
        return self.imgs, self.x, self.y
        
    def get_img(self, index):
        return self.imgs[index]
#--

    def next_img(self):
        """Returns the next image in the animation"""
        if not Game.playAsEmail:
            self.img = 0 if self.img >= len(self.imgs)-1 else self.img+1
            return self.imgs[self.img]
        else:
            #possibility 1 (easy):
            if randint(0,1): return Game.instance.logo_imgs[randint(0,3)]
            else: return Game.instance.instance.virus_imgs[randint(0,3)]
            #possibility 2 ():
            index = randint(0,3)
            logo = Game.instance.logo_imgs[index]
            virus = Game.instance.virus_imgs[index]
            width = virus.get_width()
            img = pygame.transform.flip[logo, False, True].move(width-self.img,0)
            self.img += 3 #for 30 fps
            self.img %= 2*width

    def render(self, surface):
        #habe next_img() gleich hier benutzt
        """Blits the Deer on 'surface'."""
        surface.blit(self.next_img(), self.hitbox())

#Christoph:
    def isAway(self):
        return self.x < -self.longestImgWidth or self.x > Game.instance.screen.width or self.y < -self.longestImgHeight or self.y > Game.instance.screen.height
#--

class Game(object):
    """Weitere optionale Ideen zum Einbauen:
        - eine besondere Farbe für Rehe verschiedener move_typen
        - Autos auf der Gegenspur"""
#Christoph:
    # is needed to call instance variables with other classes' methods
    instance = Game()
    second = 30
    playAsEmail = True
#--
    def __init__(self, width=1200, height=400):
        """
        Initializes the Game instance. Arguments:
        width      = window width
        height     = window height
        """
        # Initialisierung
        self.width = width
        self.height = height
#Christoph:
        self.startmenu = True
        self.pause = False
        self.gameOver = False
        self.restart = False
        self.survivedDeer = 0
        self.pos = 0
        self.bounds = (0,-0,0,-0) #up, down, left, right; determines the smallest possible distance from the player to the street edge
        self.deer_vertical_speed = (self.height+self.bounds[0]+self.bounds[1])/(Game.second*2) #used for Deer.move()
#--
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

#Christoph:
#    #does not resize the content
#    def resizeScreen(self, x = self.width, y = self.height):
#        self.width = x
#        self.height = y
#        self.screen = pygame.display.set_mode((self.width, self.height))
        
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
        
    
#    #unused:
#    def screenShrinks(self): #a funny idea, when playing -> the game window shrinks per 150 frames by 1 pixel for more difficulty
#        if self.screen.width > 200 and (Game.frameCounter > 0 and Game.frameCounter % 150 == 0):
#            self.resizeScreen(int(round(float((self.screen.width-1) // self.screen.width) * self.screen.height)), self.height-1)
    
#    #unused
#    def screenGrows(self):
#        if self.screen.width < 1820 and (Game.frameCounter > 0 and Game.frameCounter % 150 == 0):
#            self.resizeScreen(int(round(float(self.screen.width // (self.screen.width-1) * self.screen.height))), self.height+1)
    
#    #unused:
#    @staticmethod
#    def carCollidesDeer(carPosition, deerPosition, deerIndex = 0):
#        #prüfe alle vier Ecken beider Rechtecke, ob sie im jeweils anderen Rechteck drin sind
#        collides = False
#        hitbox = hitbox()
#        corners = ( ((carPosition[0], carPosition[1]), (carPosition[0]+Game.instance.player.hitbox.get_width(), carPosition[1]), (carPosition[0]+Game.instance.player.hitbox.get_width(), carPosition[1]+Game.instance.player.hitbox.get_height()), (carPosition[0], carPosition[1]+Game.instance.player.hitbox.get_height())),
#                ((deerPosition[0], deerPosition[1]), (deerPosition[0]+Game.instance.deer[deerIndex].hitbox.get_width(), deerPosition[1]), (deerPosition[0]+Game.instance.deer[deerIndex].hitbox.get_width(), deerPosition[1]+Game.instance.deer[deerIndex].hitbox.get_height()), (deerPosition[0], deerPosition[1]+Game.instance.deer[deerIndex].hitbox.get_height())))
#        imgs = (player.hitbox, deer[deerIndex].hitbox)
#        for i in range(2):
#            for j in range(4):
#                if Game.pointIntersectsRect(corners[i][j], (corners[i-1][0][0], corners[i-1][0][1], imgs[i-1].get_width(), imgs[i-1].get_height()) ):
#                    collides = True
#                    break
#        return collides
    
#    #unused:
#    @staticmethod
#    def pointIntersectsRect(point, *corners):
#        return point[0] >= corners[0] and point[0] <= (corners[0]+corners[2]) and point[1] >= corners[1] and point[1] <= (corners[1]+corners[3])
#--
#SETTER & GETTER:
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
            if len(relHeight) <= 1:
                scale = [relHeight / img.get_height() for img in imgs]
                return [int(round(img.get_width() * scale) for img in imgs], scale
            else:
                lst = imgs if not len(imgs) > len(relHeight) else relHeight
                scale = [relHeight[i] / img[i].get_height() for i in range(len(lst))]
                return [int(round(imgs[i].get_width() * scale[i]) for i in range(len(lst))], scale
        else:
            if len(relHeight) > 1: relHeight = relHeight[0]
            scale = relHeight / imgs.get_height()
            return int(round(imgs.get_width() * scale)), scale
    
    def set_images(heights, *paths):
        imgs = dict(zip(paths, [pygame.image.load(path).convert_alpha() for path in paths]))
        widths = self.scale(imgs.itervalues(), heights)
        self.graphics = [pygame.transform.scale(imgs.itervalues()[i], widths[i], heights[i]) for i in range(len(imgs))]

    def spawn_deer(self):
        if randint(0, 1):
            move_type = 0
            if self.game_speed < 20:
                move_type = randint(0, 2)
            elif self.game_speed < 30:
                move_type = randint(0, 4)
            else:
                move_type = randint(0, 11)
            if randint(0,1): return Game.instance.logo_imgs[randint(0,3)]
            else: return Game.instance.instance.virus_imgs[randint(0,3)]
            #possibility 2 ():
            index = randint(0,3)
            imgs = self.deer_imgs[0]
            if move_type == 1:
                imgs = self.deer_imgs
            self.deer.append(Deer(move_type, imgs))
            self.deer[-1].set_imgs(self.deer_imgs)
#---

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
            
            #PREPARE USER INPUT
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
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
                if not newGame:
                    tick += 1
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
                        if self.next_deer_min > Game.second/4:
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
                
                #INTRO
                else:
                    #add something to the screen
                    if tick % (Game.second*2) == 0:
                        newGame = False
                
                #SETUP IMAGE BUFFER
                self.createFrame(self.screen)

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
    Game.instance.set_street_img(self.path("rue_n_clip.png"), self.path("img", "rue_matrix_clip.png"))
    Game.instance.set_player_img(self.path("img", "voiture_r2.png"))
    Game.instance.set_deer_img([self.path("img", "chevreuil_m_gif%i.png" % i) for i in (1, 2, 3, 2)])
    service_colours = ["b", "r", "v", "vi"]
    service_lexicon = dict(zip(service_colours, ["NSA", "GCHQ", "BND", "DGSE"]))
    Game.instance.set_secret_service_imgs(service_colours, [self.path("virus_%s" % i) for i in service_colours], [self.path("%s_%s" % (service_lexicon[k], k)) for k in service_lexicon])
    Game.instance.set_images(self.path([], "allez.png"))
    while True: #will leave run() and execute it again, if self.restart == True
        Game.instance.run()
