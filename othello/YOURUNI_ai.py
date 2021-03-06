#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to
complete and submit.

@author: YOUR NAME AND UNI
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache = {}

def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """
    u1, u2 = get_score(board)
    if color == 1: return u1 - u2
    if color == 2: return u2 - u1


############ MINIMAX ###############################

def minimax_min_node(board, color):
    if color == 1: oppo_color = 2
    if color == 2: oppo_color = 1
    min_move = None
    min_utility = float("inf")
    moves = get_possible_moves(board, oppo_color)
    if moves:
        for move in moves:
            next_state = play_move(board, oppo_color, move[0], move[1])
            if next_state in cache:
                utility = cache[next_state]
            else:
                utility = minimax_max_node(next_state, color)[1]
                cache[next_state] = utility
            if utility < min_utility:
                min_move = move
                min_utility = utility
        return (min_move, min_utility)
    else:
        return (None, compute_utility(board, color))


def minimax_max_node(board, color):
    max_move = None
    max_utility = - float("inf")
    moves = get_possible_moves(board, color)
    if moves:
        for move in moves:
            next_state = play_move(board, color, move[0], move[1])
            if next_state in cache:
                utility = cache[next_state]
            else:
                utility = minimax_min_node(next_state, color)[1]
                cache[next_state] = utility
            if utility > max_utility:
                max_move = move
                max_utility = utility
        return (max_move, max_utility)
    else:
        return (None, compute_utility(board, color))


def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    cache.clear()
    return minimax_max_node(board, color)[0]

############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    if color == 1: oppo_color = 2
    if color == 2: oppo_color = 1
    min_move = None
    min_utility = float("inf")
    moves = get_possible_moves(board, oppo_color)

    def _compute_util(move):
        next_state = play_move(board, oppo_color, move[0], move[1])
        return compute_utility(next_state, color)
    moves.sort(key=_compute_util)

    if moves and level <= limit:
        for move in moves:
            next_state = play_move(board, oppo_color, move[0], move[1])
            if next_state in cache:
                utility = cache[next_state]
            else:
                utility = alphabeta_max_node(next_state, color, alpha, beta, level+1, limit)[1]
                cache[next_state] = utility
            if utility < min_utility:
                min_move = move
                min_utility = utility
            if min_utility <= alpha:
                return (min_move, min_utility)
            beta = min(beta, min_utility)
        return (min_move, min_utility)
    else:
        return (None, compute_utility(board, color))


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    max_move = None
    max_utility = - float("inf")
    moves = get_possible_moves(board, color)

    def _compute_util(move):
        next_state = play_move(board, color, move[0], move[1])
        return compute_utility(next_state, color)
    moves.sort(key=_compute_util, reverse=True)

    if moves and level <= limit:
        for move in moves:
            next_state = play_move(board, color, move[0], move[1])
            if next_state in cache:
                utility = cache[next_state]
            else:
                utility = alphabeta_min_node(next_state, color, alpha, beta, level+1, limit)[1]
                cache[next_state] = utility
            if utility > max_utility:
                max_move = move
                max_utility = utility
            if max_utility >= beta:
                return (max_move, max_utility)
            alpha = max(alpha, max_utility)
        return (max_move, max_utility)
    else:
        return (None, compute_utility(board, color))


def select_move_alphabeta(board, color):
    cache.clear()
    return alphabeta_max_node(board, color, -float("inf"), float("inf"), 0, 5)[0]


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax AI") # First line is the name of this AI
    color = int(input()) # Then we read the color: 1 for dark (goes first),
                         # 2 for light.

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            # movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
