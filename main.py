import pygame
import sys

from pygame.event import post

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (238, 232, 170)
PURPLE = (138, 43, 226)
ORANGE = (255, 127, 80)

height = 3000
width = 3000
size = 2000 / 5
current_click = 0
current_card = -1
current_piece = 0
red_turn = True  # defines that red starts first
listOfCenter = []
red_student = ['r', 's']
red_master = ["r", "m"]
blue_student = ['b', 's']
blue_master = ["b", "m"]
empty_square = ["", ""]
square_pos = []
square_color = []

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

square_color = [BLACK, WHITE, YELLOW, WHITE, BLACK,
                WHITE, BLACK, WHITE, BLACK, WHITE,
                BLACK, WHITE, BLACK, WHITE, BLACK,
                WHITE, BLACK, WHITE, BLACK, WHITE,
                BLACK, WHITE, YELLOW, WHITE, BLACK,]


# create list of range of x's and range of y's for each square in from of list so total list contains lists which have two tuples (one is x one is y)
for num in range(0, 5):
    for j in range(1, 6):
        square_pos.append([((j - 1) * size, j * size), (num * size, (num + 1) * size)])

card_pos = [[(2000, 2715), (0, size)], [(2000, 2715), (size, 2*size)], [(2000, 2715),
            (3*size, 4*size)], [(2000, 2715), (4*size, 5*size)]]



card_order = [ox, tiger, boar, crab, horse]

def movement(left, right, up, down, square):
    global red_turn
    move_set = []

    if not red_turn:
        left = -1 * left
        right = -1* right
        up = -1 * up
        down = -1 * down
    if square != 0 and square != 5 and square != 10 and square != 15 and square != 20:
        move_set.append(square - left)

    if square != 4 and square != 9 and square != 14 and square != 19 and square != 24:
        move_set.append(square + right)
    move_set.append(square + up)
    move_set.append(square - down)
    return move_set

# TODO figure out how to deal with squares on the sides 
def possible_moves(begin):  # create list of what moves can be done based on what cards are available to red or blue
    global current_card
    pos_move_set = []
    full_move_set = []

    
    #  depending what the current card order is add moves to set of what player can do
    if card_order[current_card] == ox:
        pos_move_set.append(movement(1, 0, 5, 5, begin))
    elif card_order[current_card] == tiger:
        pos_move_set.append(movement(0, 0, 10, 5, begin))
    elif card_order[current_card] == boar:
        pos_move_set.append(movement(1, 1, 5, 0, begin)) 
    elif card_order[current_card] == crab:
        pos_move_set.append(movement(2, 2, 5, 0, begin))
    elif card_order[current_card] == horse:
        pos_move_set.append(movement(0, 1, 5, 5, begin))
    pos_move_set.append(None)

    pos_move_set = list(filter(None, pos_move_set))
    for b in range(0, len(pos_move_set)):
        for c in range(0, len(pos_move_set[b])):
            full_move_set.append(pos_move_set[b][c])
    # determines if a possible move will be onto a piece of the same color and removes that move
    for d in range(0, len(full_move_set)):
        if full_move_set[d] < 0:
            full_move_set[d] = None
        elif full_move_set[d] > 24:
            full_move_set[d] = None
        elif red_turn:
            if current_board[full_move_set[d]] == red_master or current_board[full_move_set[d]] == red_student:
                full_move_set[d] = None
        elif not red_turn:
            if current_board[full_move_set[d]] == blue_master or current_board[full_move_set[d]] == blue_student:
                full_move_set[d] = None
    
    full_move_set = list(filter(None, full_move_set))  # remove all the Nones
    return full_move_set


def update_board(color_order):
    update_controller = 0
    half_size = size / 2
    quarter_size = size / 4
    center_y = 0
    center_x = 0
    board.fill(BLACK)
    # create alternating white/black chess board pattern for 5x5 grid
    for y in range(0, 5, 1):
        for x in range(0, 5, 1):
            rect_1 = pygame.draw.rect(board, color_order[update_controller], (x * size, y * size, size, size))
            center = rect_1.center
            listOfCenter.append(center)
            update_controller += 1

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

    # flips cards depending on which team can use them
    for m in range(0, 5):
        card_order_copy = card_order.copy()
        if m < 2:
            card_order_copy[m] = pygame.transform.rotate(card_order_copy[m], 180)
        # if m > 2:
        if m != 2:
            window.blit(card_order_copy[m], (5 * size, m * size))
        if m == 2:
            window.blit(card_order_copy[m], (5.5 * size, m * size))


