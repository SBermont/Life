import time
import os
import random
from pynput.keyboard import Listener, Key
from threading import Thread


def paint(game_board):
    global n
    print("╔" + '═' * 2*n + "╗")
    for row in game_board:
        one_line = ''
        for elem in row:
            if elem[0]:
                one_line += u"\u2593"*2
            else:
                one_line += '  '
        print("║" + one_line + "║")
    print("╚" + '═' * 2*n + "╝")


def check_neighbors(board, row, column, m, n):
    rows_limits = {0: (0, 2), m-1: (m-2, m)}
    cols_limits = {0: (0, 2), n-1: (n-2, n)}
    if row not in rows_limits:
        rows_limits[row] = (row-1, row+2)
    if column not in cols_limits:
        cols_limits[column] = (column-1, column+2)
    (min_r, max_r) = rows_limits[row]
    (min_c, max_c) = cols_limits[column]

    for i in range(min_r, max_r):
        for j in range(min_c, max_c):
            if i != row or j != column:
                if board[i][j][0]:
                    board[row][column][1] += 1


def przeglad_stanu_planszy(game_board, m, n):
    for wiersz in range(m):
        for kolumna in range(n):
            check_neighbors(game_board, wiersz, kolumna, m, n)


def decide_who_is_alive(game):
    for i in range(len(game)):
        for j in range(len(game[0])):
            if game[i][j][0]: # jeżeli jest żywa:
                if game[i][j][1] not in (2, 3):
                    game[i][j][0] = False
            else:
                if game[i][j][1] == 3:
                    game[i][j][0] = True

            game[i][j][1] = 0


def on_press(key):
    global wyjscie
    wyjscie = key


# rozmiar

m = int(input("Ile wierszy? "))
n = int(input("Ile kolumn? "))
gameboard = [[[False, 0] for i in range(n)] for i in range(m)]
#wygeneruj poczatkowe


# ile maksymalnie zywych z m*n
a = int(input("ile maksymalnie zywych z " + str(m*n) + " komórek? "))

for _ in range(a):
    gameboard[random.randint(0, m-1)][random.randint(0, n-1)][0] = True

wyjscie = None

while True:
    os.system("cls")
    paint(gameboard)

    with Listener(on_press=on_press) as ls:
        def time_out(period_sec: int):
            time.sleep(period_sec)  # Listen to keyboard for period_sec seconds
            ls.stop()


        Thread(target=time_out, args=(1,)).start()
        ls.join()
    if wyjscie == Key.esc:
        break

    przeglad_stanu_planszy(gameboard, m, n)
    decide_who_is_alive(gameboard)


input('The end!')