import threading
import time

from tkinter import *

global terminal_state, walls, width, x_cord, y_cord, player


def create_board():
    for x in range(x_cord):
        for y in range(y_cord):
            board.create_rectangle(x*width, y*height, (x+1)*width, (y+1)*height, fill="white", width=1)
            temp = {}
            cell_scores[(x, y)] = temp


def create_terminal_state():
    for (x, y, color, w) in terminal_state:
        board.create_rectangle(x*width, y*height, (x+1)*width, (y+1)*height, fill=color, width=1)


def create_boundaries():
    for (x, y) in walls:
        board.create_rectangle(x*width, y*height, (x+1)*width, (y+1)*height, fill="black", width=1)


def try_move(dx, dy):
    global player, x_cord, y_cord, score, walk_reward, me, restart
    if restart is 1:
        rerun_main()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x_cord) and (new_y >= 0) and (new_y < y_cord) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*width+width*.2, new_y*height+height*.2, new_x*width+width*.8, new_y*height+height*.8)
        player = (new_x, new_y)
    for (x, y, color, w) in terminal_state:
        if new_x == x and new_y == y:
            score -= walk_reward
            score += w
            if score > 0:
                print("Success!\t", score)
            else:
                print("Fail!\t", score)
            restart = 1
            return


def rerun_main():
    global player, score, me, restart
    player = (10, y_cord-1)
    score = 1
    restart = 0
    board.coords(me, player[0]*width+width*.2, player[1]*height+height*.2,
                     player[0]*width+width*.8, player[1]*height+height*.8)


def has_restarted():
    return restart


def poss_move(position):
    s = player
    r = -score
    if position == moves_list[0]:
        try_move(0, -1)
    elif position == moves_list[1]:
        try_move(0, 1)
    elif position == moves_list[2]:
        try_move(-1, 0)
    elif position == moves_list[3]:
        try_move(1, 0)
    else:
        return
    state_two = player
    r += score
    return s, position, r, state_two


def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc


def run():
    global gamma
    time.sleep(1)
    alpha = 1
    t = 1

    while True:
        s = player
        max_act, max_val = max_Q(s)
        (s, a, r, state_two) = poss_move(max_act)

        max_act, max_val = max_Q(state_two)
        inc_Q(s, a, alpha, r + gamma * max_val)

        t += 1.0
        if has_restarted():
            rerun_main()
            time.sleep(0.01)
            t = 1.0

        alpha = pow(t, -0.01)

        time.sleep(0.001)


def run_main():
    frame.mainloop()


frame = Tk()

min_points = -0.8
max_points = 0.8
walk_reward = -0.04

width = 25
height = 25

(x_cord, y_cord) = (11, 11)
moves_list = ['up', 'down', 'left', 'right']

board = Canvas(frame, width=width*x_cord, height=height*y_cord)
player = (10, y_cord-5)
score = 1
restart = 0


walls = [                                                        (0, 7),
                 (1, 1), (1, 2), (1, 3), (1, 4),         (1, 6), (1, 7), (1, 8), (1, 9),
                 (2, 1),
                 (3, 1),         (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
                 (4, 1),                                                 (4, 8),
         (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6),         (5, 8),        (5, 10),
                 (6, 1),                 (6, 4),
                 (7, 1), (7, 2),         (7, 4),         (7, 6), (7, 7),        (7, 9),
                                                                 (8, 7),        (8, 9), (8, 10),
                 (9, 1),         (9, 3),         (9, 5),         (9, 7),        (9, 9),
                 (10, 1),                                        (10, 7)]

terminal_state = [(4, 0, "green", 1)]

cell_scores = {}
create_board()
create_terminal_state()

me = board.create_rectangle(player[0]*width+width*.2, player[1]*height+height*.2,
                            player[0]*width+width*.8, player[1]*height+height*.8,
                            fill="yellow", width=1, tag="me")

frame.bind("<Up>", try_move(0, -1))
frame.bind("<Down>", try_move(0, 1))
frame.bind("<Left>", try_move(-1, 0))
frame.bind("<Right>", try_move(1, 0))

board.grid(row=0, column=0)

gamma = 0.3
moves_list = moves_list
states = []
Q = {}

for x in range(x_cord):
    for j in range(y_cord):
        states.append((x, j))

for state in states:
    temp = {}
    for position in moves_list:
        temp[position] = 0.1
    Q[state] = temp

for (x, y, color, w) in terminal_state:
    for position in moves_list:
        Q[(x, y)][position] = w

t = threading.Thread(target=run)
t.daemon = True
t.start()
run_main()
