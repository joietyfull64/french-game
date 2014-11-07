#!/usr/bin/env python2
# vim: set fileencoding=utf-8

import os.path
import sys
from math import ceil

import pygame

#we don't need Entity anymore, it would only hold two variables:
#class Entity:
##moved street and game_speed, see the comment at the end of this constructor
#    def __init__(self, x, y):
#        """Initializes the Entity instance. Arguments:
#        x     = The initial x coordinate of the Entity
#        y     = The initial y coordinate of the Entity
#        """
##Christoph:
##        self.speed = (0, 0) #beta - pixel speed, will be set individually for derived objects
##--
#        self.x = x
#        self.y = y
#        #self.position = (x, y) #beta - a compound variable to use for loops
#        #self.max_x = max_x
#        #self.max_y = max_y
#        #self.img = img #ist gleichzeitig die Größe 
#        #self.street = street # brauchen wir nicht, da wir schon self.screen in Game.instance haben
#        #self.game_speed = game_speed # hab ich in die Klasse Game in eine Klasseninstanz gemacht

class Player(Entity):

    def __init__(self, x, y, img):
        """Initializes the Player instance. Arguments:
        x     = The initial x coordinate of the Player
        y     = The initial y coordinate of the Player
        img   = The player's image
        """
        #super(Player, self).__init__(x,y)
#Christoph:
        self.x = x
        self.y = y
        self.set_image(img)
        self.boost = False #mehr dazu: unterer Kommentar
        self.boostFactor = 2.0 #when space is pressed, the movement will be faster by this factor

#    def decelerate(self):
#        """Decelerates the Player."""
#        leftBound = screen.width/2-max_x/2
#        self.speed[0] = -5 * (1 if not self.boost else self.boostFactor)
#        space = self.position[0] - leftBounds
#        if space < (self.speed[0] if not self.boost else (self.speed[0]*self.boostFactor)):
#            self.speed[0] = -space
#            self.position[0] = leftBounds
#        else:
#            self.position[0] += self.speed[0] if not self.boost else (self.speed[0]*self.boostFactor)
#
#    def accelerate(self):
#        """Accelerates the Player."""
#        rightBound = screenWidth/2+max_x/2
#        self.speed[0] = 5 * (1 if not self.boost else self.boostFactor)
#        space = screen.width-rightBound-self.img.get_width()-self.position[0]
#        if space < (self.speed[0] if not self.boost else (self.speed[0]*self.boostFactor)):
#            self.speed[0] = space
#            self.position[0] = screen.width-rightBound-self.img.get_width()
#        else:
#            self.position[0] += self.speed[0]
#
#    def up(self): #override
#        upperBound = screen.height/2-max_y/2
#        self.speed[1] = -5
#        space = self.position[1] - upperBound
#        if space < self.speed[1]: #upperBound muss nicht unbedingt 0 sein
#            self.speed[1] = -space
#            self.position[1] = upperBound
#        else:
#            self.position[1] += self.speed[1]
#        
#    def down(self): #override
#        lowerBound = screen.height/2+max_y/2
#        self.speed[1] = 5
#        space = screen.height-lowerBound-self.img.get_height()-self.position[1]
#        if space < self.speed[1]:
#            self.speed[1] = space
#            self.position[1] = screen.height-lowerBound-self.img.get_height()
#        else:
#            self.position[1] += self.speed[1]
#    #unused:
#    def hasCrashed(self):
#        interference = False
#        #the following is the simplest algorithm possibility but it takes a few more time to process
#        for deer in deer:
#            objects = (self, deer)
#            i = 0; i2 = 1
#            reverse = True
#            if sqrt(self.speed[0]**2 + self.speed[1]**2) < sqrt(deer.speed[0]**2 + deer.speed[1]**2):
#                i = 1; i2 = 0
#                reverse = False
#            collision1 = (float(objects[i].hitbox.get_width()), float(objects[i].hitbox.get_height())) #1 is for the quicker object
#            origin1 = (objects[i].hitbox.get_width(), objects[i].hitbox.get_height())
#            distance1 = (objects[i].speed[0], objects[i].speed[1])
#            collision2 = (float(objects[i2].hitbox.get_width()), float(objects[i2].hitbox.get_height()))
#            origin2 = (objects[i2].hitbox.get_width(), objects[i2].hitbox.get_height())
#            distance2 = (objects[i2].speed[0], objects[i2].speed[1])
#            objects = None
#            if abs(distance2[0]) > abs(distance2[1]):
#                i = 1; i2 = 0
#            else:
#                i = 0; i2 = 1
#            #checks the crash condition for every intermediate position with the pace of one pixel
#            #for the axis with the biggest distance value
#            sign = (distance2[i] >>> 31) | 1
#            speed2 = float(distance2[i2])/float(distance2[i])*sign
#            speed1 = float(distance1[i])/float(abs(distance2[i])) # 1/kleineEntfernungVomLangsamerenObjekt = Faktor
#            speed12 = float(distance1[i2])/float(abs(distance2[i]))
#            n = 1
#            while n < distance2[i] and not interference:
#                collision2[i] = origin2[i] + n*sign
#                collision2[i2] = origin2[i2] + int(n*speed2)
#                collision1[i] = origin1[i] + int(n*speed1)
#                collision1[i2] = origin1[i2] + int(n*speed12)
#                if not reverse:
#                    interference = Game.carCollidesDeer(collision1, collision2)
#                else: interference = Game.carCollidesDeer(collision2, collision1)
#                n += 1
#
#        self.speed = (0,0) #because we set the speed each time when calling down(), up(), right(), left(), accelerate() or decelerate()
#                            #this enables us to infer the used movement function
#        return interference
#--
    def up(self):
