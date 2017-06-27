import sys, pygame
from random import randrange
from math import sqrt, pow

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
SPEED = [0, 1]
WIDTH = 750
HEIGHT = 600
PLAYERSPEED = 9
PLAYERSIZE = 30
BULLETSPEED = 2
BULLETRADIUS = 5
HIGHSCORE = 0


class Square:

    def __init__(self, surface):
        self._height = 20.0
        self._width = 20.0
        self._size = 20.0
        self.surface = surface
        self._speed = [0, 5]
        self._x_position = randrange(WIDTH - self._width)
        self._y_position = 125 - self._height - randrange(15)
        self.square = pygame.Rect(self._x_position, self._y_position, self._width, self._height)
        self.center_x = self.square.centerx
        self.center_y = self.square.centery
        self.bottom = self.square.bottom
        self.onscreen = True
        self.collision = False

    def draw(self):
        if self.center_y < HEIGHT + self._height:
            pygame.draw.rect(self.surface, RED, self.square)
        else:
            self.onscreen = False

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

    def check_collision(self, obj):
        distance = sqrt(pow(self.center_x - obj.center_x, 2) + pow(self.center_y - obj.center_y, 2))
        # if distance <= 45 and obj.bottom <= HEIGHT - 120:
        if distance <= self._size/2 + obj.size/2 and obj.onscreen:
            self.collision = True
            obj.collision = True
            print("collision")


class Player:

    def __init__(self, surface):
        self.collision = False
        self.surface = surface
        self.onscreen = True
        self._color = WHITE
        self.size = PLAYERSIZE
        self.center_x = WIDTH / 2
        self.center_y = HEIGHT - 120 - PLAYERSIZE/2
        self.vertices = [(self.center_x - self.size/2, HEIGHT - 120), (
            self.center_x + self.size/2, HEIGHT - 120),
            (self.center_x, HEIGHT - 120 - self.size)]

    def update_position(self):
        self.vertices = ((self.center_x - self.size / 2, HEIGHT - 120),
                           (self.center_x + self.size / 2, HEIGHT - 120),
                           (self.center_x, HEIGHT - 120 - self.size))

    def draw(self):
        # pygame.draw.circle(self.surface, WHITE, (int(self.center_x), int(self.center_y)), 5)
        pygame.draw.polygon(self.surface, WHITE, self.vertices)

    def move_left(self):
        self.center_x -= PLAYERSPEED
        self.update_position()

    def move_right(self):
        self.center_x += PLAYERSPEED
        self.update_position()


class Bullet:
    def __init__(self, surface, x_position):
        self.surface = surface
        self.onscreen = True
        self.collision = False
        self.speed = [0, -PLAYERSPEED]
        self._radius = BULLETRADIUS
        self.size = 2 * self._radius
        self.center_x = x_position
        self.center_y = HEIGHT - 120 - self.size
        self._rect = pygame.Rect(self.center_x, self.center_y - PLAYERSIZE / 2 - self._radius*2, self._radius * 2, self._radius * 2)

    def draw(self):
        if self._rect.centery > 125 and not self.collision:
            pygame.draw.ellipse(self.surface, RED, self._rect)
        else:
            self.onscreen = False

    def fly(self):
        self._rect = self._rect.move(self.speed)
        self.center_x = self._rect.centerx
        self.center_y = self._rect.centery
        self.draw()

    # def explode(self, ):
    #   print("bullet explodes when hitting an obstacle")


pygame.init()

size = WIDTH, HEIGHT

screen = pygame.display.set_mode(size)
squares = list()
squares.append(Square(screen))
bullets = list()
player = Player(screen)
counter = 0
score = 0

myfont = pygame.font.SysFont("monospace", 30)

text_score = myfont.render(str(score), 5, (255, 25, 0))
screen.blit(text_score, (375, 50))


while 1:
    counter += 1
    score += 1
    pygame.time.delay(40)

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(screen, player.center_x - BULLETRADIUS))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    for bullet in bullets:
        if bullet.onscreen:
            bullet.fly()

    new_squares = list()
    for square in squares:
        if not square.onscreen:
            squares.remove(square)
        else:
            for bullet in bullets:
                square.check_collision(bullet)
            if not square.collision:
                square.move()
                square.check_collision(player)
                new_squares.append(square)
            if square.collision:
                print("bang!!!")

    squares = new_squares

    if counter >= 10:
        for i in range(randrange(10)):
            squares.append(Square(screen))
        counter = 0
    # screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (0, 125), (1000, 125), 5)

    for square in squares:
        square.draw()
    if player.collision:
        if score > HIGHSCORE:
            HIGHSCORE = score
        score = 0
        player.collision = False
    text_score = myfont.render(str(score), 5, (255, 25, 0))
    text_highscore = myfont.render(str(HIGHSCORE), 5, (255, 25, 0))
    screen.blit(text_score, (375, 50))
    screen.blit(text_highscore, (450, 50))

    player.draw()
    pygame.display.flip()
