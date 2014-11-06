#!/usr/bin/env python2
# vim: set fileencoding=utf-8

import os.path
import sys
from math import ceil

import pygame

#Christoph: ich gehe davon aus, dass die Position eines Objekts immer die obere linke Ecke ist
#img.get_width() - Länge des Bildes, img.get_height() - Höhe des Bildes
#screen.width - Länge des Fensters, screen,height - Höhe des Fensters
#random(arg1, arg2) - a random value in the given range; arg1 - inclusive start of range, arg2 - inclusive end of range

class Entity(object):
    def __init__(self, max_x, max_y, img = None):
        """
        Initializes the Entity instance. Arguments:
        x     = The initial x coordinate of the Entity
        y     = The initial y coordinate of the Entity
        max_x = The maximum x coordinate the Entity can go to
        max_y = The maximum y coordinate the Entity can go to
        img   = A pygame.Surface containing the image for the Entity.
                Defaults to None. Can be changed later.
        """
#Christoph:
        self.speed = (0, 0) #pixel speed, will be set individually for derived objects
#--
        #self.x = 0
        #self.y = 0 #self.position = (x, y)
        self.max_x = max_x
        self.max_y = max_y
        self.img = img #ist gleichzeitig die Größe 

    def up(self):
        """Moves the Entity up."""
#       if self.y == 0: #glitchy
#           return
#       self.y -= 10 #Literale (hardgecodete Werte) sind nur im Notfall notwendig
        upperBound = screen.height/2-max_y/2
        self.speed[1] = -10
        space = self.position[1] - upperBounds
        if space < self.speed[1]: #upperBound muss nicht unbedingt 0 sein
            self.speed[1] = -space
            self.position[1] = upperBound
        else:
            self.position[1] += self.speed[1]

    def down(self):
        """Moves the Entity down."""
#       if self.y == self.max_y: #glitchy
#           return
#       self.y += 10
        lowerBound = screen.height/2+max_y/2
        self.speed[1] = 10
        space = screen.height-lowerBound-self.img.get_height()-self.position[1]
        if space < self.speed[1]:
            self.speed[1] = space
            self.position[1] = screen.height-lowerBound-self.img.get_height()
        else:
            self.position[1] += self.speed[1]
#Christoph:
    def left(self):
        leftBound = screen.width/2-max_x/2
        self.speed[0] = -10
        space = self.position[0] - leftBounds
        if space < self.speed[0]:
            self.speed[0] = -space
            self.position[0] = leftBounds
        else:
            self.position[0] += self.speed[0]

    def right(self):
        rightBound = screen.width/2+max_x/2
        self.speed[0] = 10
        space = screen.width-rightBound-(self.img.get_width()+self.position[0])
        if space < speed[0]:
            self.speed[] = space
            self.position[0] = screen.width-rightBound-img.get_width()
        else:
            self.position[0] += speed[0]
#--

    def render(self, surface):
        """Blits the Entity on 'surface'."""
        surface.blit(self.img, self.position)

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
#Christoph:
        self.boost = False #mehr dazu: unterer Kommentar
        self.boostFactor = 2.0 #when space is pressed, the movement will be faster by this factor
        self.speed = (5,5)
#--

    def decelerate(self):
        """Decelerates the Player."""
#       if self.x == 0:
#           return
#       self.x -= 5
        leftBound = screen.width/2-max_x/2
        self.speed[0] = -5 * (1 if not self.boost else self.boostFactor)
        space = self.position[0] - leftBounds
        if space < (self.speed[0] if not self.boost else (self.speed[0]*self.boostFactor)):
            self.speed[0] = -space
            self.position[0] = leftBounds
        else:
            self.position[0] += self.speed[0] if not self.boost else (self.speed[0]*self.boostFactor)

    def accelerate(self):
        """Accelerates the Player."""
