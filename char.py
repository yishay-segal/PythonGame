import pygame
import random

pygame.mixer.init()
crash_sound = pygame.mixer.Sound('sounds/hit.wav')

trash_images = [pygame.image.load('img/bottle_photo-removebg-preview.png'), pygame.image.load('img/trash-can.png'),
                pygame.image.load('img/apple.png'), pygame.image.load('img/fish-trash.png'), pygame.image.load('img/carton-trash.png'),
                pygame.image.load('img/light-trash.png')]

def collide(obj1, obj2):
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.player_vel = 5
        # load all the images of the player
        for num in range (1, 5):
            img_left = pygame.image.load(f'img/char{num}.png')
            img_left = pygame.transform.scale(img_left, (40, 80))
            # instead of loading other images, just flip them
            img_right = pygame.transform.flip(img_left, True, False)
            self.images_left.append(img_left)
            self.images_right.append(img_right)
        self.image = self.images_left[self.index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.score = 0
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.jumpCount = 0
        self.direction = 0

    def update(self, screen):
        dx = 0
        dy = 0
        walk_cooldown = 5

        # get keypress
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not self.jumped and self.rect.y == 520 :
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_SPACE]:
            self.jumped = False
        if key[pygame.K_LEFT] and self.rect.x - self.player_vel > 0:
            dx -= self.player_vel
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.x + self.player_vel + 40 < 1000:
            dx += self.player_vel
            self.counter += 1
            self.direction = 1
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            else:
                self.image = self.images_left[self.index]



        # handle animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > 600:
            self.rect.bottom = 600
            dy = 0

        # draw player onto screen
        screen.blit(self.image, self.rect)

    def score_bar(self, screen, font):
        score_label = font.render(f'Score: {self.score}', 1, (255, 255, 255))
        screen.blit(score_label, (40, 15 + score_label.get_height()))


class Trash():
    def __init__(self, x, y, img):
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.v0 = random.random() * 3
        self.t = 1/60
        print(self.v0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, vel):
        self.rect.y += vel

    # def update(self, screen):
    #     # draw trash onto screen
    #     if self.rect.y < 700:
    #         self.rect.x += self.v0*self.t
    #         self.rect.y += 0.5* self.t**2
    #         self.t += 1/20
    #     screen.blit(self.image, self.rect)

    def off_screen(self, height):
        return not self.rect.bottom <= height and self.rect.top >= 0
    def collision(self, obj):
        return collide(self, obj)

class Enemy():
    COOLDOWN = 30

    def __init__(self, x, y):
        img = pygame.image.load('img/monkey1.png')
        img2 = pygame.image.load('img/monkey2.png')
        self.image = [pygame.transform.scale(img, (50, 75)), pygame.transform.scale(img2, (75, 75))]
        self.shooting = 0
        self.rect = self.image[self.shooting].get_rect()
        self.mask = pygame.mask.from_surface(self.image[self.shooting])
        self.rect.x = x
        self.rect.y = y
        self.trashes = []
        self.cool_down_counter = 0

    def move(self):
        if self.cool_down_counter == 0:
            random_number = random.randrange(150, 815)
            # print(random_number)
            self.rect.x = random_number

    def draw(self, screen):
        # print(self.shooting)
        screen.blit(self.image[self.shooting], self.rect)
        for trash in self.trashes:
            trash.draw(screen)


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move_trash(self, vel, obj, screen):
        self.cooldown()

        if len(self.trashes):
            if not self.trashes[-1].collision(self):
                self.shooting = 0

        for trash in self.trashes:
            trash.move(vel)
            # if not trash.collision(self):
            #     self.shooting = 0

            # print(trash.collision(self))
            if trash.off_screen(700):
                self.trashes.remove(trash)
            elif trash.collision(obj):
                obj.score += 1
                self.trashes.remove(trash)
                crash_sound.play()
                print('hit')

    def shoot(self):
        if self.cool_down_counter == 0:
            # print(f'image coords: {self.image}')
            trash = Trash(self.rect.x + 25, self.rect.y, trash_images[random.randrange(0, len(trash_images))])
            # print(trash.collision(self))
            print('new shoot')
            self.shooting = 1
            self.trashes.append(trash)
            self.cool_down_counter = 1

    # def change_image(self):
    #     if self.cool_down_counter ==

    def off_width(self, width, num):
        return not self.rect.left + num - 50 >= 0 and self.rect.right <= width + num - 50

