import pygame 
import math
import random

# Window Setup
windowWidth = 1366
windowHeight = 768


pygame.init()
win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Penguin")

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

pygame.joystick.init()
if pygame.joystick.get_count() != 8:
    print("ERROR: Incorrect number of joysticks")
    print("There are only " + str(pygame.joystick.get_count()) + " joysticks.")

# Initializing all joysticks
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

numOfPlayers = 8
numOfHoles = 10
numOfPresents = 12

bounciness = 3

SnowManColors = [(255, 0, 0, 255), 
                (0, 255, 0, 255),
                (0, 0, 255, 255), 
                (255, 255, 0, 255), 
                (255, 0, 255, 255), 
                (0, 255, 255, 255), 
                (255, 100, 100, 255), 
                (165, 42, 42, 255)]


def distance(x1, y1, x2, y2, val):
    return (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2) <= val*val

# Snowman(Player) class
class Penguin(pygame.sprite.Sprite):
    def __init__(self, snowManNumber, img):
        # Sprite stuff
        pygame.sprite.Sprite.__init__(self)
        self.trueImage = pygame.transform.scale(img, (75, 75))
        self.image = pygame.transform.scale(img, (75, 75))
        #self.trueImage.fill((100, 100, 255))
        self.rect = self.image.get_rect()

        # Arranging the players in a circle
        self.rect.center = (math.cos(2*math.pi/numOfPlayers*(snowManNumber+1)) * 200 + windowWidth/2,
                            math.sin(2*math.pi/numOfPlayers*(snowManNumber+1)) * 200 + windowHeight/2)
        self.number = snowManNumber
        self.xVel = 0
        self.yVel = 0
        self.score = 0
        self.airborne = False
        self.drowning = False
        self.color = SnowManColors[snowManNumber]
        self.touchdownTime = 50
        self.sideLen = 75
        self.iceHoleX = 0
        self.iceHoleY = 0

    def update(self, others):

        if self.drowning:
            if self.sideLen > 0:
                self.sideLen -= 1
                if self.rect.centerx < self.iceHoleX:
                    self.rect.centerx += 1
                elif self.rect.centerx > self.iceHoleX:
                    self.rect.centerx -= 1

                if self.rect.centery < self.iceHoleY:
                    self.rect.centery += 1
                elif self.rect.centery > self.iceHoleY:
                    self.rect.centery -= 1
                angle = math.atan2(self.yVel, self.xVel)/math.pi*180 - 90
                angle = -180 - angle
                self.image = pygame.transform.scale(self.trueImage, (self.sideLen + 1, self.sideLen + 1))
                self.image = pygame.transform.rotate(self.image, angle)
                temp = self.rect
                self.rect = self.image.get_rect()
                self.rect.centerx = temp.centerx
                self.rect.centery = temp.centery

            else: 
                self.xVel = 0
                self.yVel = 0
                self.sideLen = 75
                self.score -= 5
                if self.score < 0:
                    self.score = 0
                self.drowning = False
                self.rect.center = (math.cos(2*math.pi/numOfPlayers*(self.number+1)) * 200 + windowWidth/2,
                                    math.sin(2*math.pi/numOfPlayers*(self.number+1)) * 200 + windowHeight/2)


            return



        if self.number < pygame.joystick.get_count():
            self.xVel += pygame.joystick.Joystick(self.number).get_axis(0) * 0.15
            self.yVel += pygame.joystick.Joystick(self.number).get_axis(1) * 0.15
            if not self.airborne and joysticks[self.number].get_button(2):
                self.touchdownTime = 50
                self.airborne = True

        # Movement by velocities
        if 20 < self.rect.centerx + self.xVel < windowWidth - 20:
            self.rect.centerx += self.xVel
        else:
            self.xVel = 0
        if 20 < self.rect.centery + self.yVel < windowHeight - 20:
            self.rect.centery += self.yVel
        else:
            self.yVel = 0

        # Drawing the score above the player
        text = myfont.render(str(self.score), False, self.color)
        win.blit(text,(self.rect.centerx,self.rect.centery - 80))

        ## Rotating the sprite towards the direction its going
        # Getting the angle for rotation
        angle = math.atan2(self.yVel, self.xVel)/math.pi*180 - 90
        angle = -180 - angle
        
        # Rotating the actual image
        self.image = pygame.transform.scale(self.trueImage, (self.sideLen, self.sideLen))
        self.image = pygame.transform.rotate(self.image, angle)
        temp = self.rect
        self.rect = self.image.get_rect()
        self.rect.centerx = temp.centerx
        self.rect.centery = temp.centery


        # Debugging line showing direction
        #pygame.draw.line(win, (0, 0, 0), 
        #(self.rect.centerx, self.rect.centery), 
        #(self.rect.centerx + math.cos(math.atan2(self.yVel, self.xVel))*40,
        #self.rect.centery + math.sin(math.atan2(self.yVel, self.xVel))*40), 2)
        
        # Collision
        for otherSnowman in others:
            if otherSnowman.number != self.number and self.airborne == otherSnowman.airborne and self.drowning == otherSnowman.drowning:
                if distance(self.rect.centerx, self.rect.centery, otherSnowman.rect.centerx, otherSnowman.rect.centery, 50):
                    angle = math.atan2(self.rect.centery - otherSnowman.rect.centery, self.rect.centerx - otherSnowman.rect.centerx)
                    self.xVel = math.cos(angle) * bounciness
                    self.yVel = math.sin(angle) * bounciness

        if self.airborne:
            self.touchdownTime -= 1
            if self.touchdownTime > 25:
                self.sideLen += 1
            elif 0 < self.touchdownTime <= 25:
                self.sideLen -= 1
            if self.touchdownTime <= 0:
                self.airborne = False
                self.sideLen = 75

