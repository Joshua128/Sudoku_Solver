import copy
from collections import defaultdict
import sys
import os
from keras.models import load_model
from board_extract import get_board
import numpy as np


flag = [False]
def puzzle_solver(board, pos):
    col = pos % 9
    row = (int)(pos / 9)
    
    #end of board just return
    if(row == 9 and col ==0):
        
        print("YEEYEEYEY")
        flag[0] = True
        write_board_to_file(board)
        print(board)
        return
    if(row >= len(board) or col >= len(board[0])):
        return
    if(row < 0 or col < 0):
        return 
    if(board[row][col] > 0):
        puzzle_solver(board,pos+1)
        return
    for i in range(1,10):
        board[row][col] = i

        box_col = col//3 
        box_row = row - (row % 3)
        box_area = box_row + box_col
        print(box_area)
        area_boxes[box_area][i] +=1 
        if(checkRow(board[row]) == False or checkCol(board,col) == False or check_area(box_area) == False):
            board[row][col] = 0
            area_boxes[box_area][i] -=1 
            continue
        puzzle_solver(board, pos+1)
        if(flag[0]):
            break
        board[row][col] = 0
        area_boxes[box_area][i] -=1 
    #if you are on a immutable square  move on 



def checkRow(arr):
    num = set()
    for i in range(9):
        if arr[i] != 0:
            if arr[i] in num:
                return False
            num.add(arr[i])

    return True
    
def checkCol(arr,col):
    col_arr = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        col_arr[i] = arr[i][col]
    num = set()
    for i in range(9):
        if col_arr[i] != 0:
            if col_arr[i] in num:
                return False
            num.add(col_arr[i])

    return True

def check_area(box_index):
    for i in range(1,10):
        if(area_boxes[box_index][i]  == 2):
            return False
    return True

#writes the final board to file 
def write_board_to_file(board, filename="output.txt"):
    with open(filename, "w") as f:
        for row in board:
            row_str = " ".join(str(num) for num in row)
            f.write(row_str + "\n")



area_boxes = [defaultdict(int) for i in range(9)]



#sample board

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

new_board = get_board()
new_board = new_board.tolist()
print(new_board)

for i in range(9):
    for j in range(9):
        if new_board[i][j] > 0:
            print("DUsudhuhssHduhdushhdusds")
            board_row = i - (i % 3)
            board_col = j // 3
            board_index = board_row + board_col
            area_boxes[board_index][new_board[i][j]] +=1



puzzle_solver(new_board,0)
