# build 2048 in python using pygame!!
import pygame
import random

pygame.init()


# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')

# win image
dance_win=pygame.image.load("images/3.png").convert_alpha()
d_win=dance_win.get_rect()
dance_win = pygame.transform.scale(dance_win, (150, 150))
d_win.topleft = (100, 200)

# lose image
lose_img=pygame.image.load("images/1.png").convert_alpha()
l_img=lose_img.get_rect()
lose_img = pygame.transform.scale(lose_img, (150, 170))
l_img.topleft = (110, 165)


# levels_img=pygame.image.load("images/levels.png").convert_alpha()
# lvl_img=levels_img.get_rect()
# levels_img= pygame.transform.scale(levels_img, (450, 500))
# lvl_img.topleft = (400, 405)



# el vitesse mta3 el morab3at 9adeh yab9a wa9et bech yt3ada
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library


# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
# board or board_values  hia el matrice
game_over = False
win=False
spawn_new = True
init_count = 0
direction = ''
score = 0
# file = open('high_score', 'r')
# init_high = int(file.readline())
# file.close()
high_score = 1000


# fonctions

# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 300], 0, 10)
    # kober el moraba3 el ak7el eli  yo5rejli ki na5serrr
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    # les msgs eli ijiyouni ki na5sar
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))
    screen.blit(lose_img, l_img.topleft)


def draw_win():
    pygame.draw.rect(screen, 'white', [50, 50, 300, 300], 0, 10)
    game_win_text1 = font.render('You win!', True, 'black')
    game_win_text2 = font.render('Press Enter to ', True, 'black')
    game_win_text3 = font.render('pass to next level ', True, 'black')
    screen.blit(game_win_text1, (130, 65))
    screen.blit(game_win_text2, (110, 105))
    screen.blit(game_win_text3, (110, 165))
    screen.blit(dance_win, d_win.topleft)
    
def win_all_game():
    pygame.draw.rect(screen, 'white', [50, 50, 300, 300], 0, 10)
    game_win_text1 = font.render('You win ', True, 'black')
    game_win_text2 = font.render('all the game!', True, 'black')
  
    screen.blit(game_win_text1, (130, 65))
    screen.blit(game_win_text2, (110, 105))

    screen.blit(dance_win, d_win.topleft)
    

# take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board_lv1():
    pygame.draw.rect(screen, (187, 173, 160), [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {1000}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 440))
    # screen.blit(levels_img, (10, 450))
    # screen.blit(pygame.transform.scale(pygame.image.load('images/levels.png'), (580, 120)), (0, 470))
    timer_text = timer_font.render(f'Time 120 seconds:'  + str(level1_time / 1000 - timer_seconds), True, 'black' )
    screen.blit(timer_text, (10, 470))
    pass

