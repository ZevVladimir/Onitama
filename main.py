import pygame
from tkinter import *
from tkinter import Toplevel, messagebox
from tkinter import ttk
import random
import sys

win = Tk()
def open_popup(winner):
    win.geometry("1500x250")
    win.title("Game Over!")
    Label(win, text = winner, font=('Mistral 18 bold')).place(x = 150, y = 80)
    win.mainloop()

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
blue_turn = True  # defines that blue starts first
listOfCenter = []
red_student = ['r', 's']
red_master = ["r", "m"]
blue_student = ['b', 's']
blue_master = ["b", "m"]
empty_square = ["", ""]
square_pos = []
square_color = []
highlight = []
card_order = []

# load pictures for cards
tiger = pygame.image.load("tiger.jpg")
frog = pygame.image.load("frog.jpg")
rabbit = pygame.image.load("rabbit.jpg")
crab = pygame.image.load("crab.jpg")
elephant = pygame.image.load("elephant.jpg")
goose = pygame.image.load("goose.jpg")
rooster = pygame.image.load("rooster.jpg")
monkey = pygame.image.load("monkey.jpg")
mantis = pygame.image.load("mantis.jpg")
horse = pygame.image.load("horse.jpg")
ox = pygame.image.load("ox.jpg")
crane = pygame.image.load("crane.jpg")
boar = pygame.image.load("boar.jpg")
eel = pygame.image.load("eel.jpg")
cobra = pygame.image.load("cobra.jpg")

all_cards = [tiger, frog, rabbit, crab, elephant, goose, rooster, monkey, mantis, horse, ox, crane, boar, eel, cobra]

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

# Randomize what cards are chosen for each game
all_cards_copy = all_cards.copy()
for p in range(0, 5):
    
    add = random.randint(0, len(all_cards_copy) - 1)
    card_order.append(all_cards_copy[add])
    all_cards_copy.pop(add)


def distance_to_edge(current):
    test = current
    distance_left = 0
    distance_right = 0
    distance_up = 0
    distance_down = 0
    distance_uldiag = 0
    distance_drdiag = 0
    distance_urdiag = 0
    distance_dldiag = 0

    distances = []

    for a in range(0, 4):  
        if test % 5 == 0:
            break
        test -= 1
        distance_left += 1
    test = current

    for b in range(0, 4):
        if (test + 1) % 5 == 0:
            break
        test += 1
        distance_right += 1
    test = current
    
    for c in range(0, 4):
        if test < 0:
            break
        test -= 5
        distance_up += 1
    test = current
    
    for d in range(0, 4):
        if test > 24:
            break
        test += 5
        distance_down += 1
    test = current

    for e in range(0,4):
        if (test - 6) < 0 or test == 10 or test == 15 or test == 20:
            print("here" + str(distance_uldiag))
            break
        test -= 6
        distance_uldiag += 1
    test = current
    
    for f in range(0, 4):
        if (test + 6) > 24 or test == 4 or test == 9 or test == 14:
            break
        test += 6
        distance_drdiag += 1
    test = current

    for g in range(0,4):
        if (test - 4) < 1 or test == 9 or test == 14 or test == 19 or test == 24:
            break
        test -= 4
        distance_urdiag += 1
    test = current

    for h in range(0,4):
        if test + 4 > 23 or test == 0 or test == 5 or test == 10 or test == 15:
            break
        test += 4
        distance_dldiag += 1
    
    distances.append(distance_left)
    distances.append(distance_right)
    distances.append(distance_up)
    distances.append(distance_down)
    distances.append(distance_uldiag)
    distances.append(distance_drdiag)
    distances.append(distance_urdiag)
    distances.append(distance_dldiag)
    # diagonals are swtiched when board is upside down
    if not blue_turn:
        distances_copy = distances.copy()
        distances[0] = distances[1]
        distances[1] = distances_copy[0]
        distances[4] = distances[5]
        distances[5] = distances_copy[4]
        distances[6] = distances[7]
        distances[7] = distances_copy[6]
    return distances


