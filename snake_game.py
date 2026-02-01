import pygame
import sys
import random
import os
import json

pygame.init()

SIZE_BLOCK = 20
FRAME_COLOR = (0,255,204)
WHITE = (255,255,255)
BLACK = (6,2,8)
BLUE = (204,255,255)
RED = (221,0,0)
HEADER_COLOR = (0,204,153)
SNAKE_COLOR = (0,102,0)
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN=1
WIDTH=800

size = [SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK+MARGIN*COUNT_BLOCKS,
        SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK+MARGIN*COUNT_BLOCKS+HEADER_MARGIN]
print(size)

screen=pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')
timer = pygame.time.Clock()
font_big = pygame.font.SysFont("courier", 48)
font = pygame.font.SysFont("courier", 32)

courier = pygame.font.SysFont("courier", 36)
courier2 = pygame.font.SysFont("courier", 50)
player_name =""
MAX_NAME_LEN=10
score_saved = False
def clear_score():
    save_scores([])

def handle_name_input(event):
    global player_name
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            player_name = player_name[:-1]
        elif event.key == pygame.K_RETURN:
            return True  # имя введено
        else:
            if len(player_name) < 10:
                player_name += event.unicode
    return False


def draw_name_screen():
    screen.fill((30, 30, 30))

    title = courier.render(f"Введите имя: {player_name}", True, WHITE)

    screen.blit(title, (size[0]//2 - title.get_width()//2, 150))

    button_play.draw()
    button_exit.draw()

    pygame.display.flip()



def load_scores():
    if not os.path.exists("scores.json"):
        return []
    with open("scores.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_scores(scores):
    with open("scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=4)

def add_score(name, score):
    scores = load_scores()
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:5]
    save_scores(scores)

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
        screen.blit(text_surface,(self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2))

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            self.rect.collidepoint(event.pos))

def draw_pause():
    screen.fill(HEADER_COLOR)
    pause_text = courier2.render("Pause", True, WHITE)
    screen.blit(pause_text, (size[0]//2 - pause_text.get_width()//2,200))
    continue_button.draw()
    menu_button.draw()

    pygame.display.flip()

def draw_game_over():
    screen.fill(FRAME_COLOR)

    title = courier.render("GAME OVER", True, RED)
    score_text = courier.render(f"Score: {total}", True, BLACK)
    speed_text = courier.render(f"Speed: {speed}", True, BLACK)

    screen.blit(title, (size[0]//2 - title.get_width()//2, 80))
    screen.blit(score_text, (size[0]//2 - score_text.get_width()//2, 160))
    screen.blit(speed_text, (size[0]//2 - speed_text.get_width()//2, 200))

    menu_button.draw()
    restart_button.draw()

    pygame.display.flip()



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

def draw_leaderboard_windows():
    screen.fill(HEADER_COLOR)

    title = courier2.render("LEADERS BOARD", True, WHITE)
    screen.blit(title, (size[0] // 2 - title.get_width() // 2, 80))
    draw_leaderboard(100, 120)

    menu_button.draw()

    pygame.display.flip()


def draw_leaderboard(x, y):
    scores = load_scores()
    if not scores:
        line = courier.render("—", True, WHITE)
        screen.blit(
            line,
            (size[0] // 2 - line.get_width() // 2, y + 40)
        )
        return

    for i, record in enumerate(scores):
        text = f"{i+1}. {record['name']} — {record['score']}"
        line = courier.render(text, True, WHITE)
        screen.blit(line, (size[0]//2-line.get_width()//2, y + 40 + i * 30))


def draw_menu():
    screen.fill(FRAME_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], size[1]])

    title = courier2.render("SNAKE GAME", True, WHITE)
    screen.blit(title, (size[0] // 2 - title.get_width() // 2, 180))

    start_button.draw()
    exit_button.draw()
    button_leaderboard.draw()

    pygame.display.flip()

button_play = Button(size[0] // 2 - 100, 280, 200, 50, "PLAY")
button_exit = Button(size[0] // 2 - 100, 350, 200, 50, "EXIT")
button_leaderboard = Button(size[0] // 2 - 100, 420, 200, 50, "LEADERS")
start_button = Button(size[0] // 2 - 100, 280, 200, 50, "START")
exit_button = Button(size[0] // 2 - 100, 350, 200, 50, "EXIT")
continue_button = Button(size[0] // 2 - 100, 280, 200, 50, "CONTINUE")
menu_button = Button(size[0] // 2 - 100, 350, 200, 50, "MENU")
restart_button = Button(size[0] // 2 - 100, 280, 200, 50, "RESTART")

def start_game():
    global snake_block, apple, d_row, d_col, total, speed, score_saved
    snake_block = [SnakeBlock(9,8), SnakeBlock(9,9),SnakeBlock(9,10)]
    apple = get_random_empty_block()
    d_row = 0
    d_col = 1
    total = 0
    speed = 1
    score_saved=False

GAME_MENU = 0
GAME_RUN = 1
GAME_PAUSE =2
GAME_OVER =3
GAME_LEADER = 4
GAME_NAME=5
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

        if game_state == GAME_NAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(player_name)>0:
                    start_game()
                    game_state = GAME_RUN
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.unicode.isprintable() and len(player_name)<MAX_NAME_LEN:
                    player_name += event.unicode
            elif button_play.is_clicked(event):
                start_game()
                game_state = GAME_RUN
            elif button_exit.is_clicked(event):
                game_state = GAME_MENU

        elif game_state==GAME_MENU:
            if button_leaderboard.is_clicked(event):
                game_state = GAME_LEADER
            if start_button.is_clicked(event):
                game_state = GAME_NAME
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


        elif game_state==GAME_LEADER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = GAME_MENU
            if menu_button.is_clicked(event):
                game_state = GAME_MENU


        elif game_state==GAME_RUN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = GAME_PAUSE
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
        elif game_state==GAME_PAUSE:
            if menu_button.is_clicked(event):
                game_state = GAME_MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = GAME_MENU
                elif event.key == pygame.K_RETURN:
                    game_state = GAME_RUN
        elif game_state==GAME_OVER:
            if restart_button.is_clicked(event):
                start_game()
                game_state = GAME_RUN
            if menu_button.is_clicked(event):
                game_state = GAME_MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_game()
                    game_state = GAME_RUN
                elif event.key == pygame.K_ESCAPE:
                    game_state = GAME_MENU

    if game_state==GAME_NAME:
        draw_name_screen()
        continue
    if game_state==GAME_MENU:
        draw_menu()
        continue
    if game_state==GAME_LEADER:
        draw_leaderboard_windows()
        continue
    if game_state == GAME_PAUSE:
        draw_pause()
        continue
    if game_state == GAME_OVER:
        if not score_saved:
            add_score(player_name, total)
            score_saved = True
        draw_game_over()
        continue
    if game_state == GAME_RUN:
        head = snake_block[-1]
        if not head.is_inside():
            game_state = GAME_OVER
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
        #if not score_saved:
            #print('game over')
            #add_score(player_name, total)
            #score_saved = True
        game_state = GAME_OVER
        continue

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
       #if not score_saved:
            #add_score(player_name, total)
            #score_saved = True
        game_state = GAME_OVER
    snake_block.append(new_head)
    snake_block.pop(0)

    pygame.display.flip()
    timer.tick(3+speed)
print(total)