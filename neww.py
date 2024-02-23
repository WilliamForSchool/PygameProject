import pygame
from sys import exit
import math 
from random import randint


class Map: 
	
	def __init__(self):
		self.walls = []
		# 							   x,  y,  width, height
		self.walls.append(pygame.Rect(500,300, 50, 100))
		
		
	def addWall(self, wall): 
		self.walls.append(wall)
		
	def draw(self, surface):
		# 				  screen,  color,         rectangle
		pygame.draw.rect(surface, (255,255,255), self.walls[0])
		
	def checkMapCollision(self, car): 
		for wall in self.walls: 
			if wall.colliderect(car.getRect()):
				print("Collision")
				return True
				
		return False
		



class Car(pygame.sprite.Sprite):
	
	
	## constructor
	def __init__(self): 
		super().__init__()
		self.image = pygame.image.load('graphics\pure_red_car_32.png').convert_alpha()
		self.rect = self.image.get_rect(center = (300,400))
		var = pygame.PixelArray(self.image)
		var.replace((220,0,0), (randint(0,255), randint(0,255), randint(0,255)))
		self.x = 300.0 # store x independently of rectangle so that it can be a double 
		self.y = 400.0
		self.changingGearUp = False
		self.changingGearDown = False
		self.gear = 1 
		self.angle = 0
		self.master_image = self.image
		self.master_rect = self.rect # keep a copy of the original rectangle for rotation
		
	def forward(self, map): 
		oldx = self.x
		oldy = self.y
		if(not self.gear == 0):
			self.x = self.x + self.gear * math.cos(self.angle/180 * math.pi)
			self.y = self.y + self.gear * math.sin(self.angle/180*math.pi)
			self.rect.center = (self.x, self.y)
			
		if map.checkMapCollision(self):
			self.x = oldx
			self.y = oldy
			self.rect.center = (self.x, self.y)
		
	def back(self): 
		if(not self.gear == 0): 
			self.x = self.x - self.gear * math.cos(self.angle/180 * math.pi)
			self.y = self.y - self.gear * math.sin(self.angle/180*math.pi)
			self.rect.center = (self.x, self.y)
		
	def rotateLeft(self): 
		self.angle -= 3
		if self.angle < 0: 
			self.angle = 359 
		self.image = pygame.transform.rotate(self.master_image, 360 - self.angle)
		self.rect = self.image.get_rect(center = self.rect.center)
	
	def rotateRight(self): 
		self.angle = (self.angle + 3) % 360
		self.image = pygame.transform.rotate(self.master_image, 360 - self.angle)
		self.rect = self.image.get_rect(center = self.rect.center)
		
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
		
			
	def player_input(self, map):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_w]:
		
			self.forward(map)
			
		if keys[pygame.K_a]:
			self.rotateLeft()
		if keys[pygame.K_s]:
			self.back()
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
		
	# Override
	def update(self, map):
		self.player_input(map)
		
		
# Start of the main execution

def clearScreen(): 
	pygame.draw.rect(screen, 'Black', pygame.Rect(0,0,800,600))


pygame.init() # initialize and start the pygame engine
screen = pygame.display.set_mode((800, 600)) # open a window with size
clock = pygame.time.Clock() # allows us to set FPS rates

# make a single Car object
car1 = pygame.sprite.GroupSingle()
car1.add(Car())

map1 = Map()


while True: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	clearScreen()
	car1.update(map1)
	map1.checkMapCollision(car1.sprite)
	
	map1.draw(screen)
	car1.draw(screen)
	pygame.display.update()
	clock.tick(60)