#Christoph: added conditional operator with self.boost and alignable street bounds
        """Moves the Player up."""
        if self.hitbox.top > self.street.top+self.bounds[0]:
            self.hitbox = self.hitbox.move(0, ((-Game.instance.screen.height / 30) if not self.boost else (-Game.instance.screen.height/30*self.boostFactor)) )

    def down(self):
        """Moves the Player down."""
        if self.hitbox.bottom < self.street.bottom+self.bounds[1]:
            self.hitbox = self.hitbox.move(0, ((Game.instance.screen.height / 30) if not self.boost else (Game.instance.screen.height/30*self.boostFactor)) )

    def accelerate(self):
        """Accelerates the Player."""
        if self.hitbox.right < self.street.right+self.bounds[3]:
#            print "ACC"
            self.hitbox = self.hitbox.move( ((Game.instance.screen.width / 120) if not self.boost else (Game.instance.screen.width/120*self.boostFactor)), 0)
#        else:
#            print self.hitbox.right, self.street.right
    def decelerate(self):
        """Decelerates the Player."""
        if self.hitbox.left > self.street.left+self.bounds[2]:
#            print "DEC"
            self.hitbox = self.hitbox.move( ((-Game.instance.screen.width / 120) if not self.boost else (-Game.instance.screen.width/120*self.boostFactor)), 0)

    def set_img(self, img):
        """Sets the image (and hitbox) of the Player. Argument:
        img = pygame.Surface containing the image for the Enity.
        """
        self.img = img
        self.hitbox = self.img.get_rect().move(self.x, self.y)

#Christoph:
    def get_img(self):
        """Returns: arg0 = self.img, arg1 = self.x, arg2 = self.y"""
        return self.img, self.x, self.y
#--

    def render(self, surface):
        """Blits the Player on 'surface'."""
        surface.blit(self.img, self.hitbox)

class Deer(Entity):
    #the x and y coordinate will be set randomly
    def __init__(self, move_type, imgs):
        """Initializes the Deer instance. Arguments:
        move_type = The movement type. See Deer.move().
        imgs = a tuple of images whose elementary images are switched
        """
        #super(Deer, self).__init__(*args)
        self.move_type = move_type
        self.img = -1 #animation index, -1 weil wir vor jedem Anzeigen zuerst diese Variable erhöhen
        self.imgs = imgs #animation
