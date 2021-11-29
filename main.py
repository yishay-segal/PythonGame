import pygame
import button
import char
import random

pygame.font.init()
pygame.init()

background_color = (0, 0, 0)
(width, height) = (1000, 700)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Trash Monkeys')
screen.fill(background_color)
pygame.display.flip()
clock = pygame.time.Clock()

# fonts for the game
main_font = pygame.font.SysFont('comicsans', 40)
title_font = pygame.font.SysFont('comicsans', 100)

# load button images
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()

# load background images
start_background = pygame.image.load('img/background1.jpg').convert_alpha()
open_background = pygame.image.load('img/something.jpg')

# create button instances
start_button = button.Button(330, 450, start_img, 0.6)
exit_button = button.Button(530, 450, exit_img, 0.6)

# light shade of the button
color_light = (170, 170, 170)
# dark shade of the button
color_dark = (100, 100, 100)
WHITE = (255, 255, 255)

# level_one_time = 60
# timer = 3600

level_one_time = 30
timer = 1800
pause = False


def display_clock():
    global timer
    global level_one_time
    global pause
    # clock.tick(60)
    timer -= 1
    clock_font = pygame.font.SysFont('comicsans', 40)
    clock_label = clock_font.render(f'Time left: {str(level_one_time)}', 1, WHITE)

    if timer % 60 == 0 and not pause:
        level_one_time -= 1
    if level_one_time == -1:
        pause = True
        lose_label = main_font.render('You Lost', 1, WHITE)
        screen.blit(lose_label, (width / 2 - lose_label.get_width() / 2, 350))
        print('The time had expiered')

    screen.blit(clock_label, (820, 10))


def display_won():
    global pause
    pause = True
    win_label = main_font.render('You Won', 1, WHITE)
    screen.blit(win_label, (width / 2 - win_label.get_width() / 2, 350))
    # print('The time had expiered')


def display_level(level):
    level_label = main_font.render(f'Level: {level}', 1, WHITE)
    screen.blit(level_label, (40, 10))


# def display_score():
#     score_label = main_font.render('Score: 5', 1, WHITE)
#     screen.blit(score_label, (40, 15 + score_label.get_height()))


def show_rules():
    rules_font = pygame.font.SysFont('comicsans', 30)
    rules_label = rules_font.render(f'Welcome to our game', 1, WHITE)
    rules_label2 = rules_font.render(f'You need to catch the the trash that is thrown to you', 1, WHITE)
    rules_label3 = rules_font.render(f'and avoid catch the good stuff that are thrown at you', 1, WHITE)
    screen.blit(rules_label, (width / 2 - rules_label.get_width() / 2, 350))
    screen.blit(rules_label2, (width / 2 - rules_label2.get_width() / 2, 378))
    screen.blit(rules_label3, (width / 2 - rules_label3.get_width() / 2, 406))


def display_open_background():
    title_label = title_font.render('Trash Monkeys', 1, (255, 255, 255))
    screen.blit(pygame.transform.scale(open_background, (1000, 700)), (0, 0))
    screen.blit(title_label, (width / 2 - title_label.get_width() / 2, 350))


def collide(obj1, obj2):
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


# start_button.draw(screen)
# exit_button.draw(screen)

player = char.Player(600, 500)
# trash = char.Trash(100, 100)
# enemy = char.Enemy(150, 20)

FPS = 60

def main_menu():
    level = 0
    run = True

    monkey_group = 0
    score = 0

    enemies = []
    start = 0

    while run:
        clock.tick(FPS)
        # pos = pygame.mouse.get_pos()
        # print(pos)
        start_ticks = 0
        if level == 0:
            display_open_background()

            if start_button.draw(screen):
                level += 1
                screen.fill((0, 0, 0))
                screen.blit(pygame.transform.scale(start_background, (1000, 700)), (0, 0))

            if not level and exit_button.draw(screen):
                run = False
                # print('exit')

        # start = 0
        if level:
            # clock.tick(FPS)
            # print(start)
            start += 1
            seconds = start / 100
            # print(seconds)
            # print(seconds)

            if seconds < 3:
                show_rules()
            elif 3 < seconds < 3.5:
                print('clear the screen')
                screen.fill((0, 0, 0))
                screen.blit(pygame.transform.scale(start_background, (1000, 700)), (0, 0))
            elif seconds > 3.5 and not pause:
                # print('draw players')

                screen.blit(pygame.transform.scale(start_background, (1000, 700)), (0, 0))
                for monkey in enemies:
                    monkey.draw(screen)

                if len(enemies) == 0:
                    monkey_group += 2
                    for i in range(monkey_group):
                        random_number = random.randrange(150, 815)
                        monkey = char.Enemy(random_number, 10)
                        enemies.append(monkey)
                player.update(screen)
                if player.score == 10:
                    display_won()
                display_clock()
                display_level(level)
                # display_score()
                player.score_bar(screen, main_font)

                for monkey in enemies[:]:
                    # clock.tick(FPS)
                    # random_num = random.randrange(-10, 10)
                    # if not monkey.off_width(1000, random_num):
                    #     monkey.move(random_num)
                    monkey.move_trash(level, player, screen)

                    if random.randrange(0, 2 * 60) == 1:
                        monkey.move()
                        monkey.shoot()

                pygame.display.update()
            # start += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()


main_menu()