def draw_board_lv2():
    pygame.draw.rect(screen, (187, 173, 160), [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {3000}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    timer_text = timer_font.render(f'Time 300 seconds:'  + str(level2_time / 1000 - timer_seconds), True, 'black' )
    screen.blit(timer_text, (10, 470))
    pass


def draw_board_lv3():
    pygame.draw.rect(screen, (187, 173, 160), [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {5000}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    timer_text = timer_font.render(f'Time 700 seconds:'  + str(level3_time / 1000 - timer_seconds), True, 'black' )
    screen.blit(timer_text, (10, 470))
    
    pass

def draw_board_lv4():
    pygame.draw.rect(screen, (187, 173, 160), [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {10000}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    timer_text = timer_font.render(f'Time 1200 seconds:'  + str(level4_time / 1000 - timer_seconds), True, 'black' )
    screen.blit(timer_text, (10, 470))
    pass

def draw_board_lv5():
    pygame.draw.rect(screen, (187, 173, 160), [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {20000}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    timer_text = timer_font.render(f'Time 2000 seconds :'  + str(level5_time / 1000 - timer_seconds), True, 'black' )
    screen.blit(timer_text, (10, 470))
    
    pass
# dictionary for colors and images
colors = {0: ((204, 192, 179), None),
          2: ((237, 224, 200), pygame.transform.scale(pygame.image.load('images/20.png'), (75, 75))),
          4: ((237, 224, 200), pygame.transform.scale(pygame.image.load('images/50.png'), (75, 75))),
          8: ((242, 177, 121), pygame.transform.scale(pygame.image.load('images/100.png'), (75, 75))),
          16: ((245, 149, 99),  pygame.transform.scale(pygame.image.load('images/200.png'), (75, 75))),
          32: ((246, 124, 95),  pygame.transform.scale(pygame.image.load('images/500.png'), (75, 75))),
          64: ((246, 94, 59),  pygame.transform.scale(pygame.image.load('images/1d.png'), (75, 75))),
          128: ((237, 207, 114),  pygame.transform.scale(pygame.image.load('images/2d.png'), (75, 75))),
          256: ((237, 204, 97),  pygame.transform.scale(pygame.image.load('images/5d.png'), (75, 75))),
          512: ((237, 200, 80),  pygame.transform.scale(pygame.image.load('images/10d.jpg'), (75, 75))),
          1024: ((237, 197, 63),  pygame.transform.scale(pygame.image.load('images/20d.jpg'), (75, 75))),
          2048: ((237, 194, 46),  pygame.transform.scale(pygame.image.load('images/50d.jpg'), (75, 75))),
          'light text': ((249, 246, 242), None),
          'dark text': ((119, 110, 101), None),
          'other': ((0, 0, 0), None),
          'bg': ((187, 173, 160), None)}




# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            color, img = colors[value]
            if img:
                # create rect for tile
                tile_rect = pygame.Rect(j * 95 + 20, i * 95 + 20, 75, 75)
                # create rect for image with max size equal to tile size
                img_rect = img.get_rect()
                img_rect.width = min(img_rect.width, tile_rect.width)
                img_rect.height = min(img_rect.height, tile_rect.height)
                img_rect.center = tile_rect.center
                # clip image to fit within tile boundaries
                img_rect.clamp_ip(tile_rect)
                # draw tile background and clipped image
                pygame.draw.rect(screen, color, tile_rect, 0, 5)
                screen.blit(img, img_rect)
            else:
                pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
                if value > 0:
                    if value > 8:
                        value_color = colors['light text'][0]
                    else:
                        value_color = colors['dark text'][0]
                    value_len = len(str(value))
                    font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                    screen.blit(value_text, text_rect)
                    pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)






# 
def wait_for_key(key):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == key:
                return
            


# main game loop

timer_font = pygame.font.SysFont('arial', 30)

level1_score = 100
# Set the initial time for level 1
level1_time = 120000

level2_score = 300
level2_time = 300000

level3_score = 5000
level3_time = 700000

level4_score = 10000
level4_time = 1200000

level5_score = 200000
level5_time = 2000000

# Initialize the clock object
clock = pygame.time.Clock()




# Main game loop
run = True
level = 1
timer = 0 


while run:
    # Update the clock object and get the time since the last call
    dt = clock.tick(fps)
    timer += dt

    # Convert the timer value to seconds
    timer_seconds = int(timer / 1000)

    # Check if the time limit for the current level has been reached
    if level == 1 and timer_seconds >= level1_time / 1000:
        draw_over()
        pygame.display.flip()
        wait_for_key(pygame.K_RETURN)
        run = False

    screen.fill('gray')

    # Draw the timer text on the screen
    timer_text = timer_font.render('Time: ' + str(level1_time / 1000 - timer_seconds), True, 'white')
    screen.blit(timer_text, (10, 10))

    if level == 1:
        if score >= level1_score and timer_seconds <= level1_time / 1000:
            draw_win()
            pygame.display.flip()
            wait_for_key(pygame.K_RETURN)
            level = 2
            timer = 0  # Reset the timer for the next level
        draw_board_lv1()
        draw_pieces(board_values)
    elif level == 2:
        if score >= level2_score and timer_seconds <= level2_time / 1000:
            draw_win()
            pygame.display.flip()
            wait_for_key(pygame.K_RETURN)
            level = 3
            timer = 0
        draw_board_lv2()
        draw_pieces(board_values)

    elif level == 3:
        if score >= level3_score and timer_seconds <= level3_time / 1000:
            draw_win()
            pygame.display.flip()
            wait_for_key(pygame.K_RETURN)
            level = 4
            timer = 0
        draw_board_lv3()
        draw_pieces(board_values)

    elif level == 4:
        if score >= level4_score and timer_seconds <= level4_time / 1000:
            draw_win()
            pygame.display.flip()
            wait_for_key(pygame.K_RETURN)
            level = 5
            timer = 0
        draw_board_lv4()
        draw_pieces(board_values)


    elif level == 5:
        if score >= level5_score and timer_seconds <= level5_time / 1000:
            win_all_game()
            pygame.display.flip()
            wait_for_key(pygame.K_RETURN)
            level = 6
            timer = 0


        draw_board_lv5()
        draw_pieces(board_values)
    elif level == 6:
    # handle winning the entire game
    # wait for the player to press Enter
        win_all_game()
        pygame.display.flip()
        wait_for_key(pygame.K_RETURN)
        run = False



    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1

    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True

    if game_over:
        draw_over()
        pygame.display.flip()
        wait_for_key(pygame.K_RETURN)
        board_values = [[0 for _ in range(4)] for _ in range(4)]
        spawn_new = True
        init_count = 0
        score = 0
        direction = ''
        game_over = False
        win = False
        level = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

            if event.key == pygame.K_RETURN:
                if game_over:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    direction = ''
                    game_over = False
                    win = False
                    level = 1
                elif win:
                    wait_for_key(pygame.K_RETURN)
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    direction = ''
                    game_over = False
                    win = False
                    if level == 1 and score >= 1000 and score <= 1200:
                        level = 2
                    elif level == 2 and score >= 3000:
                        level = 3
                    elif level == 3 and score >= 5000:
                        level = 4
                    elif level == 4 and score >= 10000:
                        level = 5
                        # win_all_game()
                    elif level == 5 and score >= 20000:
                        level = 6
                    else:
                        run = False
                        # level == 1

                        

    pygame.display.flip()

pygame.quit()

