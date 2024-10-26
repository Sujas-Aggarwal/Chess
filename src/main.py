import pygame
from config import WIDTH, HEIGHT
from chess import Game

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess!")
    
    game = Game(screen)
    game.start()

if __name__ == "__main__":
    main()
