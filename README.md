import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("shyter")

image = pygame.image.load('background.png.gif')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))  
    screen.blit(image, (100, 100))
    pygame.display.flip()

pygame.quit()
sys.exit()
