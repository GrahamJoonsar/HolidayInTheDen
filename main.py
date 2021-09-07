import pygame
import math

# Window Setup
windowWidth = 500
windowHeight = 500
pygame.init()
win = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("SnowMan")
numOfPlayers = 8
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
        self.trueImage = pygame.transform.scale(img, (50, 50))
        self.image = pygame.transform.scale(img, (50, 50))
        #self.trueImage.fill((100, 100, 255))
        self.rect = self.image.get_rect()

        # Arranging the players in a circle
        self.rect.center = (math.cos(2*math.pi/numOfPlayers*(snowManNumber+1)) * 200 + windowWidth/2,
                            math.sin(2*math.pi/numOfPlayers*(snowManNumber+1)) * 200 + windowHeight/2)
        self.number = snowManNumber
        self.xVel = 0
        self.yVel = 0
        self.score = 0
        #self.color = SnowManColors[snowManNumber]
        
    def collide(self, otherx, othery):
        angle = math.atan2(self.y - othery, self.x - otherx)
        self.xVel = math.cos(angle) * bounciness
        self.yVel = math.sin(angle) * bounciness
        

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

        ## Rotating the sprite towards the direction its going
        # Getting the angle for rotation
        angle = math.atan2(self.yVel, self.xVel)/math.pi*180 - 90
        angle = -180 - angle
        
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
        
        for otherSnowman in others:
            if otherSnowman.number != self.number:
                if distance(self.rect.centerx, self.rect.centery, otherSnowman.rect.centerx, otherSnowman.rect.centery) <= 25:
                    angle = math.atan2(self.rect.centery - otherSnowman.rect.centery, self.rect.centerx - otherSnowman.rect.centerx)
                    self.xVel = math.cos(angle) * bounciness
                    self.yVel = math.sin(angle) * bounciness

snowManList = pygame.sprite.Group()

# Initializing Players
for i in range(numOfPlayers):
    snowManList.add(Snowman(i, pygame.image.load("snowman.png").convert_alpha()))

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

    win.fill((100, 100, 255))

    

    snowManList.draw(win)
    snowManList.update(snowManList)


    pygame.display.update()

pygame.quit()
