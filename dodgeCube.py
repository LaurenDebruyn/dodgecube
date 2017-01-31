import sys, pygame
from random import randrange
from math import sqrt, pow

BLACK = 0, 0, 0
WHITE = 255, 255, 255
SPEED = [0, 1]
WIDTH = 750
HEIGHT = 600
PLAYERSPEED = 7


class Square:

    def __init__(self, surface):
        self._height = 20.0
        self._width = 20.0
        self.surface = surface
        self._speed = [0, 5]
        self._x_position = randrange(WIDTH - self._width)
        self._y_position = 125 - self._height - randrange(15)
        self.square = pygame.Rect(self._x_position, self._y_position, self._width,
                                  self._height)
        self.center_x = self.square.centerx
        self.center_y = self.square.centery
        self.bottom = self.square.bottom

    def draw(self):
        if self._y_position < HEIGHT:
            pygame.draw.rect(self.surface, WHITE, self.square)

    def move(self):
        self.adjust_speed()
        self.adjust_size()
        self.square = self.square.move(self._speed)
        self.center_x = self.square.centerx
        self.center_y = self.square.centery
        self.bottom = self.square.bottom

    def adjust_speed(self):
        if self._x_position < WIDTH/2 - 2*self._width:
            self._speed[0] -= 0.05
        elif self._x_position > WIDTH/2 + 2*self._width:
            self._speed[0] += 0.05

    def adjust_size(self):
        self._width *= 1.001
        self._height *= 1.001
        self.square = self.square.inflate(self._width - 20, self._height - 20)


class Player:

    def __init__(self, surface):
        self.surface = surface
        self.collision = False
        self._color = WHITE
        self._size = 30
        self._center = WIDTH / 2
        self._pointlist = [(self._center - self._size/2, HEIGHT - 120), (
            self._center + self._size/2, HEIGHT - 120),
            (self._center, HEIGHT - 120 - self._size)]

    def update_position(self):
        self._pointlist = ((self._center - self._size / 2, HEIGHT - 120),
                           (self._center + self._size / 2, HEIGHT - 120),
                           (self._center, HEIGHT - 120 - self._size))

    def draw(self):
        pygame.draw.polygon(self.surface, WHITE, self._pointlist)

    def move_left(self):
        self._center -= PLAYERSPEED
        self.update_position()

    def move_right(self):
        self._center += PLAYERSPEED
        self.update_position()

    def check_collision(self, obj):
        distance = sqrt(pow(obj.center_x - self._center, 2) + pow(obj.center_y - (HEIGHT - 120), 2))
        # print(distance)
        if distance <= 45 and obj.bottom <= HEIGHT - 120:
            self.collision = True
            print("DEAD")


pygame.init()

size = 750, 600

screen = pygame.display.set_mode(size)
squares = list()
squares.append(Square(screen))
player = Player(screen)
counter = 0
score = 0

myfont = pygame.font.SysFont("monospace", 30)

text_score = myfont.render(str(score), 5, (255, 25, 0))
screen.blit(text_score, (375, 50))


while not player.collision:
    counter += 1
    score += 1
    pygame.time.delay(40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    for square in squares:
        square.move()
        player.check_collision(square)
    if counter >= 10:
        for i in range(randrange(10)):
            squares.append(Square(screen))
        counter = 0
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (0, 125), (1000, 125), 5)

    for square in squares:
        square.draw()

    text_score = myfont.render(str(score), 5, (255, 25, 0))
    screen.blit(text_score, (375, 50))

    player.draw()
    pygame.display.flip()


