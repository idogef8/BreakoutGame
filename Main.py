import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

my_font = pygame.font.SysFont('Roboto', 20)

class Player(pygame.Rect):

    def __init__(self, x, y):
        super().__init__(x, y, 100, 25)   # arbitrary values TODO weak
        self.vx = 0

    def draw(self):
        pygame.draw.rect(screen, 'orange', self, 0) # fill
        pygame.draw.rect(screen, 'black', self, 1) # outline

    def update(self):
        self.x += self.vx
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width

class Ball(pygame.Rect):
    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.vx = random.randint(0, 3) * random.choice([1, -1])
        self.vy = random.randint(4, 6) # TODO tweaking

    def draw(self):
        pygame.draw.rect(screen, 'white', self, 0) # check out my new graphics!

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x >= screen.get_width() - self.width and self.vx > 0:
            self.vx *= -1
        if self.x <= 0 and self.vx < 0:
            self.vx *= -1
        if self.y <= 0 and self.vy < 0:
            self.vy *= -1
        if self.y >= screen.get_height() - self.height and self.vy > 0:
            self.x = screen.get_width()//2
            self.y = screen.get_height()//2

class Brick(pygame.Rect):
    width = 115
    height = 35

    def __init__(self, x, y):
        super().__init__(x, y, Brick.width, Brick.height)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self):

        pygame.draw.rect(screen, self.color, self, 0, border_radius=5) # fill
        pygame.draw.rect(screen, 'black', self, 1, border_radius=5)



# initializing

player = Player(screen.get_width()/2 - 50, screen.get_height() - 50)
ball = Ball(screen.get_width()/2 - 10, screen.get_height()/2 + 20, 20)
bricks = []
for x in range(0, 6):
    for y in range(0, 10):
        bricks.append(Brick(10 + (y * (Brick.width + 10)), 10 + (x * (Brick.height + 10))))




while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += -5
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += 5
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += -5

    # Do logical updates here.

    player.update()
    ball.update()


    if ball.colliderect(player):
        ball.vy *= -1
        ball.y = player.y - ball.width # perhaps sideways collision would look better?
        player_center = player.x + player.width / 2
        ball_center = (ball.x + ball.width / 2)
        diff = ball_center - player_center
        ball.vx += diff // 10

    for Brick in bricks:
        if ball.colliderect(Brick):
            bricks.remove(Brick)
            ball.vy *= -1





    screen.fill('grey')  # Fill the display with a solid color

    # Render the graphics here.

    player.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()

    text_surface = my_font.render('Score: ', False, (0, 0, 0))
    screen.blit(text_surface, (screen.get_width() - text_surface.get_width() - 10, screen.get_height() - text_surface.get_height() - 10))



    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)

