import pygame
from os import path

pygame.display.init()

screen_size = pygame.Vector2(pygame.display.get_desktop_sizes()[0]) / 1.2

def get_file_path(filename: str) -> str:
    file = path.abspath(path.join(path.dirname(__file__), filename))
    return file
