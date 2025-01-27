import pygame
import pygame.image
from pygame.locals import *
import sys
import random

from classes import Item, Bin, Button, draw_text, item_imgs
import settings

# initialise pygame
pygame.init()

# create window
screen = pygame.display.set_mode(settings.screen_size)
pygame.display.set_caption("Rubbish game")

# setup clock
FPS = 60
clock = pygame.time.Clock()

# game variables
clicking = False
paused = False
ended = False

score = 0
timer = 0

# functions called by clicking on buttons


def close_game():
    pygame.quit()
    sys.exit()


def update_click():
    '''Gets left mouse button state, stores it in clicking variable'''
    global clicking
    clicking = pygame.mouse.get_pressed()[0]


def unpause():
    global paused
    paused = False


def restart():
    global score, timer
    unpause()
    score = 0
    timer = 0
    new_item()
    item.sprite.rect.center = settings.screen_size / 2


def try_again():
    global ended
    ended = False


def new_item():
    new_item = Item(random.choice(item_types))
    item.add(new_item)


# main menu loop
def main_menu():
    global clicking
    while True:
        clock.tick(FPS)

        # evemt loop
        for event in pygame.event.get():
            if event.type == QUIT:
                close_game()

        update_click()

        draw_background()
        draw_logo()

        # htp: how to play
        htp_line_1 = draw_text(
            "How to play: Drag the items into the correct bins.", "white")
        htp_line_2 = draw_text(
            "Try to get as many correct as you can in 30s!", "white")
        screen.blit(htp_line_1, htp_line_1.get_frect(center=(middle_x, 490)))
        screen.blit(htp_line_2, htp_line_2.get_frect(center=(middle_x, 540)))

        # item displays
        for i in range(1, 9):
            # space vertically
            draw_y = (i % 4) * 100 + 80
            # draw in from sides
            x_offset = 60
            label = draw_text(item_names[i-1], "white")
            # split into two columns
            if i <= 4:
                # draw on left
                x = x_offset
                screen.blit(label, label.get_frect(
                    midleft=(x + 50, draw_y)))
            else:
                # draw on right
                x = settings.screen_size.x - x_offset
                screen.blit(label, label.get_frect(
                    midright=(x - 50, draw_y)))

            screen.blit(items[i-1], items[i-1].get_frect(
                center=(x, draw_y)))

        # update and draw buttons
        for button in menu_buttons:
            button.update(clicking)
            button.draw(screen)

        pygame.display.flip()


# pause menu loop
def pause_menu():
    global clicking, paused

    paused = True
    while paused:
        clock.tick(FPS)

        # evemt loop
        for event in pygame.event.get():
            if event.type == QUIT:
                close_game()

        update_click()

        draw_background()

        for button in pause_buttons:
            button.update(clicking)
            button.draw(screen)

        pygame.display.flip()


# main game loop
def game():
    global clicking, score, timer

    while timer < 30:
        # delta time
        dt = clock.tick(FPS) / 1000

        # evemt loop
        for event in pygame.event.get():
            if event.type == QUIT:
                close_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause_menu()

        update_click()

        draw_background()

        pause_button.update(clicking)
        pause_button.draw(screen)

        bins.draw(screen)

        item.update(clicking)
        item.draw(screen)

        # check collisions with bins
        for bin_sprite in bins:
            if bin_sprite.mask.overlap(item.sprite.mask,
                                       (item.sprite.rect.x - bin_sprite.rect.x,
                                        item.sprite.rect.y - bin_sprite.rect.y)):
                if bin_sprite.bin_type == item.sprite.item_type:
                    score += 1
                else:
                    score -= 1

                new_item()
                item.sprite.rect.center = settings.screen_size/2

        # score counter
        score_text = draw_text(f"Score: {score}", "white")
        screen.blit(score_text, (20, 20))

        # timer
        timer += dt
        timer_text = draw_text(str(round(timer, 1)), "white")
        screen.blit(timer_text, timer_text.get_frect(
            midtop=(middle_x, 20)))

        pygame.display.flip()

    end_screen()


# shows when time runs out
def end_screen():
    global score, clicking, ended

    ended = True
    while ended:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                close_game()

        update_click()

        draw_background()

        end_text = draw_text(f"Game over! You scored {score}", "white", True)
        screen.blit(end_text, end_text.get_frect(
            center=settings.screen_size/2))

        for button in end_buttons:
            button.update(clicking)
            button.draw(screen)

        pygame.display.flip()

    restart()
    game()


item_types = ["rubbish", "recycling", "foodscrap"]

# used as labels on main menu
item_names = ["Rubbish bag",
              "Plastic bag",
              "Cardboard box",
              "Newspaper",
              "Glass bottle",
              "Apple core",
              "Banana skin",
              "Fish bone"]

# create first item
item = pygame.sprite.GroupSingle()
new_item()

middle_y = settings.screen_size.y / 2
middle_x = settings.screen_size.x / 2
# create 3 bins
bin_y = settings.screen_size.y - 80
rubbish_bin = Bin((settings.screen_size.x / 4, bin_y), "rubbish")
recycle_bin = Bin((middle_x, bin_y), "recycling")
foodscrap_bin = Bin((settings.screen_size.x / (4/3), bin_y), "foodscrap")
bins = pygame.sprite.Group()
bins.add(rubbish_bin, recycle_bin, foodscrap_bin)


# create main menu buttons
start_button = Button("Start", (middle_x, middle_y), game)
quit_button = Button("Quit", (middle_x, middle_y + 70), close_game)
menu_buttons: list[Button] = [start_button, quit_button]

# create pause menu buttons
resume_button = Button("Resume", (middle_x, middle_y - 100), unpause)
restart_button = Button("Restart", (middle_x, middle_y - 50), restart)
pause_buttons: list[Button] = [
    resume_button, quit_button, restart_button]

# pausse button
pause_button = Button("Pause", (settings.screen_size.x - 20, 20), pause_menu)
pause_button.rect.topright = pause_button.rect.center

# endscreen buttons
try_again_button = Button("Try again", (middle_x, middle_y + 120), try_again)
end_buttons: list[Button] = [quit_button, try_again_button]

# Item images for main menu
items: list[pygame.Surface] = []
# take names from classes item_imgs
for item_group in item_imgs.values():
    for item_name in item_group:
        # load image of that name
        item_img = pygame.image.load(settings.get_file_path(
            f"images/{item_name}.png")).convert_alpha()
        item_img = pygame.transform.scale_by(item_img, 5)
        items.append(item_img)

# logo image
logo_img = pygame.image.load(
    settings.get_file_path("images/logo.png")).convert_alpha()
logo_img_scaled = pygame.transform.scale_by(logo_img, 7)


def draw_logo():
    screen.blit(logo_img_scaled, logo_img_scaled.get_frect(
        center=(middle_x, 150)))


# background image
background_img = pygame.image.load(
    settings.get_file_path("images/background.png")).convert()
# keeps 19:9 ratio
background_scaled = pygame.transform.scale(
    background_img, (settings.screen_size.y * 16/9, settings.screen_size.y))


def draw_background():
    screen.blit(background_scaled, background_scaled.get_frect(
        centerx=middle_x))


# start game at main menu
main_menu()
