import pygame
import math
import random

# Window Setup
windowWidth = 1366
windowHeight = 768


pygame.init()
win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("SnowMan")

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

numOfPlayers = 8
numOfHoles = 10
numOfPresents = 12

bounciness = 3

SnowManColors = [(255, 0, 0), 
                (0, 255, 0),
                (0, 0, 255), 
                (255, 255, 0), 
                (255, 0, 255), 
                (0, 255, 255), 
                (255, 100, 100), 
                (165, 42, 42)]


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Snowman(Player) class
class Snowman(pygame.sprite.Sprite):
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
        self.color = SnowManColors[snowManNumber]
        

    def update(self, others):
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
        self.image = pygame.transform.rotate(self.trueImage, angle)
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
            if otherSnowman.number != self.number:
                if distance(self.rect.centerx, self.rect.centery, otherSnowman.rect.centerx, otherSnowman.rect.centery) <= 50:
                    angle = math.atan2(self.rect.centery - otherSnowman.rect.centery, self.rect.centerx - otherSnowman.rect.centerx)
                    self.xVel = math.cos(angle) * bounciness
                    self.yVel = math.sin(angle) * bounciness

class HoleInIce(pygame.sprite.Sprite):
    def __init__(self, img):
        # Sprite stuff
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (75, 30))

        self.rect = self.image.get_rect()
        # Arranging the players in a circle
        self.rect.center = (1, 1)

    def changeLocation(self, otherHoles, otherPresents):
        newX = random.randint(0, windowWidth - 76)
        newY = random.randint(0, windowHeight - 51)

        for hole in otherHoles:
            if distance(hole.rect.centerx, hole.rect.centery, newX, newY) < 100:
                self.changeLocation(otherHoles, otherPresents)
                return

        for present in otherPresents:
            if distance(present.rect.centerx, present.rect.centery, newX, newY) < 100:
                self.changeLocation(otherHoles, otherPresents)
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

    def changeLocation(self, otherHoles, otherPresents):
        newX = random.randint(0, windowWidth - 76)
        newY = random.randint(0, windowHeight - 51)

        for hole in otherHoles:
            if distance(hole.rect.centerx, hole.rect.centery, newX, newY) < 100:
                self.changeLocation(otherHoles, otherPresents)
                return

        for present in otherPresents:
            if distance(present.rect.centerx, present.rect.centery, newX, newY) < 100:
                self.changeLocation(otherHoles, otherPresents)
                return

        self.rect.centerx = newX
        self.rect.centery = newY

    def update(self, pList, oholes, opresents):
        for p in pList:
            if distance(p.rect.centerx, p.rect.centery, self.rect.centerx, self.rect.centery) < 55:
                p.score += 1
                self.changeLocation(oholes, opresents)


# All of the players
snowManList = pygame.sprite.Group()
holeList = pygame.sprite.Group()
presentList = pygame.sprite.Group()

# Initializing Players
for i in range(numOfPlayers):
    snowManList.add(Snowman(i, pygame.image.load("penguin.png").convert_alpha()))

# Initializing the holes
for i in range(numOfHoles):
    holeList.add(HoleInIce(pygame.image.load("holeInIce.png").convert_alpha()))

for hole in holeList:
    hole.changeLocation(holeList, presentList)

# Initializing the presents
for i in range(numOfPresents):
    presentList.add(Present(pygame.image.load("present.png").convert_alpha()))

for p in presentList:
    p.changeLocation(holeList, presentList)

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
            p.changeLocation(holeList, presentList)
        for h in holeList:
            h.changeLocation(holeList, presentList)

    win.fill((140, 140, 255))
    
    holeList.draw(win)
    presentList.draw(win)
    snowManList.draw(win)

    snowManList.update(snowManList)
    presentList.update(snowManList, holeList, presentList)

    pygame.display.update()

pygame.quit()
