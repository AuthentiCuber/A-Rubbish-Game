import pygame
import settings
import random

from typing import Callable

# setup font
pygame.font.init()
font = pygame.font.SysFont(None, 50)
font_large = pygame.font.SysFont(None, 100)

# setup bin and item types
item_imgs: dict[str, list[str]] = {"rubbish": ["bag", "plastic-bag"],
                                   "recycling": ["cardboard-box", "newspaper", "glass-bottle"],
                                   "foodscrap": ["apple-core", "banana-peel", "fish-bone"]}


def draw_text(text: str, colour: pygame.Color | str, large: bool = False) -> pygame.Surface:
    if large:
        render = font_large.render(text, True, colour)
    else:
        render = font.render(text, True, colour)
    return render


class Button:
    # base class for buttons
    def __init__(self, text: str, pos: tuple[float, float], run: Callable[[], None]):
        self.text = text
        self.render = font.render(self.text, True, "white")
        self.rect = self.render.get_frect(center=pos)
        self.onclick = run

    def update(self, clicking):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and clicking:
            return self.onclick()

    def draw(self, surface):
        surface.blit(self.render, self.rect)


class Item(pygame.sprite.Sprite):
    # base class for items
    def __init__(self, item_type: str):
        super().__init__()
        self.image = pygame.image.load(settings.get_file_path(
            "images/" + random.choice(item_imgs[item_type]) + ".png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 5)
        self.rect = self.image.get_frect(center=settings.screen_size/2)
        self.mask = pygame.mask.from_surface(self.image)
        self.item_type = item_type
        self.drag = False

    def update(self, clicking: bool):
        # dragging logic
        mouse_pos = pygame.mouse.get_pos()
        if clicking:
            if self.rect.collidepoint(mouse_pos):
                self.drag = True
            if self.drag:
                self.rect.center = mouse_pos
        else:
            self.drag = False


class Bin(pygame.sprite.Sprite):
    # base class for bins
    def __init__(self, pos, bin_type: str):
        super().__init__()

        self.image = pygame.image.load(settings.get_file_path(
            "images/" + bin_type + "-bin.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 5)
        self.rect = self.image.get_frect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.bin_type = bin_type
