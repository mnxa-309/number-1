from pygame import *

init()
clock = time.Clock()
windows = display.set_mode((600, 600))
display.set_caption("Пинг-понг")
background = transform.scale(image.load("fon.png"), (600, 600))
BLACK = (0, 0, 0)
game_over = False


class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = Rect(x, y, width, height)
        self.fill_color = BLACK
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        draw.rect(windows, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        windows.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = transform.scale(image.load(filename), (width, height))

    def draw(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))


ball = Picture('money.png', 140, 130, 50, 50)
platform_bottom = Picture('platform.png', 250, 550, 100, 30)
platform_top = Picture('platform.png', 250, 20, 100, 30)

dx = 5
dy = 5
move_left = False
move_right = False
move_left_top = False
move_right_top = False

while not game_over:
    windows.blit(background, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game_over = True
        elif e.type == KEYDOWN:
            if e.key == K_RIGHT:
                move_right = True
            elif e.key == K_LEFT:
                move_left = True
            elif e.key == K_d:
                move_right_top = True
            elif e.key == K_a:
                move_left_top = True
        elif e.type == KEYUP:
            if e.key == K_RIGHT:
                move_right = False
            elif e.key == K_LEFT:
                move_left = False
            elif e.key == K_d:
                move_right_top = False
            elif e.key == K_a:
                move_left_top = False

    if move_right:
        platform_bottom.rect.x += 10
    if move_left:
        platform_bottom.rect.x -= 10
    if move_right_top:
        platform_top.rect.x += 10
    if move_left_top:
        platform_top.rect.x -= 10

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.x > 550 or ball.rect.x < 0:
        dx *= -1
    if ball.rect.colliderect(platform_bottom.rect):
        dy *= -1
    if ball.rect.colliderect(platform_top.rect):
        dy *= -1

    if ball.rect.y > 600 or ball.rect.y < -50:
        time_text = Label(100, 260, 1, 1, BLACK)
        time_text.set_text('ПОРАЖЕНИЕ', 60, (200, 0, 0))
        time_text.draw(10, 10)
        display.update()
        time.delay(2000)
        game_over = True
        continue

    platform_bottom.draw()
    platform_top.draw()
    ball.draw()
    display.update()
    clock.tick(40)
