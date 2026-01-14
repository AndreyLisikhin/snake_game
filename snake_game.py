import pygame
import sys
import random
pygame.init()

SIZE_BLOCK = 20
FRAME_COLOR = (0,255,204)
WHITE = (255,255,255)
BLUE = (204,255,255)
RED = (221,0,0)
HEADER_COLOR = (0,204,153)
SNAKE_COLOR = (0,102,0)
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN=1

size = [SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK+MARGIN*COUNT_BLOCKS,
        SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK+MARGIN*COUNT_BLOCKS+HEADER_MARGIN]
print(size)

screen=pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()
courier = pygame.font.SysFont("courier", 36)
courier2 = pygame.font.SysFont("courier", 50)

class SnakeBlock:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def is_inside(self):
        return 0<=self.x<COUNT_BLOCKS and 0<=self.y<COUNT_BLOCKS
    def __eq__(self, other):
        return isinstance(other,SnakeBlock) and self.x==other.x and self.y==other.y

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color_idle = (0, 200, 200)
        self.color_hover = (0, 150, 150)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_idle

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        text_surface = courier.render(self.text, True, WHITE)
        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2
            )
        )

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            self.rect.collidepoint(event.pos))


def get_random_empty_block():
    x = random.randint(0,COUNT_BLOCKS-1)
    y = random.randint(0,COUNT_BLOCKS-1)
    empty_block = SnakeBlock(x,y)
    while empty_block in snake_block:
        empty_block.x = random.randint(0,COUNT_BLOCKS-1)
        empty_block.y = random.randint(0,COUNT_BLOCKS-1)
    return empty_block

def draw_block(color,row,column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1), SIZE_BLOCK,
                                     SIZE_BLOCK])

def draw_menu():
    screen.fill(FRAME_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], size[1]])

    title = courier2.render("SNAKE GAME", True, WHITE)
    screen.blit(title, (size[0] // 2 - title.get_width() // 2, 180))

    start_button.draw()
    exit_button.draw()

    pygame.display.flip()

start_button = Button(size[0] // 2 - 100, 280, 200, 50, "START")
exit_button = Button(size[0] // 2 - 100, 350, 200, 50, "EXIT")


def start_game():
    global snake_block, apple, d_row, d_col, total, speed
    snake_block = [SnakeBlock(9,8), SnakeBlock(9,9),SnakeBlock(9,10)]
    apple = get_random_empty_block()
    d_row = 0
    d_col = 1
    total = 0
    speed = 1

GAME_MENU = 0
GAME_RUN = 1
game_state = GAME_MENU

snake_block = []
apple = None
d_row = 0
d_col = 0
total = 0
speed = 1

while True:
    timer.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('exit')
            pygame.quit()
            sys.exit()

        if game_state==GAME_MENU:
            if start_button.is_clicked(event):
                start_game()
                game_state = GAME_RUN
            if exit_button.is_clicked(event):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game()
                    game_state = GAME_RUN
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


        elif game_state==GAME_RUN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col !=0:
                    d_row=-1
                    d_col=0
                elif event.key == pygame.K_DOWN and d_col!=0:
                    d_row=1
                    d_col=0
                elif event.key == pygame.K_LEFT and d_row!=0:
                    d_row = 0
                    d_col=-1
                elif event.key == pygame.K_RIGHT and d_row!=0:
                    d_row=0
                    d_col=1

    if game_state==GAME_MENU:
        draw_menu()
        continue


    screen.fill(FRAME_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, [0,0,size[0], HEADER_MARGIN])

    text_total = courier.render(f"Total:{total}", 0, WHITE)
    text_speed = courier.render(f"Speed:{speed}", 0, WHITE)
    screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
    screen.blit(text_speed, (SIZE_BLOCK+230, SIZE_BLOCK))

    for row in range(COUNT_BLOCKS):
        for column in range(COUNT_BLOCKS):
            if (row+column)%2==0:
                color = BLUE
            else:
                color = WHITE
            draw_block(color,row,column)

    head = snake_block[-1]
    if not head.is_inside():
        print(f'Crash\nTotal: {total}\nSpeed: {speed}')
        pygame.quit()
        sys.exit()

    draw_block(RED,apple.x,apple.y)
    for block in snake_block:
        draw_block(SNAKE_COLOR, block.x,block.y)

    if apple == head:
        total+=1
        speed=total//5+1
        snake_block.append(apple)
        apple = get_random_empty_block()

    new_head = SnakeBlock(head.x+d_row,head.y+d_col)
    if new_head in snake_block:
        print(f'Crash yourself\nTotal: {total}\nSpeed: {speed}')
        pygame.quit()
        sys.exit()
    snake_block.append(new_head)
    snake_block.pop(0)

    pygame.display.flip()
    timer.tick(3+speed)
print(total)