#Christoph:
        self.x = x
        self.y = y
        self.speed_x = 0 #we need it for movment_type 8 & 9
        self.speed_y = 0 #we need it for movement_type 4 & 5
        #self.hitbox = self.hitbox() #instead of self.hitbox use self.hitbox()
        self.longestImgWidth = imgs[0] #benutzt in isAway() und hier drunter
        self.longestImgHeight = imgs[0]
        if len(imgs) > 1:
            for i in imgs:
                if i.get_width() > self.longestImgWidth:
                    self.longestImgWidth = i.get_width()
                if i.get_height() > self.longestImgHeight:
                    self.longestImgHeight = i.get_height()
         #beta version:
#        # 0
#        if move_type == 0:
#            self.position = (screen.width, random((screen.height/2-max_y/2), (screen.height/2+max_y/2)))
#        # 1 & 2 & 3 & 4
#        elif not move_type == 5 and not move_type == 6 and not move_type == 7:
#            # 1 & 3
#            if move_type == 1 or move_type == 3:
#                self.position = (random(screen.width/2-max_x/2, screen.width/2+max_x/2), -self.img.get_height())
#            # 2 & 4
#            else:
#                self.position = (random(screen.width/2-max_x/2, screen.width/2+max_x/2), screen.height)
#            # 1 & 2
#            if move_type == 1 or move_type == 2:
#                self.speed = (0, (10 if move_type == 1 else -10) )
#            # 3 & 4
#            else:
#                #strahlensatz mit pythagoras
#                deerCenter = (self.position[0]+self.img.get_width()/2, self.position[1]+self.img.get_height()/2)
#                carCenter = (player.position[0]+player.hitbox.get_width()/2, player.position[1]+player.hitbox.get_height()/2)
#                xDistance = carCenter[0]-deerCenter[0]; yDistance = carCenter[1]-deerCenter[1]
#                distance = sqrt(xDistance**2 + yDistance**2)
#                x = float(xDistance)/float(distance)*10; y = float(yDistance)/float(distance)*10
#                self.speed = (x,y)
#        # 5 & 6
#        elif move_type == 5 or move_type == 6:
#            self.position = (screen.width, random((screen.height/2-max_y/2), (screen.height/2+max_y/2)))
#            # 5
#            if move_type == 5: self.speed = (gameSpeed, -10)
#            # 6
#            else: self.speed = (gameSpeed, 10)
#        # > 6
#        else:
#            self.position = (screen.width, random((screen.height/2-max_y/2), (screen.height/2+max_y/2)))
        #starting positions of the move_types
        g = Game.instance
        if self.move_type == 2:
            self.x = g.screen.width
            self.y = random(g.screen.height/2, g.screen.height+g.bounds[1]-self.longestImgHeight))
        elif self.move_type == 3:
            self.x = g.screen.width
            self.y = random(g.bounds[0], g.screen/2-self.longestImgHeight)
        elif self.move_type == 4:
            self.x = g.screen.width
            self.y = random(g.player.y,g.screen.height-self.longestImgheight+g.bounds[1])
            self.speed_y = ((g.player.y+g.player.hitbox.height/2)-(self.y+self.hitbox().height/2))/((g.player.x+g.player.hitbox.width/2)-(self.x+self.hitbox().width/2))*g.game_speed
        elif self.move_type == 5:
            self.x = g.screen.width
            self.y = random(g.bounds[0], g.player.y+g.player.height-self.longestImgHeight)
            self.speed_y = ((g.player.y+g.player.hitbox.height/2)-(self.y+self.hitbox().height/2))/((g.player.x+g.player.hitbox.width/2)-(self.x+self.hitbox().width/2))*g.game_speed
        elif self.move_type == 6 or self.move_type == 8:
            self.x = random(g.bounds[2], g.screen.width+g.bounds[3]-self.longestImgWidth)
            self.y = -imgs[0].height
        elif self.move_type == 8:
            self.x = random(g.bounds[2], g.screen.width+g.bounds[3]-self.longestImgWidth)
            self.y = -imgs[0].height
            self.speed_x = ((g.player.x+g.player.hitbox.width/2)-(self.x+self.hitbox().width/2))/((g.player.y+g.player.hitbox.height/2)-(self.y+self.hitbox().height/2))*g.screen.height/120
        elif self.move_type == 7 or self.move_type == 9:
            self.x = random(g.bounds[2], g.screen.width+g.bounds[3]-self.longestImgWidth)
            self.y = g.screen.height
        elif self.move_type == 9:
            self.x = random(g.bounds[2], g.screen.width+g.bounds[3]-self.longestImgWidth)
            self.y = g.screen.height
            self.speed_x = ((g.player.x+g.player.hitbox.width/2)-(self.x+self.hitbox().width/2))/((g.player.y+g.player.hitbox.height/2)-(self.y+self.hitbox().height/2))*g.screen.height/120
        else: #0 & 1 & 10 & 11
            if self.move_type == 10: self.speed_y = -g.vertical_deer_speed
            elif self.move_type == 11: self.speed_y = g.vertical_deer_speed
            self.x = g.screen.width
            self.y = random(g.bounds[0], g.screen.height-self.longestImgHeight+g.bounds[1])

    def hitbox():
        """Returns the current hitbox for the current image"""
        return self.imgs[img].get_rect().move(self.x, self.y)

    def move(self):
        """Moves the Deer according to its move_type. The movements are:
#--
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
#Christoph:
         #beta version with self.position and self.speed
#        # 1 & 2
#        if move_type == 1 or move_type == 2:
#            self.position[1] += self.speed[1]
#        # 3 & 4
#        elif move_type == 3 or move_type == 4:
#            for i in range(2):
#                self.position[i] += self.speed[i]
#        # 5 & 6
#        elif move_type == 5 or move_type == 6:
#            self.position[0] -= Game.gameSpeed
#            upperBounds = screen.height/2-max_y/2; lowerBounds = screen.height/2+max_y/2
#            # upper end
#            if self.speed[1] < 0 and (self.position[1] - upperBounds) < self.speed[1]:
#                self.position[1] = upperBounds
#                self.speed[1] *= -1
#            # lower end
#            elif self.speed[1] >= 0 and (screen.height-lowerBounds-self.img.get_height()-self.position[1]) < self.speed[1]:
#                self.position[1] = screen.height-lowerBounds-self.img.get_height()
#                self.speed[1] *= -1
#            # between ends
#            else: self.position[1] += self.speed[1]
#        # 0
#        elif move_type == 0:
#            self.position[0] -= Game.gameSpeed
#        # > 6
#        else:
#            self.position[0] -= Game.gameSpeed/2
#--
        #position changes for move_types
        g = Game.instance
        if self.move_type == 0:
            #self.hitbox = self.hitbox.move(-g.game_speed, 0) #instead, we only modify self.x and self.y
            self.x -= g.game_speed
#           print "MOVED %s" % self.hitbox
        elif self.move_type == 1:
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
            else:
                self.y += self.speed_y

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
        self.img += 1
        self.img %= len(self.imgs)
        return self.imgs[self.img]

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
    # is needed for staticmethods from this class and to call instance variables with other classes' methods
    instance = Game()
#--
    def __init__(self, width=1200, height=400):
        """
        Initializes the Game instance. Arguments:
        width      = window width
        height     = window height
        """
        # Initialisierung
#Christoph:
        self.startmenu = True
        self.pause = False
        self.gameOver = False
        self.survivedDeer = 0
        self.maximumSpeed = 50 #pixels per frame
#--
        self.width = width
        self.height = height
#Christoph:
        self.bounds = (0,-0,0,-0) #up, down, left, right; determines the smallest possible distance from the player to the street edge
        self.deer_vertical_speed = (self.height+self.bounds[0]+self.bounds[1])/120 #used for Deer.move()
#--

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Passée")
        pygame.mouse.set_visible(1)
        
        self.game_speed = 10
        #ich brauch noch eine Bildvariable für img
        self.player = Player(self.bounds[2], self.height//2, img)

        self.deer = []
        self.next_deer = 30
        self.next_deer_max = 90
        self.next_deer_min = 70
        
        # Tastendruck wiederholt senden, falls nicht losgelassen
        pygame.key.set_repeat(1, 30)
        self.clock = pygame.time.Clock()
        self.running = False

#Christoph:
    def resizeScreen(self, x = self.width, y = self.height):
        self.width = x
        self.height = y
        self.screen = pygame.display.set_mode((self.width, self.height))
        
    def resetGameScene(self): #set up everything
        self.player = Player(self.bounds[2], self.height//2, img) # player should become a class variable
        self.deer = []
        self.survivedDeer = 0
        self.startmenu = False
        self.pause = False
        self.gameOver = False
        self.speed = 10
        #self.clock = pygame.time.Clock()
    
    def createFrame(self, surface):
        #draw background
        pos = 0
        pos += self.game_speed
        pos %= self.scaled_street.get_width()
        self.screen.blit(self.get_street_img(pos), (0, 0))
        #draw player
        self.player.render(self.screen)
        #draw deer
        for deer in self.deer:
            deer.render(self.screen)
        #draw stats (score, time (with tenth seconds))
    
    def createPauseFrame(self):
        self.createFrame()
        # draw and write something on the screen
    
    def createGameOverFrame(self):
        # draw and write something on the screen
    
    def createStartMenuFrame(self):
        # draw and write something on the screen
    
    def renderControls(self, surface):
        # draw and write something on the screen
    
    #unused:
    def screenShrinks(self): #a funny idea, when playing -> the game window shrinks per 150 frames by 1 pixel for more difficulty
        if self.screen.width > 200 and (Game.frameCounter > 0 and Game.frameCounter % 150 == 0):
            self.resizeScreen(int(round(float((self.screen.width-1) // self.screen.width) * self.screen.height)), self.height-1)
    
    #unused
    def screenGrows(self):
        if self.screen.width < 1820 and (Game.frameCounter > 0 and Game.frameCounter % 150 == 0):
            self.resizeScreen(int(round(float(self.screen.width // (self.screen.width-1) * self.screen.height))), self.height+1)
    
    #unused:
    @staticmethod
    def carCollidesDeer(carPosition, deerPosition, deerIndex = 0):
        #prüfe alle vier Ecken beider Rechtecke, ob sie im jeweils anderen Rechteck drin sind
        collides = False
        corners = ( ((carPosition[0], carPosition[1]), (carPosition[0]+Game.instance.player.hitbox.get_width(), carPosition[1]), (carPosition[0]+Game.instance.player.hitbox.get_width(), carPosition[1]+Game.instance.player.hitbox.get_height()), (carPosition[0], carPosition[1]+Game.instance.player.hitbox.get_height())),
                ((deerPosition[0], deerPosition[1]), (deerPosition[0]+Game.instance.deer[deerIndex].hitbox().get_width(), deerPosition[1]), (deerPosition[0]+Game.instance.deer[deerIndex].hitbox().get_width(), deerPosition[1]+Game.instance.deer[deerIndex].hitbox().get_height()), (deerPosition[0], deerPosition[1]+Game.instance.deer[deerIndex].hitbox().get_height())))
        imgs = (player.hitbox, deer[deerIndex].hitbox())
        for i in range(2):
            for j in range(4):
                if Game.pointIntersectsRect(corners[i][j], (corners[i-1][0][0], corners[i-1][0][1], imgs[i-1].get_width(), imgs[i-1].get_height()) ):
                    collides = True
                    break
        return collides
    
    #unused:
    @staticmethod
    def pointIntersectsRect(point, *corners):
        return point[0] >= corners[0] and point[0] <= (corners[0]+corners[2]) and point[1] >= corners[1] and point[1] <= (corners[1]+corners[3])
#--
#SETTER & GETTER:
    #Road Adjustment
    def set_street_img(self, path):
        img = pygame.image.load(path)
        img = img.convert()
        self.street_img = img

        self.scaled_street = self.scale_street_img()

    def scale_street_img(self):
        width = self.street_img.get_width()
        height = self.street_img.get_height()
        scale = height // self.height #self.height // height
        img = pygame.transform.scale(self.street_img,
                (width // scale, self.height)) #scale * width
        return img

    def get_street_img(self, offset): 
        surf = pygame.Surface((self.width, self.height))
        for x in range(-offset, self.width, self.scaled_street.get_width()):
            surf.blit(self.scaled_street, (x, 0))
        return surf

    #player presentation
    def set_player_img(self, path):
        img = pygame.image.load(path)
        img = img.convert_alpha()
        scale = img.get_height() / (self.height / 5.0)
        img = pygame.transform.scale(img, (int(round(img.get_width() / scale)),
            int(round(img.get_height() / scale))))
        self.player.set_img(img)

    def set_deer_img(self, paths):
        imgs = [pygame.image.load(path).convert_alpha() for path in paths]
        scale = imgs[0].get_height() / (self.height / 5.0)
        imgs = [pygame.transform.scale(img, (int(round(img.get_width() / scale)), int(round(img.get_height() / scale)))) for img in imgs]
        self.deer_imgs = imgs
        for deer in self.deer:
            deer.set_imgs(imgs)

    def spawn_deer(self):
        if randint(0, 1):
        # Laters
        #if self.speed < 20:
        #move_type = randint(0, 2)
        #elif self.speed < 30:
        #move_type = randint(0, 4)
        #else:
        #move_type = randint(0, 7)
        self.deer.append(Deer(0, self.width, randint(0, self.height - self.deer_imgs[0].get_height()), self.scaled_street.get_rect(), self.speed))
        self.deer[-1].set_imgs(self.deer_imgs)
#---

    #core function
    #RECHECK
    def run(self):
#Christoph:
        renderControls = False
        #pos = 0 #is already included in the function before display.flip(), see below
        tick = 0
        spawnCount = 0 #number of spawned deer
        maximumCount = 4 #more than 4 deer aren't allowed on the road
#--
        self.running = True
        while self.running:
            self.clock.tick(30)
            tick += 1
            
            #PREPARE USER INPUT
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
            keys = pygame.key.get_pressed()
#Christoph:
            if self.startmenu:
                if renderControls:
                    #USER input
                    if keys[pygame.K_RIGHT]:
                        renderControls = False
                        self.renderControls()
                else:
                    #USER input
                    if keys[pygame.K_SPACE]: renderControls = True
                    elif not len(keys) == 0:
                        renderControls = False
                        self.resetGameScene()
                        self.createStartMenuFrame()
            
            elif self.gameOver:
                # #USER input
                if keys[pygame.K_RIGHT]:
                    if keys[pygame.K_ESCAPE]: startmenu = True
                    else: self.resetGameScene()
                
                ##New (4.11.):
                self.createGameOverFrame()
            
            elif self.pause:
                # #USER input
                if not len(keys) == 0:
                
                self.createPauseFrame()
            
            else:
#--
                ##USER INPUT:
    
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
#Christoph:
                if keys[pygame.K_SPACE]:
                    Game.instance.player.boost = True # self.boost ist schon in accelerate() und decelerate() eingebaut
                else: Game.instance.player.boost = False # WICHTIG
#--
                if keys[pygame.K_ESCAPE]:
                    pause = True #fänd ich gut, vielleicht kann man dann von dort beenden
#Christoph:
                #while (spawn-condition): spawnCount+=1
                    # if spawnCount:
                    #   for i in range(spawnCount):
                    #       spawnedDeer.add(Deer(...))
                    #   spawnCount = 0
                    
                #GAME routine
                #self.gameOver = Game.instance.player.hasCrashed()
                for deer in Game.instance.deer:
                    deer.move()
                    if deer.isAway():
                        Game.instance.deer.remove(deer)
                        self.survivedDeer += 1
#--
                if tick % 90 == 0:
                    if self.next_deer_max > 30:
                        self.next_deer_max -= 1
                    if self.next_deer_min > 15:
                        self.next_deer_min -= 1
                if tick % 75 == 0 and self.speed < 50:
                    self.speed += 1
                    for deer in self.deer:
                        deer.game_speed = self.speed
                        self.player.game_speed = self.speed

                if self.next_deer == 0:
                    self.spawn_deer()
                    self.next_deer = randint(self.next_deer_min, self.next_deer_max)
                else:
                    self.next_deer -= 1

                for deer in self.deer:
                    deer.move()
                
            ##SETUP IMAGE BUFFER
            self.createFrame()
            #pygame.draw.polygon(self.screen, (120, 120, 120), self.street)

            ##SHOW CONTENT
            pygame.display.flip()

if __name__ == "__main__":
    #game = Game() #we don't need it anymore
    #Game.instance.set_player_img(os.path.join("img", "voiture_r2.png"))
    #Game.instance.set_street_img(os.path.join("img", "rue_n_clip.png"))
    Game.instance.run()
