import pygame

running = True

size = (700, 500)
GREEN = (0, 255,0)
WHITE = (0,0,0)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Game.java")

SHIP = pygame.Rect(50,50,100,100)
pygame.draw.rect(screen, GREEN, SHIP)

print(pygame.QUIT)

while running:
	screen.fill(WHITE)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYUP:
			if event.dict["key"] == pygame.K_LEFT:
				print("Move left")
				SHIP.move_ip(-100,0)
			if event.dict["key"] == pygame.K_RIGHT:
				SHIP.move_ip(100,0)
				print("Move right")
		# if event.dict == pygame.K_LEFT:
		# 	SHIP.move(10,0)
		# if event.type == pygame.KEYRIGHT:
		# 	SHIP.move(-10,0)

		# print(event)
		# print(event.dict)

	pygame.draw.rect(screen, GREEN, SHIP)

	pygame.display.flip()

pygame.quit()