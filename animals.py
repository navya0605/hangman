import sys
import pygame

def main(level):
    # Initialize Pygame
    pygame.init()

    # Set up display
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(f"Animals Game - {level.capitalize()} Level")

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill((255, 255, 255))  # Fill the screen with white
        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python animals.py <level>")
    else:
        main(sys.argv[1])
