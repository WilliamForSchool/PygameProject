import pygame

pygame.init() # initialize and start the pygame engine
screen = pygame.display.set_mode((800, 600)) # open a window with size


while True: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	pygame.display.update()