class HoleInIce(pygame.sprite.Sprite):
    def __init__(self, img):
        # Sprite stuff
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (75, 75))

        self.rect = self.image.get_rect()
        # Arranging the players in a circle
        self.rect.center = (1, 1)

    def update(self, playerz):
        for currentP in playerz:
            if not currentP.airborne and distance(self.rect.centerx, self.rect.centery, currentP.rect.centerx, currentP.rect.centery, 37.5):
                currentP.drowning = True
                currentP.iceHoleX = self.rect.centerx
                currentP.iceHoleY = self.rect.centery

    def changeLocation(self, otherHoles, otherPresents, players):
        newX = random.randint(0, windowWidth - 76)
        newY = random.randint(0, windowHeight - 51)

        for hole in otherHoles:
            if distance(hole.rect.centerx, hole.rect.centery, newX, newY, 100):
                self.changeLocation(otherHoles, otherPresents, players)
                return

        for present in otherPresents:
            if distance(present.rect.centerx, present.rect.centery, newX, newY, 100):
                self.changeLocation(otherHoles, otherPresents, players)
                return

        for p in players:
            if distance(p.rect.centerx, p.rect.centery, newX, newY, 100):
                self.changeLocation(otherHoles, otherPresents, players)
                return

        self.rect.centerx = newX
        self.rect.centery = newY


class Present(pygame.sprite.Sprite):
    def __init__(self, img):
        # Sprite stuff
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (75, 75))

        self.rect = self.image.get_rect()
        # Arranging the players in a circle
        self.rect.center = (1, 1)

    def changeLocation(self, otherHoles, otherPresents, players):
        newX = random.randint(0, windowWidth - 76)
        newY = random.randint(0, windowHeight - 51)

        for hole in otherHoles:
            if distance(hole.rect.centerx, hole.rect.centery, newX, newY, 100):
                self.changeLocation(otherHoles, otherPresents, players)
                return

        for present in otherPresents:
            if distance(present.rect.centerx, present.rect.centery, newX, newY, 100):
                self.changeLocation(otherHoles, otherPresents, players)
                return

        for p in players:
            if distance(p.rect.centerx, p.rect.centery, newX, newY, 100):
                self.changeLocation(otherHoles, otherPresents, players)
                return

        self.rect.centerx = newX
        self.rect.centery = newY

    def update(self, pList, oholes, opresents):
        for p in pList:
            if not p.airborne and distance(p.rect.centerx, p.rect.centery, self.rect.centerx, self.rect.centery, 55):
                p.score += 1
                self.changeLocation(oholes, opresents, pList)


# All of the players
snowManList = pygame.sprite.Group()
holeList = pygame.sprite.Group()
presentList = pygame.sprite.Group()

playerImg = pygame.image.load("penguin.png").convert_alpha()

def changeScarfColor(playerNum):
    w, h = playerImg.get_size() # width and height of the img
    temp = playerImg.copy()
    for x in range(w):
        for y in range(h):
            if temp.get_at((x, y)) == pygame.Color(252, 255, 2, 255): # default scarf color
                temp.set_at((x, y), SnowManColors[playerNum])
    return temp


# Initialixing players
for i in range(numOfPlayers):
    snowManList.add(Penguin(i, changeScarfColor(i)))

# Initializing the holes
holeImg = pygame.image.load("holeInIce.png").convert_alpha()
for i in range(numOfHoles):
    holeList.add(HoleInIce(holeImg))

for hole in holeList:
    hole.changeLocation(holeList, presentList, snowManList)

# Initializing the presents
presentImg = pygame.image.load("present.png").convert_alpha()
for i in range(numOfPresents):
    presentList.add(Present(presentImg))

for p in presentList:
    p.changeLocation(holeList, presentList, snowManList)

# Main game Loop
running = True
while running:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Test movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        for s in snowManList:
            s.yVel -= 0.1
            break
    if keys[pygame.K_s]:
        for s in snowManList:
            s.yVel += 0.1
            break
    if keys[pygame.K_a]:
        for s in snowManList:
            s.xVel -= 0.1
            break
    if keys[pygame.K_d]:
        for s in snowManList:
            s.xVel += 0.1
            break
    if keys[pygame.K_r]:
        for p in presentList:
            p.changeLocation(holeList, presentList, snowManList)
        for h in holeList:
            h.changeLocation(holeList, presentList, snowManList)

    win.fill((140, 140, 255))
    
    holeList.draw(win)
    presentList.draw(win)
    for s in snowManList:
        if not s.airborne:
            win.blit(s.image, s.rect)
    
    for s in snowManList:
        if s.airborne:
            win.blit(s.image, s.rect)

    snowManList.update(snowManList)
    holeList.update(snowManList)
    presentList.update(snowManList, holeList, presentList)

    pygame.display.update()

pygame.quit()
