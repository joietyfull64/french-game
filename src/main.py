#!/usr/bin/env python2
# vim: set fileencoding=utf-8

import os.path
import sys
from math import ceil

import pygame

#Christoph: ich gehe davon aus, dass die Position eines Objekts immer die obere linke Ecke ist
#img.width - Länge des Bildes, img.height - Höhe des Bildes
#screen.width - Länge des Fensters, screen,height - Höhe des Fensters
#random(arg1, arg2) - a random value in the given range; arg1 - inclusive start of range, arg2 - inclusive end of range

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
#Christoph:
        self.speed = (10, 10) #pixel speed
#--
        self.x = x # x und y braucht man nicht als Parameter, man kann dafür einfach einen Startwert festlegen oder generieren
        self.y = y #self.position = (x, y)
        self.max_x = max_x #self.xDistance = max_x
        self.max_y = max_y #self.yDistance = max_y
        self.img = img #ist gleichzeitig die Größe 

    def up(self):
        """Moves the Entity up."""
        if self.y == 0: #geht so nicht ganz
            return
        self.y -= 10 #Literale (hardgecodete Werte) sind nur im Notfall zu benutzen
#       upperBound = screen.height/2-max_y/2
#       if (self.position[1] - upperBounds) < self.speed[1]: #upperBound muss nicht unbedingt 0 sein
#          self.position[1] = upperBound
#       else:
#           self.speed[1] = -abs(self.speed[1]) #we need this because the position will be modified in other functions with +=
#           self.position[1] += self.speed[1]

    def down(self):
        """Moves the Entity down."""
        if self.y == self.max_y: #dürfte so leider auch nicht ganz funktionieren
            return
        self.y += 10
#       lowerBound = screen.height/2+max_y/2
#       if (screen.height-lowerBound-(self.img.height+self.position[1]) < self.speed[1]:
#           self.position[1] = screen.height-lowerBound-self.img.height
#       else:
#           self.speed[1] = abs(self.speed[1])
#           self.position[1] += self.speed[1]
#Christoph:
    def left(self):
        leftBound = screen.width/2-max_x/2
        if (self.position[0] - leftBounds) < self.speed[0]:
            self.position[0] = leftBounds
        else:
            self.speed[0] = -abs(self.speed[0])
            self.position[0] += self.speed[0]

    def right(self):
        rightBound = screen.width/2+max_x/2
        if (screen.width-rightBound-(self.img.width+self.position[0])) < speed[0]:
            self.position[0] = screen.width-rightBound-img.width
        else:
            self.speed[0] = abs(self.speed[0])
            self.position[0] += speed[0]
#--

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
#Christoph:
        self.boost = False #mehr dazu: unterer Kommentar
        self.boostFactor = 2.0 #when space is pressed, the movement will be faster by this factor
        self.speed = (5,5)
#--

    def decelerate(self):
        """Decelerates the Player."""
        if self.x == 0:
            return
        self.x -= 5
#       leftBound = screen.width/2-max_x/2
#       if (self.position[0] - leftBounds) < (self.speed[0] if not boost else (self.speed[0]*self.boostFactor)):
#           self.position[0] = leftBounds
#       else:
#           self.speed[0] = -abs(self.speed[0])
#           self.position[0] -= self.speed[0] if not boost else (self.speed[0]*self.boostFactor)

    def accelerate(self):
        """Accelerates the Player."""
        if self.x == self.max_x:
            return
        self.x += 5
#       rightBound = screenWidth/2+max_x/2
#       if (screen.width-rightBound-(self.img.width+self.position[0])) < (self.speed[0] if not boost else (self.speed[0]*self.boostFactor)):
#           self.position[0] = screen.width-rightBound-self.img.width
#       else:
#           self.speed[0] = abs(self.speed[0])
#           self.position[0] += self.speed[0] if not boost else (self.speed[0]*self.boostFactor)