def movement(left, right, up, down, uldiag, drdiag, urdiag, dldiag, square):
    global blue_turn
    move_set = []
    limit_to_move = distance_to_edge(square)

    if not blue_turn:
        up = -1 * up
        down = -1 * down
        right = -1 * right
        left = -1 * left
        uldiag = -1 * uldiag
        drdiag = -1 * drdiag
        urdiag = -1 * urdiag
        dldiag = -1 * dldiag
    
    print(limit_to_move)
    print("left: " + str(left))
    print("right: " + str(right))
    print("up: " + str(up))
    print("down: " + str(down))
    print("uldiag: " + str(uldiag))
    print("drdiag: " + str(drdiag))
    print("urdiag: " + str(urdiag))
    print("dldiag: " + str(dldiag)) 
    move_set.append(square - left)
    if abs(left) == 1 and limit_to_move[0] <= 0:
        move_set[0] = None
    elif abs(left) == 2 and limit_to_move[0] <= 1:
        move_set[0] = None

    move_set.append(square + right)
    if abs(right) == 1 and limit_to_move[1] <= 0:
        move_set[1] = None
    elif abs(right) == 2 and limit_to_move[1] <= 1:
        move_set[1] = None

    move_set.append(square - (up * 5))

    move_set.append(square + (down * 5))

    move_set.append(square - (uldiag * 6))
    if limit_to_move[4] < 1:
        move_set[4] = None
    move_set.append(square + (drdiag * 6))
    if limit_to_move[5] < 1:
        move_set[5] = None
    move_set.append(square - (urdiag * 4))
    if limit_to_move[6] < 1:
        move_set[6] = None
    move_set.append(square + (dldiag * 4))
    if limit_to_move[7] < 1:
        move_set[7] = None
    print(move_set)
    move_set = list(filter(None, move_set)) 
    return move_set

# TODO figure out how to deal with squares on the sides 
def possible_moves(begin):  # create list of what moves can be done based on what cards are available to red or blue
    global current_card
    pos_move_set = []
    full_move_set = []

    
    #  depending what the current card order is add moves to set of what player can do
    # order goes: left, right, up, down, up left diag, down right diag, up right diag, down left diag
    if card_order[current_card] == tiger:
        pos_move_set.append(movement(0, 0, 2, 1, 0, 0, 0, 0, begin))
    elif card_order[current_card] == frog:
        pos_move_set.append(movement(2, 0, 0, 0, 1, 1, 0, 0, begin))
    elif card_order[current_card] == rabbit:
        pos_move_set.append(movement(0, 2, 0, 0, 0, 0, 1, 1, begin))
    elif card_order[current_card] == crab:
        pos_move_set.append(movement(2, 2, 1, 0, 0, 0, 0, 0, begin))
    elif card_order[current_card] == elephant:
        pos_move_set.append(movement(1, 1, 0, 0, 1, 0, 1, 0, begin))
    elif card_order[current_card] == goose:
        pos_move_set.append(movement(1, 1, 0, 0, 1, 1, 0, 0, begin))
    elif card_order[current_card] == rooster:
        pos_move_set.append(movement(1, 1, 0, 0, 0, 0, 1, 1, begin))
    elif card_order[current_card] == monkey:
        pos_move_set.append(movement(0, 0, 0, 0, 1, 1, 1, 1, begin))
    elif card_order[current_card] == mantis:
        pos_move_set.append(movement(0, 0, 0, 1, 1, 0, 1, 0, begin))
    elif card_order[current_card] == horse:
        pos_move_set.append(movement(1, 0, 1, 1, 0, 0, 0, 0, begin))
    elif card_order[current_card] == ox:
        pos_move_set.append(movement(0, 1, 1, 1, 0, 0, 0, 0, begin))
    elif card_order[current_card] == crane:
        pos_move_set.append(movement(0, 0, 1, 0, 0, 1, 0, 1, begin))
    elif card_order[current_card] == boar:
        pos_move_set.append(movement(1, 1, 1, 0, 0, 0, 0, 0, begin))
    elif card_order[current_card] == eel:
        pos_move_set.append(movement(0, 1, 0, 0, 1, 0, 0, 1, begin))
    elif card_order[current_card] == cobra:
        pos_move_set.append(movement(1, 0, 0, 0, 0, 1, 1, 0, begin))
    
    
    
    # pos_move_set.append(None)

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
        elif blue_turn:
            if current_board[full_move_set[d]] == blue_master or current_board[full_move_set[d]] == blue_student:
                full_move_set[d] = None
        elif not blue_turn:
            if current_board[full_move_set[d]] == red_master or current_board[full_move_set[d]] == red_student:
                full_move_set[d] = None
    
    full_move_set = list(filter(None, full_move_set))  # remove all the Nones
    return full_move_set


