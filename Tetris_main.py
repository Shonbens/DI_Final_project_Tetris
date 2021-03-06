import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  # colors based on index
        self.rotation = 0  # shape starts with 0 rotation, when key is pressed this is increased.


def create_grid(locked_pos={}):  # stores the taken positions with colors.
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]  # create one list for every row, base grid.
    # If there is a shape a locked position, retrieve it and change the value in the grid.
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):  # makes the shape variables readable by the computer.
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]  # checks the rotation and matches it to the shape

    for i, line in enumerate(format):  # get the line from a row and loop to check for 0 or .
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))  # take current shape value and ads it to column and row

    for i, pos in enumerate(positions):  # offsets the values to ignore the '.' lines and makes it more accurate.
        positions[i] = (pos[0] - 2, pos[1] - 4)  # -4 spawns the shape outside the screen .

    return positions


def valid_space(shape, grid):
    # gets all the positions of our 10x20 grid, only adds it if its empty.
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]  # converts it to a 1D list, easier to loop.

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:  # the shape spawns in -4, so we don't want it to check outside the screen.
                return False
    return True


def check_lost(positions):  # checks if the shape passed the edges and fails the game.
    for pos in positions:  # if position is greater than 1 return false else return true and fail.
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():  # Grabs a random shape each time.
    return Piece(5, 0, random.choice(shapes))


def draw_menu_text(surface, text, size, color):
    # Text style
    font = pygame.font.SysFont("Viking", size)
    label = font.render(text, 1, color)

    # Location
    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height - 400 - label.get_height() / 2))


def draw_grid(surface, grid):  # draws 20 vertical line and 10 horizontal forming a grid.
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):  # amount of rows we have.
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):  # amount of columns in a row.
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):
    # if we remove a row, increment increases by 1
    increment = 0
    # loops through the grid backwards to not override existing rows in the dictionary.
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        # If there are no black squares in a row, it means it is full so clear.
        if (0, 0, 0) not in row:
            increment += 1  # checks how many rows where removed.
            ind = i
            for j in range(len(row)):  # gets every position in the full row.
                try:
                    del locked[(j, i)]  # delete locked positions from dictionary.
                except:
                    continue
    if increment > 0:  # sorts the locked pos list based on Y value.
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key  # Gets every key in locked pos.
            if y < ind:  # Checks if the y value is above the index that was removed. only moves down the above rows.
                updated_key = (x, y + increment)  # Gets the new key and ads increment to move it down.
                locked[updated_key] = locked.pop(key)  # moves the updated key to locked pos dictionary with same color.

    return increment  # Returns the amount of deleted rows.


def next_shape(shape, surface):
    # text font and color.
    font = pygame.font.SysFont('Viking', 80)
    label = font.render('Next', 1, (160, 32, 240))

    # position in screen.
    sx = top_left_x + play_width - 500
    sy = top_left_y + play_height - 500
    formatting = shape.shape[shape.rotation % len(shape.shape)]

    # draws the static image of the next shape
    for i, line in enumerate(formatting):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':  # takes the upcoming shape based on its initial position and copies it.
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    # draws the 'next' on the screen
    surface.blit(label, (sx + 10, sy - 80))


def high_score(newscore):
    score = highest_score()
    # replaces score if higher tha high score.
    with open('HighScores.txt', 'w') as f:
        if int(score) > newscore:
            f.write(str(score))
        else:
            f.write(str(newscore))


def highest_score(): #display the high score
    with open('HighScores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score=0, last_score = 0):
    surface.fill((64, 64, 64))

    pygame.font.init()
    font = pygame.font.SysFont('Viking', 70)
    label = font.render('PyTris', 1, (0, 255, 0))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score display
    font = pygame.font.SysFont('Viking', 30)
    label = font.render('High score: ' + str(score), 1, (255, 255, 255))

    # position in screen
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 30, sy + 100))
    # high score
    label = font.render('Score:' + str(last_score) , 1, (255, 255, 255))

    sx = top_left_x - 200
    sy = top_left_y + 150

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)


def main(win):
    last_score = highest_score()
    # Creates a grid with locked pos
    locked_positions = {}
    grid = create_grid(locked_positions)

    # Variables to start game
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.30
    difficulty_time = 0
    score = 0
    # game loop
    while run:
        grid = create_grid(locked_positions)  # constantly updates grid with new locked positions.
        fall_time += clock.get_rawtime()  # gets the amount of time since the last clock tick. runs the same in all PC.
        difficulty_time += clock.get_rawtime()
        clock.tick()
        # increases difficulty
        if difficulty_time / 1000 > 5:
            difficulty_time = 0
            if difficulty_time > fall_speed:
                difficulty_time -= fall_speed
        # makes piece fall
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            # Event listener fo key pressing,checks if valid place.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)  # checks the positions while the piece is falling.

        for i in range(len(shape_pos)):  # adds color to the grid
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:  # updates locked positions dictionary with color and position.
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()  # changes current piece to the next one.
            change_piece = False  # gets a new random shape.
            score += clear_rows(grid, locked_positions) * 5  # increases score.

        draw_window(win, grid, last_score, score)
        next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):  # if you loose break while loop.
            draw_menu_text(win, "GAME OVER", 180, (255, 0, 0))  # displays loosing text.
            pygame.display.update()
            pygame.time.delay(3000)
            run = False  # Brings you back to main menu.
            high_score(score)


def main_menu(win):  # Game menu
    run = True
    while run:
        win.fill((64, 64, 64))
        draw_menu_text(win, 'PRESS ANY KEY TO PLAY', 80, (0, 255, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:  # Whenever you press a key, game starts (you call main)
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('PyTris')
main_menu(win)