#        if self.x == self.max_x:
#           return
#       self.x += 5
        rightBound = screenWidth/2+max_x/2
        self.speed[0] = 5 * (1 if not self.boost else self.boostFactor)
        space = screen.width-rightBound-self.img.get_width()-self.position[0]
        if space < (self.speed[0] if not self.boost else (self.speed[0]*self.boostFactor)):
            self.speed[0] = space
            self.position[0] = screen.width-rightBound-self.img.get_width()
        else:
            self.position[0] += self.speed[0]

#Christoph:
    def up(self): #override
        upperBound = screen.height/2-max_y/2
        self.speed[1] = -5
        space = self.position[1] - upperBound
        if space < self.speed[1]: #upperBound muss nicht unbedingt 0 sein
            self.speed[1] = -space
            self.position[1] = upperBound
        else:
            self.position[1] += self.speed[1]
        
    def down(self): #override
        lowerBound = screen.height/2+max_y/2
        self.speed[1] = 5
        space = screen.height-lowerBound-self.img.get_height()-self.position[1]
        if space < self.speed[1]:
            self.speed[1] = space
            self.position[1] = screen.height-lowerBound-self.img.get_height()
        else:
            self.position[1] += self.speed[1]
    #unused:
    def hasCrashed(self):
        interference = False
        #the following is the simplest algorithm possibility but it takes a few more time to process
        for deer in deer:
            objects = (self, deer)
            i = 0; i2 = 1
            reverse = True
            if sqrt(self.speed[0]**2 + self.speed[1]**2) < sqrt(deer.speed[0]**2 + deer.speed[1]**2):
                i = 1; i2 = 0
                reverse = False
            collision1 = (float(objects[i].img.get_width()), float(objects[i].img.get_height())) #1 is for the quicker object
            origin1 = (objects[i].img.get_width(), objects[i].img.get_height())
            distance1 = (objects[i].speed[0], objects[i].speed[1])
            collision2 = (float(objects[i2].img.get_width()), float(objects[i2].img.get_height()))
            origin2 = (objects[i2].img.get_width(), objects[i2].img.get_height())
            distance2 = (objects[i2].speed[0], objects[i2].speed[1])
            objects = None
            if abs(distance2[0]) > abs(distance2[1]):
                i = 1; i2 = 0
            else:
                i = 0; i2 = 1
            #checks the crash condition for every intermediate position with the pace of one pixel
            #for the axis with the biggest distance value
            sign = (distance2[i] >>> 31) | 1
            speed2 = float(distance2[i2])/float(distance2[i])*sign
            speed1 = float(distance1[i])/float(abs(distance2[i])) # 1/kleineEntfernungVomLangsamerenObjekt = Faktor
            speed12 = float(distance1[i2])/float(abs(distance2[i]))
            n = 1
            while n < distance2[i] and not interference:
                collision2[i] = origin2[i] + n*sign
                collision2[i2] = origin2[i2] + int(n*speed2)
                collision1[i] = origin1[i] + int(n*speed1)
                collision1[i2] = origin1[i2] + int(n*speed12)
                if not reverse:
                    interference = Game.carCollidesDeer(collision1, collision2)
                else: interference = Game.carCollidesDeer(collision2, collision1)
                n += 1

        self.speed = (0,0) #because we set the speed each time when calling down(), up(), right(), left(), accelerate() or decelerate()
                            #this enables us to infer the used movement function
        return interference
#--

class Deer(Entity):
    def __init__(self, move_type, *args):
        """
        Initializes the Deer instance. Arguments:
        move_type = The movement type. See Deer.move().
        x         = The initial x coordinate of the Deer
        y         = The initial y coordinate of the Deer
        max_x     = The maximum x coordinate the Deer can go to (x movement space)
        max_y     = The maximum y coordinate the Deer can go to (y movement space)
        img       = A pygame.Surface containing the image for the Deer.
                    Defaults to None. Can be changed later.
        """
        super(Deer, self).__init(*args) #__init__
        self.move_type = move_type
