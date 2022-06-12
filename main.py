

from __future__ import print_function
from iddfs import iddfs, nr_iddfs
from random import shuffle
from board import *
from bfs import bfs
from a_star import a_star
import globals
import psutil
import time
import gc
import os


def intro():


    print('Welcome to the 15 Puzzle Program.')
    print('Directions:')


    print('USE THIS: 1 2 3 4 5 6 7 8 13 9 12 15 0 11 10 14\n')
    print('Copy paste this and hit enter')
    return input("Please enter here: ")


def check_input(user_input):


    if user_input == 'r' or user_input == 'R':
        return True

    check_against = GOAL_STATE_15_AS_SLIST
    user_input = user_input.split(" ")

    if len(user_input) != 16:
        return False
    for num in check_against:
        if num not in user_input:
            return False
    return True


def randomize_board ():


    users_board = GOAL_STATE_15_AS_SLIST
    return shuffle(users_board)


def print_board(users_board):

    board = ""
    count = 0
    for num in users_board:
        if count % EDGE_LENGTH == 0 and count != 0:
            board += '\n'
        if len(num) == 1:
            if num == '0':
                board += '   '
            else:
                board += num + '  '
        else:
            board += num + ' '
        count += 1
    print(board)


def main():


    user_input = intro()
    users_board = -999
    is_valid = check_input(user_input)
    if is_valid:
        if user_input == 'r' or user_input == 'R':
            users_board = randomize_board()
        else:
            users_board = user_input.split(' ')
        print('Successful input. Solving the board.')
        print('Your board: ')
        print_board(users_board)
    else:
        print('Incorrect input. Terminating program. Try again.')
        exit(0)

    print('Time to solve your Puzzle using DFS.\n\n')

    directions ="N","S","E","W"

    print(directions)
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss
    memory_main = memory / 1000000

    globals.memory_main = memory_main

    # bfs time
    bfs_start_time = time.time()
    bfs(users_board)
    bfs_time = time.time() - bfs_start_time
    gc.collect()

    # iddfs time
    iddfs_start_time = time.time()
    iddfs(users_board)
    iddfs_time = time.time() - iddfs_start_time
    gc.collect()

    nr_iddfs_start_time = time.time()
    nr_iddfs(users_board)
    nr_iddfs_time = time.time() - nr_iddfs_start_time
    gc.collect()

    # Manhattan Heuristic used with A*
    manhattan_astar_start_time = time.time()
    a_star(users_board, 'M')
    manhattan_astar_time = time.time() - manhattan_astar_start_time
    gc.collect()

    # Displaced Tiles Heuristic used with A*
    displaced_astar_start_time = time.time()
    a_star(users_board, 'D')
    displaced_astar_time = time.time() - displaced_astar_start_time
    gc.collect()



    print('\n------------')
    print('Result of Time Elapsed:')
    print('------------')
    print('BFS Time Elapsed: ', bfs_time * 1000, 'ms')
    print('IDDFS Time Elapsed: ', iddfs_time * 1000, 'ms')
    print('NR_IDDFS Time Elapsed: ', nr_iddfs_time * 1000, 'ms')
    print('Manhattan A* Time Elapsed: ', manhattan_astar_time * 1000, 'ms')
    print('Displaced A* Time Elapsed: ', displaced_astar_time * 1000, 'ms')
    print('------------')
    print('Results on Memory Usage:')
    print('------------')
    print("Memory used in main, just before any search:                      | ", globals.memory_main, ' MB')
    print("Memory used just before returning in bfs search:                  | ", globals.memory_bfs, ' MB')
    print("Memory used just before returning in recursive iddfs search:      | ", globals.memory_iddfs, ' MB')
    print("Memory used just before returning in Non-recursive iddfs search:  | ", globals.memory_nr_iddfs, ' MB')
    print("Memory used just before returning in BFS Manhattan A* search:     | ", globals.memory_manhattan_astar, ' MB')
    print("Memory used just before returning in BFS Displaced A* search:     | ", globals.memory_displaced_astar, ' MB')
    print('------------')


if __name__ == "__main__":
    main()