def update_board(color_order):
    global current_card
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
    global blue_turn
    global card_order
    global square_color
    winner = ""
    
    current_board_copy = current_board.copy()
    current_board[finish] = current_board[begin]
    current_board[begin] = empty_square
    
    if blue_turn:
        if current_board[2] == blue_master or current_board[2] == blue_student:
            winner = "Blue won by capturing Red's dojo"
        elif current_board_copy[finish] == red_master:
            winner = "Blue won by capturing Red's master"
    elif not blue_turn:
        if current_board[22] == red_master or current_board[22] == red_student:
            winner = "Red won by capturing Blue's dojo"
        elif current_board_copy[finish] == blue_master:
            winner = "Red won by capturing Blue's master"

    card_order_copy = card_order.copy()
    card_order[used] = card_order[2]
    card_order[2] = card_order_copy[used]


    blue_turn = not blue_turn
    update_board(square_color)
    if winner != "":
        open_popup(winner)


def check_piece_there(there):
    global start
    global origin
    global current_click

    if current_click < 2:
        if blue_turn:
            if current_board[there] == empty_square:
                return False
            elif current_board[there] == red_student or current_board[there] == blue_student:
                return True
        if not blue_turn:
            if current_board[there] == empty_square:
                return False
            elif current_board[there] == blue_student or current_board[there] == blue_master:
                return True
       
    elif current_click == 2:
        if not blue_turn:
            if current_board[there] == empty_square:
                return True
            elif current_board[there] == blue_student:
                return True
            elif current_board[there] == blue_master:
                return True
            elif current_board[there] == red_student or current_board[there] == red_master:
                return False
        if blue_turn:
            if current_board[there] == empty_square:
                return True
            elif current_board[there] == red_student:
                return True
            elif current_board[there] ==red_master:
                return True
            elif current_board[there] == blue_student or current_board[there] == blue_master:
                return False


def check_mouse_pos(cur_x, cur_y, what_click):
    global current_click
    global current_card
    global square_color
    global current_piece
    global highlight
    new_board = square_color.copy()
    # determines if the click was on one of the cards

    for k in range(0, len(card_pos)):
        c_low_range_x, c_high_range_x = card_pos[k][0]
        c_low_range_y, c_high_range_y = card_pos[k][1]
        if c_low_range_x <= cur_x <= c_high_range_x and c_low_range_y <= cur_y <= c_high_range_y:
            if blue_turn and k > 1:
                current_click = 1
                current_card = k + 1
                return k
            if not blue_turn and k < 2:
                current_click = 1 
                current_card = k 
                return k

    # determines if the click was on one of the squares
    if current_click >= 1: 
        for i in range(0, len(square_pos)):
            low_range_x, high_range_x = square_pos[i][0]
            low_range_y, high_range_y = square_pos[i][1]

            if low_range_x <= cur_x <= high_range_x:
                if low_range_y <= cur_y <= high_range_y:
                    if current_click == 1:
                        highlight.clear()
                        highlight = possible_moves(i)
                        # if the click was on one of the squares and a card has been selected determine what piece is there
                        if check_piece_there(i):
                            highlight = possible_moves(i)
                            for j in range(0, len(highlight)):
                                if current_card == 0 or current_card == 3:
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
                        elif not check_piece_there(i):
                            highlight = possible_moves(i)
                            for j in range(0, len(highlight)):
                                if current_card == 0 or current_card == 3:
                                    new_board[highlight[j]] = ORANGE
                                elif current_card == 1 or current_card == 4:
                                    new_board[highlight[j]] = PURPLE
                            current_piece = i
                            update_board(new_board)


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

        window.blit(board, board.get_rect())
        pygame.display.update()

main()
