import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (138, 43, 226)
ORANGE = (255, 127, 80)

height = 3000
width = 3000
size = 2000 / 5
red_turn = True  # defines that red starts first
listOfCenter = []
red_student = ['r', 's']
red_master = ["r", "m"]
blue_student = ['b', 's']
blue_master = ["b", "m"]
empty_square = ["", ""]
square_pos = []

# load pictures for cards
boar = pygame.image.load("boar.jpg")
crab = pygame.image.load("crab.jpg")
horse = pygame.image.load("horse.jpg")
ox = pygame.image.load("ox.jpg")
tiger = pygame.image.load("tiger.jpg")

# create window
window = pygame.display.set_mode((height, width))
pygame.display.set_caption("Onitama")

# create surface that is all white and smaller than window
board = pygame.Surface((height - 1000, width - 1000))
board.fill((255, 255, 255))

# board that has all the positions and what should be displayed in each
current_board = [red_student, red_student, red_master, red_student, red_student,
                 empty_square, empty_square, empty_square, empty_square, empty_square,
                 empty_square, empty_square, empty_square, empty_square, empty_square,
                 empty_square, empty_square, empty_square, empty_square, empty_square,
                 blue_student, blue_student, blue_master, blue_student, blue_student]


# create list of range of x's and range of y's for each square in from of list so total list contains lists which have two tuples (one is x one is y)
for num in range(0, 5):
    for j in range(1, 6):
        square_pos.append([((j - 1) * size, j * size), (num * size, (num + 1) * size)])

card_pos = [[(2000, 2715), (0, size)], [(2000, 2715), (size, 2*size)], [(2000, 2715),
            (3*size, 4*size)], [(2000, 2715), (4*size, 5*size)]]


def boar_move(square):  # define all moves: take current square then return possible coordinates of movement
    cur_pos_x, tup_x = square_pos[square][0]
    cur_pos_y, tup_y = square_pos[square][1]
    boar_set = []
    if red_turn:
        boar_set = [[cur_pos_x - size, cur_pos_y], [cur_pos_x + size, cur_pos_y], [cur_pos_x, cur_pos_y + size]]
    elif not red_turn:
        boar_set = [[cur_pos_x + size, cur_pos_y], [cur_pos_x - size, cur_pos_y], [cur_pos_x, cur_pos_y - size]]

    return boar_set


def crab_move(square):
    cur_pos_x, tup_x = square_pos[square][0]
    cur_pos_y, tup_y = square_pos[square][1]
    crab_set = []

    if red_turn:
        crab_set = [[cur_pos_x - 2 * size, cur_pos_y], [cur_pos_x, cur_pos_y - size], [cur_pos_x + 2 * size, cur_pos_y]]
    elif not red_turn:
        crab_set = [[cur_pos_x + 2 * size, cur_pos_y], [cur_pos_x, cur_pos_y + size], [cur_pos_x - 2 * size, cur_pos_y]]

    return crab_set


def horse_move(square):
    cur_pos_x, tup_x = square_pos[square][0]
    cur_pos_y, tup_y = square_pos[square][1]
    horse_set = []

    if red_turn:
        horse_set = [[cur_pos_x - size, cur_pos_y], [cur_pos_x, cur_pos_y - size], [cur_pos_x, cur_pos_y + size]]
    elif not red_turn:
        horse_set = [[cur_pos_x + size, cur_pos_y], [cur_pos_x, cur_pos_y + size], [cur_pos_x, cur_pos_y - size]]

    return horse_set


def ox_move(square):
    cur_pos_x, tup_x = square_pos[square][0]
    cur_pos_y, tup_y = square_pos[square][1]
    ox_set = []

    if red_turn:
        ox_set = [[cur_pos_x + size, cur_pos_y], [cur_pos_x, cur_pos_y - size], [cur_pos_x, cur_pos_y + size]]
    elif not red_turn:
        ox_set = [[cur_pos_x - size, cur_pos_y], [cur_pos_x, cur_pos_y + size], [cur_pos_x, cur_pos_y - size]]

    return ox_set


def tiger_move(square):
    cur_pos_x, tup_x = square_pos[square][0]
    cur_pos_y, tup_y = square_pos[square][1]
    tiger_set = []

    if red_turn:
        tiger_set = [[cur_pos_x, cur_pos_y - size], [cur_pos_x, cur_pos_y + 2 * size]]
    elif not red_turn:
        tiger_set = [[cur_pos_x, cur_pos_y + size], [cur_pos_x, cur_pos_y - 2 * size]]
    return tiger_set


card_order = [ox, tiger, boar, crab, horse]


def update_board():
    update_controller = 0
    half_size = size / 2
    quarter_size = size / 4
    center_y = 0
    center_x = 0
    board.fill(BLACK)
    # create alternating white/black chess board pattern for 5x5 grid
    for x in range(0, 5, 1):
        for y in range(0, 5, 1):
            if update_controller % 2 == 0:
                rect_1 = pygame.draw.rect(board, BLACK, (x * size, y * size, size, size))
                center = rect_1.center
                listOfCenter.append(center)
            else:
                pygame.draw.rect(board, WHITE, (x * size, y * size, size, size))
            update_controller += 1

    pygame.draw.rect(board, (238, 232, 170), (2 * size, 0, size, size))
    pygame.draw.rect(board, (238, 232, 170), (2 * size, 4 * size, size, size))

    # place pieces on board based on list of where pieces are make sure they are centered in their square
    for i in range(0, len(current_board)):
        if i % 5 == 0 and i != 0:
            center_y += 1

        if current_board[i][0] == "r" and current_board[i][1] == "s":
            pygame.draw.circle(board, (255, 0, 0), ((half_size + size * center_x), half_size + size * center_y),
                               quarter_size)
        elif current_board[i][0] == "r" and current_board[i][1] == "m":
            pygame.draw.rect(board, (255, 0, 0), (center_x * size + quarter_size, quarter_size + size * center_y,
                                                  half_size, half_size))
        elif current_board[i][0] == "b" and current_board[i][1] == "s":
            pygame.draw.circle(board, (0, 0, 255), ((half_size + size * center_x), half_size + size * center_y),
                               quarter_size)
        elif current_board[i][0] == "b" and current_board[i][1] == "m":
            pygame.draw.rect(board, (0, 0, 255), (center_x * size + quarter_size, quarter_size + size * center_y,
                                                  half_size, half_size))

        center_x += 1
        if center_x == 5:
            center_x = 0

    # colors cards depending on which team can use them
    for m in range(0, 5):
        card_order_copy = card_order.copy()
        if m < 2:
            card_order_copy[m] = pygame.transform.rotate(card_order_copy[m], 180)
        # if m > 2:
        if m != 2:
            window.blit(card_order_copy[m], (5 * size, m * size))
        if m == 2:
            window.blit(card_order_copy[m], (5.5 * size, m * size))


def main():
    update_board()
    while True:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                x, y = pos

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pos = pygame.mouse.get_pos()
                x, y = pos

        window.blit(board, board.get_rect())
        pygame.display.update()


main()