def move_piece(begin, finish, used):
    global current_board
    global red_turn
    global card_order
    global square_color

    current_board[finish] = current_board[begin]
    current_board[begin] = empty_square
    
    card_order_copy = card_order.copy()
    card_order[used] = card_order[2]
    card_order[2] = card_order_copy[used]


    red_turn = not red_turn
    update_board(square_color)


def check_piece_there(there):
    global start
    global origin
    global current_click

    if red_turn and current_click == 2:
        if current_board[there] == red_student or current_board[there] == red_master:
            current_click = 1
            
    elif not red_turn and current_click == 2:
         if current_board[there] == blue_student or current_board[there] == blue_master:
            current_click = 1

    if current_click < 2:
        if red_turn:
            if current_board[there] == empty_square:
                return False
            elif current_board[there] == red_student or current_board[there] == blue_student:
                return True
        if not red_turn:
            if current_board[there] == empty_square:
                return False
            elif current_board[there] == blue_student or current_board[there] == blue_master:
                return True
       
    elif current_click == 2:
        if red_turn:
            if current_board[there] == empty_square:
                return True
            elif current_board[there] == blue_student:
                return True
            elif current_board[there] == blue_master:
                win = "Red"
                win_game(win)
                return True
        if not red_turn:
            if current_board[there] == empty_square:
                return True
            elif current_board[there] == red_student:
                return True
            elif current_board[there] ==red_master:
                win = "Blue"
                win_game(win)
                return True


def check_mouse_pos(cur_x, cur_y, what_click):
    global current_click
    global current_card
    global square_color
    global current_piece
    highlight = []
    new_board = square_color.copy()
    # determines if the click was on one of the cards

    for k in range(0, len(card_pos)):
        c_low_range_x, c_high_range_x = card_pos[k][0]
        c_low_range_y, c_high_range_y = card_pos[k][1]
        if c_low_range_x <= cur_x <= c_high_range_x and c_low_range_y <= cur_y <= c_high_range_y:
            if red_turn and k < 2:
                current_click = 1
                current_card = k
                return k
            if not red_turn and k > 1:
                current_click = 1 
                current_card = k + 1
                return k

    # determines if the click was on one of the squares
    if current_click >= 1: 
        for i in range(0, len(square_pos)):
            low_range_x, high_range_x = square_pos[i][0]
            low_range_y, high_range_y = square_pos[i][1]

            if low_range_x <= cur_x <= high_range_x:
                if low_range_y <= cur_y <= high_range_y:
                    
                    highlight = possible_moves(i)
                    if current_click == 1:
                        print(check_piece_there(i))
                        # if the click was on one of the squares and a card has been selected determine what piece is there
                        if check_piece_there(i):
                            highlight = possible_moves(i)
                            print("HI")
                            for j in range(0, len(highlight)):
                                if current_card == 0 or current_card == 3:
                                    print(highlight)
                                    new_board[highlight[j]] = ORANGE
                                elif current_card == 1 or current_card == 4:
                                    new_board[highlight[j]] = PURPLE
                            current_piece = i
                            update_board(new_board)

                        current_click = 2
                        return i
                    elif current_click == 2:
                        if check_piece_there(i):
                            for p in range(0, len(highlight)):
                                if highlight[p] == i:
                                    move_piece(current_piece, highlight[p], current_card)
                                    current_click = 0
    


def win_game(winner):
    print(winner + " won!")


def main():
    global square_color
    update_board(square_color)
    while True:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                x, y = pos
                check_mouse_pos(x, y, 1)

            """ elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pos = pygame.mouse.get_pos()
                x, y = pos
                check_mouse_pos(x, y, 3) """

        window.blit(board, board.get_rect())
        pygame.display.update()

main()
