import pygame
from sys import exit 
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
		
	def forward(self): 
		self.x += 2
		self.rect.center = (self.x, self.y)
		
	# Override
	def update(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_w]:
			self.forward()
		
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