#Christoph:
        # 0
        if move_type == 0:
            self.position = (screen.width, random((screen.height/2-max_y/2), (screen.height/2+max_y/2)))
        # 1 & 2 & 3 & 4
        elif not move_type == 5 and not move_type == 6 and not move_type == 7:
            # 1 & 3
            if move_type == 1 or move_type == 3:
                self.position = (random(screen.width/2-max_x/2, screen.width/2+max_x/2), -self.img.get_height())
            # 2 & 4
            else:
                self.position = (random(screen.width/2-max_x/2, screen.width/2+max_x/2), screen.height)
            # 1 & 2
            if move_type == 1 or move_type == 2:
                self.speed = (0, (10 if move_type == 1 else -10) )
            # 3 & 4
            else:
                #strahlensatz mit pythagoras
                deerCenter = (self.position[0]+self.img.get_width()/2, self.position[1]+self.img.get_height()/2)
                carCenter = (player.position[0]+player.img.get_width()/2, player.position[1]+player.img.get_height()/2)
                xDistance = carCenter[0]-deerCenter[0]; yDistance = carCenter[1]-deerCenter[1]
                distance = sqrt(xDistance**2 + yDistance**2)
                x = float(xDistance)/float(distance)*10; y = float(yDistance)/float(distance)*10
                self.speed = (x,y)
        # 5 & 6
        elif move_type == 5 or move_type == 6:
            self.position = (screen.width, random((screen.height/2-max_y/2), (screen.height/2+max_y/2)))
            # 5
            if move_type == 5: self.speed = (gameSpeed, -10)
            # 6
            else: self.speed = (gameSpeed, 10)
        # > 6
        else:
            self.position = (screen.width, random((screen.height/2-max_y/2), (screen.height/2+max_y/2)))

    def move(self):
        """
        Moves the Deer according to its move_type. The movements are:
        0 = No movement (no animation but moves parallel to the street)
        1 = walks continually up (right-up-walking animation)
        2 = Walks continually down (right-down-walking animation)
        3 = Like 1, but aims for player's car at spawn time (left/right-up-walking animation)
        4 = Like 2, but aims for player's car at spawn time (left/right-down-walking animation)
        5 = Walks between (screen.height/2-max_y/2) and (screen.height/2+max_y/2) (yDistance) - starts going up
        6 = Walks between (screen.height/2-max_y/2) and (screen.height/2+max_y/2) (yDistance) - starts going down
        7 = Like 0 only slower (up-walking animation)
        """
        # 1 & 2
        if move_type == 1 or move_type == 2:
            self.position[1] += self.speed[1]
        # 3 & 4
        elif move_type == 3 or move_type == 4:
            for i in range(2):
                self.position[i] += self.speed[i]
        # 5 & 6
        elif move_type == 5 or move_type == 6:
            self.position[0] -= Game.gameSpeed
            upperBounds = screen.height/2-max_y/2; lowerBounds = screen.height/2+max_y/2
            # upper end
            if self.speed[1] < 0 and (self.position[1] - upperBounds) < self.speed[1]:
                self.position[1] = upperBounds
                self.speed[1] *= -1
            # lower end
            elif self.speed[1] >= 0 and (screen.height-lowerBounds-self.img.get_height()-self.position[1]) < self.speed[1]:
                self.position[1] = screen.height-lowerBounds-self.img.get_height()
                self.speed[1] *= -1
            # between ends
            else: self.position[1] += self.speed[1]
        # 0
        elif move_type == 0:
            self.position[0] -= Game.gameSpeed
        # > 6
        else:
            self.position[0] -= Game.gameSpeed/2
    
    def isAway(self):
        return self.position[0] < -self.img.width-1 or self.position[0] > screen.width+1 or self.position[1] < -self.img.height-1 or self.position[1] > screen.height+1
#--

class Game(object):
    """Weitere optionale Ideen zum Einbauen:
        - eine besondere Farbe für Rehe des move_type 5/6 und des move_type 3/4
        - Autos auf der Gegenspur"""
