import pygame
from sys import exit
import math 
from random import randint

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
		self.gear = 1 
		self.angle = 0
		self.master_image = self.image
		self.master_rect = self.rect # keep a copy of the original rectangle for rotation
		
	def forward(self): 
		self.x = self.x + self.gear * math.cos(self.angle/180 * math.pi)
		self.y = self.y + self.gear * math.sin(self.angle/180*math.pi)
		self.rect.center = (self.x, self.y)
		
	def back(self): 
		self.x = self.x - self.gear * math.cos(self.angle/180 * math.pi)
		self.y = self.y - self.gear * math.sin(self.angle/180*math.pi)
		self.rect.center = (self.x, self.y)
		
	def player_input(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_w]:
			self.forward()
		if keys[pygame.K_a]:
			self.angle -= 2
			if self.angle < 0: 
				self.angle = 359 
			self.image = pygame.transform.rotate(self.master_image, 360 - self.angle)
			self.rect = self.image.get_rect(center = self.rect.center)
		if keys[pygame.K_s]:
			self.back()
		if keys[pygame.K_d]:
			self.angle = (self.angle + 2) % 360
			self.image = pygame.transform.rotate(self.master_image, 360 - self.angle)
			self.rect = self.image.get_rect(center = self.rect.center)

	# Override
	def update(self):
		self.player_input()
		
		
# Start of the main execution

def clearScreen(): 
	pygame.draw.rect(screen, 'Black', pygame.Rect(0,0,800,600))


pygame.init() # initialize and start the pygame engine
screen = pygame.display.set_mode((800, 600)) # open a window with size
clock = pygame.time.Clock() # allows us to set FPS rates

# make a single Car object
car1 = pygame.sprite.GroupSingle()
car1.add(Car())

while True: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	clearScreen()
	car1.draw(screen)
	car1.update()
	pygame.display.update()
	clock.tick(60)