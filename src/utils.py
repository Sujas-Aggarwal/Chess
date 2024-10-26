import pygame
from pathlib import Path

class AssestsHandler:
    @staticmethod
    def loadImage(filename:str):
        """Load an image asset."""
        return pygame.image.load(Path('Assets') / filename)
    
    @staticmethod
    def scaleImage(image, scale):
        """Scale an image asset."""
        return pygame.transform.scale(image, scale)
    
    @staticmethod
    def loadSound(filename:str):
        """Load a sound asset."""
        return pygame.mixer.Sound(Path('Assets') / 'Sounds' / filename)
    
    @staticmethod
    def loadFont(filename:str, size):
        """Load a font asset."""
        return pygame.font.Font(Path(filename), size)