#Christoph:
    def up(self): #override
        upperBound = screen.height/2-max_y/2
        if (self.position[1] - upperBound) < self.speed[1]: #upperBound muss nicht unbedingt 0 sein
           self.position[1] = upperBound
        else:
            self.speed[1] = -abs(self.speed[1])
            self.position[1] += self.speed[1]
        
    def down(self): #override
        lowerBound = screen.height/2+max_y/2
        if (screen.height-lowerBound-(self.img.height+self.position[1]) < self.speed[1]:
            self.position[1] = screen.height-lowerBound-self.img.height
        else:
            self.speed[1] = abs(self.speed[1])
            self.position[1] += self.speed[1]
        
    def hasCrashed(self):
        # use self.speed
        interference = False
        #the following is the simplest algorithm possibility but it takes a few more time
        for deer in deers:
            #speeds = (, )
            objects = (self, deer)
            i = 1; i2 = 0
            if sqrt(self.speed[0]**2 + self.speed[1]**2) > sqrt(deer.speed[0]**2 + deer.speed[1]**2):
                i = 0; i2 = 1
            #speed1 = speeds[i]
            #speed2 = speeds[i2]
            #speeds = None
            collision1 = (float(objects[i].img.width), float(objects[i].img.height)) #1 is for the quicker object
            origin1 = (objects[i].img.width, objects[i].img.height)
            distance1 = (objects[i].speed[0], objects[i].speed[1])
            collision2 = (float(objects[i2].img.width), float(objects[i2].img.height))
            origin2 = (objects[i2].img.width, objects[i2].img.height)
            distance2 = (objects[i2].speed[0], objects[i2].speed[1])
            objects = None
            if distance2[0] < distance2[1]:
                i = 0; i2 = 1
            else:
                i = 1; i2 = 0
            #i3 = 1; i4 = 0
            #if distance1[0] < distance1[1]:
            #    i3 = 0; i4 = 1
            sign = (distance2[i] >>> 31) | 1
            speed2 = float(distance2[i2])/float(distance2[i])*sign
            speed1 = float(distance1[i])/float(abs(distance2[i])) # 1/kleineEntfernungVomLangsamerenObjekt = Faktor
            speed12 = float(distance1[i2])/float(abs(distance2[i]))
            while not int(collision2[i]) == (origin2[i]+distance2[i]) and not interference:
                collision2[i] += sign
                collision2[i2] += speed2
                collision1[i] += speed1
                collision1[i2] += speed12
                interference = Game.carCollidesAnimal(collision1, collision2)
            
            for i in range(0,1):  #check twice, for x-axis and for y-axis
            #TODO: funktioniert nicht ganz, x-Achsenprüfung ist unabhängig von y-Achse
                if (self.speed[i] > deer.speed[i]):
                    carPosition = self.position
                    deerPosition = deer.position
                    testPositionQuicker = float(self.speed[i])
                    quickerPace = float(self.speed[i])//deer.speed[i]
                    while deerPosition[i] >= deer.speed[i]+deer.position[i] and not interference[i]:
                        #tests all positions from the beginning of the movement to the end from the slower object (car or deer)
                        testPositionQuicker += quickerPace
                        carPosition[i] = int(testPositionQuicker)
                        deerPosition[i] += 1
                        interference[i] = carCollidesDeer(carPosition, deerPosition)
                else: #same as before only with self.vector_move and deer.vector_move switched
                    carPosition = self.position
                    deerPosition = deer.position
                    testPositionQuicker = float(deer.vector_move[i])
                    quickerPace = float(deer.vector_move[i])/self.vector_move[i]
                    while carPosition[i] >= self.vector_move[i]+self.position[i] and not interference[i]:
                        #tests all positions from the beginning of the movement to the end from the slower object (car or deer)
                        testPositionQuicker += quickerPace
                        deerPosition[i] = int(testPositionQuicker)
                        carPosition[i] += 1
                        interference[i] = carCollidesDeer(carPosition, deerPosition)
        self.speed = (0,0)
        return interference
#--

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
        self.move_type = move_type #I don't recommend to place variables in front of a super constructor call
        super(Deer, self).__init(*args) #__init__
        #place it here
#Christoph:
        #max_x is used as maximum x movement distance
        #max_y is used as maximum y movement distance
        if move_type == 0:
            self.position = (screen.width, random((screen.height/2-max_y/2), (screen.height/2+max_y/2)))
        elif not move_type == 5 and not move_type == 6 and not move_type == 7:
            if move_type == 1 or move_type == 3:
                self.position = (random(screen.width/2-max_x/2, screen.width/2+max_x/2), -self.img.height)
            else:
                self.position = (random(screen.width/2-max_x/2, screen.width/2+max_x/2), screen.height)
            if move_type == 1 or move_type == 2:
                self.speed = (0, 10)
            else:
                #strahlensatz mit pythagoras
                deerCenter = (self.position[0]+self.img.width/2, self.position[1]+self.img.height/2)
                carCenter = (player.position[0]+player.img.width/2, player.position[1]+player.img.height/2)
                xDistance = carCenter[0]-deerCenter[0]; yDistance = carCenter[1]-deerCenter[1]
                distance = sqrt(xDistance**2 + yDistance**2)
                x = float(xDistance)/float(distance)*10.0; y = float(yDistance)/float(distance)*10.0
                self.speed = (x,y)
        elif move_type == 5 or move_type == 6:
            self.position = (screen.width, random((screen.height/2-max_y/2), (screen.height/2+max_y/2)))
            if move_type == 5: self.speed = (gameSpeed, -10)
            else: self.speed = (gameSpeed, 10)
        else:
            self.position = (screen.width, random((screen.height/2-max_y/2), (screen.height/2+max_y/2)))
#--

    def move(self):
        """
        Moves the Deer according to its move_type. The movements are:
        0 = No movement (no animation but moves parallel to the street)
        1 = walks continually up (left-up-walking animation)
        2 = Walks continually down (left-down-walking animation)
        3 = Like 1, but aims for player's car at spawn time (left/right-up-walking animation)
        4 = Like 2, but aims for player's car at spawn time (left/right-down-walking animation)
        5 = Walks between (screen.height/2-max_y/2) and (screen.height/2+max_y/2) (yDistance) - starts going up
        6 = Walks between (screen.height/2-max_y/2) and (screen.height/2+max_y/2) (yDistance) - starts going down
        7 = Like 0 only slower (up-walking animation)
        """
        pass
#       if move_type == 2:
#           self.position[1] -= self.speed[1]
#       elif move_type == 1 or move_type == 3 or move_type == 4:
#           for i in range(0,1): self.position[i] += self.speed[i]
#       elif move_type == 5 or move_type == 6:
#           self.position[0] -= gameSpeed
#           upperBounds = screen.height/2-max_y/2; lowerBounds = screen.height/2+max_y/2
#           if self.speed[1] < 0 and (self.position[1] - upperBounds) < self.gameSpee[1]:
#               self.position[1] = upperBounds
#               self.speed[1] *= -1
#           elif self.speed[1] >= 0 and (screen.height-lowerBounds-self.img.height-self.position[1]) < self.speed[1]:
#               self.position[1] = screen.height-lowerBounds-self.img.height
#               self.speed[1] *= -1
#           else: self.position[1] += self.speed[1]
#       elif move_type == 0:
#           self.position[0] -= gameSpeed
#       else:
#           self.position[0] -= gameSpeed-10

class Game(object):
#Christoph:
    # we need them static because they are used by a static collision detection function which is static so that other
    # classes can use it
    player = Player(0, self.height // 2, self.width, self.height)
    deers = []
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
        self.survivedDeers = 0
#--
        self.width = width
        self.height = height

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Passée")
        pygame.mouse.set_visible(1)

        self.player = Player(0, self.height // 2, self.width, self.height) #only the class variable should be used
        self.deer = [] #sollte möglichst deers heißen damit man die Laufvariable in for-Schleifen deer nennen kann
                        #sollte nur als Klassenvariable verwendet werden
        # Tastendruck wiederholt senden, falls nicht losgelassen
        pygame.key.set_repeat(1, 30)
        self.clock = pygame.time.Clock()
        self.running = False
        self.speed = 10 # änder mal den Namen auf gameSpeed oder meinetwegen game_speed
                    # diese Variable lässt sich nach einiger Zeit updaten

#Christoph:
    def resetGameScene(self): #set up everything
        Game.player = Player(...) # player should become a class variable
        Game.deers = []
        self.gameSpeed = 10
        self.roadOffset = 0
        self.survivedDeers = 0
        self.startmenu = False
        self.pause = False
        self.gameOver = False
    
    def paintImage(self):
        #draw background
        painter.draw(imageBuffer, Rectangle(bgColor)) # bgColor can be declared as global (static) variable
        painter.draw(imageBuffer, getRoadClip())
        for deer in deers:
            deer.draw(painter, imageBuffer)
        playerCar.draw(painter, imageBuffer)
        ... # draw and write stats on the buffered image
        return imageBuffer
    
    def paintPauseImage(self):
        imageBuffer = paintImage()
        ... # draw and write something on the imageBuffer
        return imageBuffer
    
    def paintGameOverImage(self):
        imageBuffer = paintImage() # another background image
        ... # draw and write something on the imageBuffer
        return imageBuffer
    
    def paintStartMenuImage(self):
        imageBuffer = bgImage
        ... # draw and write something on the imageBuffer
        return imageBuffer
    
    def showControls(self, surface):
        ... # draw and write something on surface
        return image
    
    ##NEW (4.11.):
    def screenShrinks(self): #a funny idea, when playing -> the game window shrinks per 120 frames by 1 pixel for more difficulty
        if self.width > 200 and (Game.frameCounter > 0 and Game.frameCounter % 120 == 0):
            self.height = int(round(float(self.width // (self.width-1)) * self.height))
            self.width -= 1
    
    ##New (4.11.):
    @staticmethod
    def carCollidesDeer(carPosition, deerPosition, deerIndex = 0):
        #prüfe alle vier Ecken beider Rechtecke, ob sie im jeweils anderen Rechteck drin sind
        collides = False
        carCorners = ((carPosition[0], carPosition[1]), (carPosition[0]+Game.player.img.width, carPosition[1]), (carPosition[0]+Game.player.img.width, carPosition[1]+Game.player.img.height), (carPosition[0], carPosition[1]+Game.player.img.height))
        deerCorners = ((deerPosition[0], deerPosition[1]), (deerPosition[0]+Game.deers[deerIndex].img.width, deerPosition[1]), (deerPosition[0]+Game.deers[deerIndex].img.width, deerPosition[1]+Game.deers[deerIndex].img.height), (deerPosition[0], deerPosition[1]+Game.deers[deerIndex].img.height))
        for i in range(4):
            if :
                break
        
        if not collides:
            for i in range(4)
                if :
                    break
        pass collides
#--

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

    def get_street_img(self, pos): #pos -> off(set)
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
#Christoph:
        showControls = False
        spawnCount = 0
#--
        
        self.running = True
        pos = 0 # sollte entweder zu self.roadOffset oder self.road_offset werden (namentlich eindeutiger)
        while self.running:
            self.clock.tick(30)
            
#Christoph:
            if startmenu:
                # if showControls:
                    # #USER input
                    # if keyPressed: showControls = False
                    
                    # frame = showControls(painter, paintStartMenuImage()) #
                #else:
                    # #USER input
                    # if pressedKey is SPACE: showControls = True
                    # elif pressedKey:
                    #   showControls = False
                    #   resetGameScene()
    
                    ##New (4.11.) -> painter argument for paint function calls
                    # frame = paintStartMenuImage(painter) # paint functions see below
            
            elif gameOver:
                # #USER input
                # if pressedKey:
                #   if pressedKey is ESCAPE: startmenu = True
                #   else: resetGameScene()
                
                ##New (4.11.):
                # frame = paintGameOverImage(painter)
            
            elif pause:
                # #USER input
                # if pressedKey is ESCAPE: pause = False
                
                # frame = paintPauseImage(painter)
            
            else:
#--
            ##USER INPUT:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.player.accelerate()
            else: #diese Bedingung brauchen wir nicht unbedingt, darunter haben wir ja schon dasselbe
                self.player.decelerate()
            if keys[pygame.K_LEFT]:
                self.player.decelerate()
            if keys[pygame.K_UP]:
                self.player.up()
            if keys[pygame.K_DOWN]:
                self.player.down()
#Christoph:
            if keys[pygame.K_SPACE]:
                self.player.boost = True
#--
            if keys[pygame.K_ESCAPE]:
                sys.exit() # pause = True fänd ich gut, vielleicht kann man dann von dort beenden
#Christoph:
            #while (spawn-condition): spawnCount+=1
                # if spawnCount:
                #   for i in range(spawnCount):
                #       spawnedDeers.add(Deer(...))
                #   spawnCount = 0
                
                # #GAME routine
                # #New (4.11.):
                # gameOver = playerCar.hasCrashed()
                # for deer in spawnedDeers:
                #   deer.move()
                #   if deer.isAway(): spawnedDeers.remove(deer)
#--
                
            ##SETUP IMAGE BUFFER
            #Das Anzeigezeug hier würde ich wirklich in eine kleine Extrafunktion machen
            pos += self.speed
            pos %= self.scaled_street.get_width()
            self.screen.blit(self.get_street_img(pos), (0, 0))
            self.player.render(self.screen)

            #pygame.draw.polygon(self.screen, (120, 120, 120), self.street)

            ##SHOW CONTENT
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.set_player_img(os.path.join("img", "voiture_r2.png"))
    game.set_street_img(os.path.join("img", "rue_n_clip.png"))
    game.run()
