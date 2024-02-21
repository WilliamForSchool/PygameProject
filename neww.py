import pygame
from sys import exit 

pygame.init() # initialize and start the pygame engine
screen = pygame.display.set_mode((800, 600)) # open a window with size
clock = pygame.time.Clock() # allows us to set FPS rates

while True: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	pygame.display.update()
	clock.tick(60)