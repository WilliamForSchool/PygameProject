import pygame
from sys import exit
import math
from random import randint


class Map:
    def __init__(self):
        self.walls = []
        self.checkpoint = []  # checkpoint walls

    # 							   x,  y,  width, height

    def addCheckPoint(self, wall):
        self.checkpoint.append(wall)

    def addWall(self, wall):
        self.walls.append(wall)

    def draw(self, surface):
        # 				  screen,  color,         rectangle
        for wall in self.walls:
            pygame.draw.rect(surface, (255, 255, 255), wall)
        for checkpoint in self.checkpoint:
            pygame.draw.rect(surface, (255, 0, 255), checkpoint)

    def checkMapCollision(self, car):
        for wall in self.walls:
            if wall.colliderect(car.getRect()):
                return wall

        for i in range(0, len(self.checkpoint)):
            if self.checkpoint[i].colliderect(car.getRect()):
                car.hitCheckPoint(i)
                break
        return None


class Car(pygame.sprite.Sprite):

    ## constructor
    def __init__(self, parent1=None, parent2=None):
        super().__init__()
        self.image = pygame.image.load('graphics\pure_red_car_32.png').convert_alpha()
        self.rect = self.image.get_rect(center=(200, 100))
        var = pygame.PixelArray(self.image)
        var.replace((220, 0, 0), (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.x = 200.0  # store x independently of rectangle so that it can be a double
        self.y = 100.0
        self.changingGearUp = False
        self.changingGearDown = False
        self.gear = 1
        self.angle = 0
        self.master_image = self.image
        self.master_rect = self.rect  # keep a copy of the original rectangle for rotation
        if parent1 == None or parent2 == None:
            self.dna = []
            self.createNewDNA()
            # createNewDNA(self)
        else:
            self.dna = self.combineDNA(parent1, parent2)
        self.currentIndex = 0
        self.checks = [False, False, False, False, False, False, False, False, False]
        self.score = 0

    def combineDNA(self, parent1, parent2):
        randomNum = randint(0, 6250 - 1)
        list = parent1.getDNA()[0:randomNum] + parent2.getDNA()[randomNum + 1: len(parent2.getDNA())]

        for i in range(0, len(list)):
            random1 = randint(0, 120)
            
            if random1 < 2:
                if(13 < len(list) - i):
                    for l in range(i, i + 10):
                        list[l] = 1
                    
            elif random1 < 4:
                if(13 < len(list) - i):
                    for p in range(i, i + 10):
                        list[p] = 2


        return list

    def getDNA(self):
        return self.dna

    def createNewDNA(self):
        for i in range(6250):
            prob = randint(1, 100)
            if prob <= 10:
                self.dna.append(0)
            elif prob <= 50:
                self.dna.append(1)  # turn left
            elif prob <= 90:
                self.dna.append(2)  # right
            elif prob <= 95:
                pass
                #self.dna.append(3)  # gear down
            else:
                pass
                #self.dna.append(4)  # gear up

    def hitCheckPoint(self, num):
        if num == 0 and not self.checks[0]:
            self.checks[num] = True
            self.score += (6000 - self.currentIndex) + 5
        if num == 8 and not self.checks[8]:
            if self.checks[7] == True:
                self.checks = [False, False, False, False, False, False, False, False, False]
                self.score += (6000 - self.currentIndex) + 50
                print("Done")
        elif self.checks[num - 1] and not self.checks[num]:
            self.checks[num] = True
            self.score += (6000 - self.currentIndex) + 50

    def generationOver(self):
        return self.currentIndex >= len(self.dna)

    def reset(self):
        self.currentIndex = 0
        self.rect = self.image.get_rect(center=(200, 100))
        self.score = 0
        self.x = 200.0
        self.y = 100.0
        self.angle = 0
        self.gear = 1

        self.checks = [False, False, False, False, False, False, False, False, False]

    def forward(self, map):
        # stuckPosition type thing, where if the car is considered stuck, add more probability to turn in their combineDNA?
        oldx = self.x
        oldy = self.y
        if self.gear >= 3:
            self.gear = 3
        if self.gear <= -3:
            self.gear = -3
        if (not self.gear == 0):
            self.x = self.x + self.gear * math.cos(self.angle / 180 * math.pi)
            self.y = self.y + self.gear * math.sin(self.angle / 180 * math.pi)
            self.rect.center = (self.x, self.y)



        collisionRect = map.checkMapCollision(self)

        if collisionRect != None:
            self.x = oldx
            self.y = oldy
            self.rect.center = (self.x, self.y)

    def back(self, map):
        oldx = self.x
        oldy = self.y
        if (not self.gear == 0):
            self.x = self.x - self.gear * math.cos(self.angle / 180 * math.pi)
            self.y = self.y - self.gear * math.sin(self.angle / 180 * math.pi)
            self.rect.center = (self.x, self.y)

        if map.checkMapCollision(self) != None:
            self.x = oldx
            self.y = oldy
            self.rect.center = (self.x, self.y)
            
    def getSurface(self): 
        return self.rect

    def rotateLeft(self):
        self.angle -= 3
        if self.angle < 0:
            self.angle = 359
        self.image = pygame.transform.rotate(self.master_image, 360 - self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotateRight(self):
        self.angle = (self.angle + 3) % 360
        self.image = pygame.transform.rotate(self.master_image, 360 - self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def gearUp(self):
        if not self.changingGearUp:
            self.gear = self.gear + 1
            self.changingGearUp = True

    def gearDown(self):
        if not self.changingGearDown:
            self.gear = self.gear - 1
            self.changingGearDown = True

    def getRect(self):
        return self.rect

    def getScore(self):
        return self.score

    def player_input(self, map):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.forward(map)

        if keys[pygame.K_a]:
            self.rotateLeft()
        if keys[pygame.K_s]:
            self.back(map)
        if keys[pygame.K_d]:
            self.rotateRight()

        if keys[pygame.K_LSHIFT]:
            self.gearUp()
        else:
            self.changingGearUp = False

        if keys[pygame.K_RSHIFT]:
            self.gearDown()
        else:
            self.changingGearDown = False

    def stepAI(self, map):
        global dna
        global index

        if self.currentIndex < len(self.dna):
            if (self.dna[self.currentIndex] == 1):
                self.rotateLeft()
            elif (self.dna[self.currentIndex] == 2):
                self.rotateRight()
            elif (self.dna[self.currentIndex] == 3):
                pass
                #self.gearDown()

            elif (self.dna[self.currentIndex] == 4):
                pass
                #self.gearUp()

        self.forward(map)
        self.currentIndex += 1

    # Override
    def update(self, map):
        self.player_input(map)
        self.stepAI(map)


# Start of the main execution

def clearScreen():
    pygame.draw.rect(screen, 'Black', pygame.Rect(0, 0, 800, 500))


def createMap1():
    # x , y, widht, height
    map1.addWall(pygame.Rect(10, 10, 780, 50))  # top
    map1.addWall(pygame.Rect(740, 10, 50, 480))  # right
    map1.addWall(pygame.Rect(10, 440, 780, 50))  # top?
    map1.addWall(pygame.Rect(10, 10, 50, 480))
    map1.addWall(pygame.Rect(550, 60, 190, 125))
    map1.addWall(pygame.Rect(150, 140, 300, 220))
    map1.addWall(pygame.Rect(450, 260, 170, 100))  # left
    map1.addCheckPoint(pygame.Rect(450, 150, 100, 10))  # 1
    map1.addCheckPoint(pygame.Rect(600, 185, 10, 75))  # 2
    map1.addCheckPoint(pygame.Rect(620, 350, 120, 10))  # 3
    map1.addCheckPoint(pygame.Rect(600, 360, 10, 80))  # 4
    map1.addCheckPoint(pygame.Rect(400, 360, 10, 80))  # 5
    map1.addCheckPoint(pygame.Rect(200, 360, 10, 80))  # 6
    map1.addCheckPoint(pygame.Rect(50, 350, 120, 10))  # 7
    map1.addCheckPoint(pygame.Rect(50, 140, 120, 10))  # 8
    map1.addCheckPoint(pygame.Rect(250, 60, 10, 90))  # 9


def killBottomHalf(sortedList):
    sortedList = sortCarsByScore()
    return sortedList[0:int(len(sortedList) / 2)]


def makeBabyCars(sortedList):
    for i in range(0, len(sortedList)):
        parent1 = sortedList[randint(0, 0)]
        parent2 = sortedList[randint(0, 0)]
        sortedList.append(Car(parent1, parent2))


def createNextGeneration():
    sortedList = sortCarsByScore()
    sortedList = killBottomHalf(sortedList)
    for i in range(0, len(sortedList) - 1):
        sortedList[i].reset()
    makeBabyCars(sortedList)
    cars.empty()
    cars.add(sortedList)


def sortCarsByScore():
    listOfCars = cars.sprites()
    for i in range(0, len(listOfCars) - 1):
        for j in range(0, len(listOfCars) - 2):
            if listOfCars[j].getScore() < listOfCars[j + 1].getScore():
                temp = listOfCars[j]
                listOfCars[j] = listOfCars[j + 1]
                listOfCars[j + 1] = temp

    return listOfCars


generation = 1

pygame.init()  # initialize and start the pygame engine
screen = pygame.display.set_mode((800, 500))  # open a window with size
clock = pygame.time.Clock()  # allows us to set FPS rates

# make a single Car object
cars = pygame.sprite.Group()
for i in range(300):
    cars.add(Car())

map1 = Map()
createMap1()

toggle = False
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sorted = sortCarsByScore()
            for c in sorted:
                print(c.getScore())
            exit()
    clearScreen()
    cars.update(map1)

    map1.draw(screen)
    if keys[pygame.K_g]:
        toggle = not toggle
    if toggle: 
        sorted = sortCarsByScore()
        pygame.draw.rect(screen, (255, 0, 0), sorted[0])
    else:
        cars.draw(screen)
    pygame.display.update()
    clock.tick(500)

    if cars.sprites()[0].generationOver():
        generation += 1
        createNextGeneration()
        print(generation)