#Christoph:
    # is needed for staticmethods from this class or possibly for other methods
    player = Player(0, self.height // 2, self.width, self.height)
    deer = []
#--
    
    def __init__(self, width=800, height=600):
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

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Passée")
        pygame.mouse.set_visible(1)
        
        #OLD varibles?
        self.player = Player(0, self.height // 2, self.width, self.height)
        self.deer = []
        
        # Tastendruck wiederholt senden, falls nicht losgelassen
        pygame.key.set_repeat(1, 30)
        self.clock = pygame.time.Clock()
        self.running = False
        self.speed = 10 # änder mal den Namen auf gameSpeed oder meinetwegen game_speed

#Christoph:
    def resetGameScene(self): #set up everything
        Game.player = Player(...) # player should become a class variable
        Game.deer = []
        self.roadOffset = 0
        self.survivedDeer = 0
        self.startmenu = False
        self.pause = False
        self.gameOver = False
        self.speed = 10
        #self.clock = pygame.time.Clock()
    
    def createFrame(self, surface):
        #draw background
        pos = 0
        pos += self.speed
        pos %= self.scaled_street.get_width()
        self.screen.blit(self.get_street_img(pos), (0, 0))
        #draw car
        Game.player.render(self.screen)
        #draw deer
        for d in Game.deer:
            d.render(self.screen)
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
            self.screen.height = int(round(float((self.screen.width-1) // self.screen.width) * self.screen.height))
            self.screen.width -= 1
    
    #unused
    def screenGrows(self):
        if self.screen.width < 1820 and (Game.frameCounter > 0 and Game.frameCounter % 150 == 0):
            self.screen.height = int(round(float(self.screen.width // (self.screen.width-1) * self.screen.height)))
            self.screen.width += 1
    
    #unused:
    @staticmethod
    def carCollidesDeer(carPosition, deerPosition, deerIndex = 0):
        #prüfe alle vier Ecken beider Rechtecke, ob sie im jeweils anderen Rechteck drin sind
        collides = False
        corners = ( ((carPosition[0], carPosition[1]), (carPosition[0]+Game.player.img.get_width(), carPosition[1]), (carPosition[0]+Game.player.img.get_width(), carPosition[1]+Game.player.img.get_height()), (carPosition[0], carPosition[1]+Game.player.img.get_height())),
                ((deerPosition[0], deerPosition[1]), (deerPosition[0]+Game.deer[deerIndex].img.get_width(), deerPosition[1]), (deerPosition[0]+Game.deer[deerIndex].img.get_width(), deerPosition[1]+Game.deer[deerIndex].img.get_height()), (deerPosition[0], deerPosition[1]+Game.deer[deerIndex].img.get_height())))
        imgs = (player.img, deer[deerIndex].img)
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
        self.player.img = img

    #deer presentation
    def set_deer_img(self, path):
        img = pygame.image.load(path)
        img = img.convert_alpha()
        Game.deer_img = img
        for i in Game.deer:
            i.img = self.deer_img
#---

    #core function
    def run(self):
#Christoph:
        renderControls = False
        spawnCount = 0
        maximumCount = 4 #more than 4 deer aren't allowed on the road
#--
        self.running = True
        while self.running:
            self.clock.tick(30)
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
                    Game.player.accelerate()
                else:
                    Game.player.decelerate()
                if keys[pygame.K_LEFT]: #brake
                    Game.player.decelerate()
                if keys[pygame.K_UP]:
                    Game.player.up()
                if keys[pygame.K_DOWN]:
                    Game.player.down()
#Christoph:
                if keys[pygame.K_SPACE]:
                    Game.player.boost = True # self.boost ist schon in accelerate() und decelerate() eingebaut
                else: Game.player.boost = False # WICHTIG
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
                #self.gameOver = Game.player.hasCrashed()
                for deer in Game.deer:
                    deer.move()
                    if deer.isAway():
                        Game.deer.remove(deer)
                        self.survivedDeer += 1
#--
                
            ##SETUP IMAGE BUFFER
            self.createFrame()
            #pygame.draw.polygon(self.screen, (120, 120, 120), self.street)

            ##SHOW CONTENT
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.set_player_img(os.path.join("img", "voiture_r2.png"))
    game.set_street_img(os.path.join("img", "rue_n_clip.png"))
    game.run()
