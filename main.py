from tkinter import *
import tkinter as tk

import numpy as np

window = Tk()

GRID_WIDTH = 10
GRID_HEIGHT = 5

SQUARE_SIZE = 2

DIGITS = 9

score_frame = Frame(master=window, relief=tk.RIDGE)
score_frame.pack()
score_label = tk.Label(
    master=score_frame,
    width=GRID_WIDTH * SQUARE_SIZE,
    height=int(SQUARE_SIZE / 2),
    text=f"Digits: {DIGITS}"
)

score_label.pack()

grid_frame = Frame(
    master=window,
    width=GRID_WIDTH * SQUARE_SIZE,
    height=GRID_HEIGHT * SQUARE_SIZE
)

grid_frame.columnconfigure("all", weight=1)
grid_frame.rowconfigure("all", weight=1)

grid_frame.pack()

numbers_pressed = []

buttons = {}


# event functions

def button_onclick(event):
    widget = event.widget
    # number_pressed = int(widget.cget('text'))

    # https://stackoverflow.com/a/13149770
    number_pressed = int(list(buttons.keys())[list(buttons.values()).index(widget)])
    numbers_pressed.append(number_pressed)
    if verify_numbers_pressed(numbers_pressed):
        print("good job")
        if number_pressed == 1:
            # https://stackoverflow.com/a/3294899
            for i, button in buttons.items():
                button.config(text="")
        elif number_pressed == DIGITS:
            quit(0)
    else:
        # reset
        print("bad job")
        quit(0)
    print(f"number pressed: {number_pressed}")


# game functions

def get_random_indexes(no_of_indexes, minimum, maximum):
    to_return = np.random.randint(minimum, maximum, no_of_indexes)
    unique = np.unique(to_return, return_counts=True)
    print(f"to_return: {to_return}")
    print(f"unique: {unique}")
    print(f"unique[1]: {unique[1]}")
    print(f"all(n == 1 for n in unique[1]): {all(n == 1 for n in unique[1])}")
    if not all(n == 1 for n in unique[1]):
        return get_random_indexes(no_of_indexes, minimum, maximum)
    else:
        return to_return


def verify_numbers_pressed(arr):
    if len(arr) == 0:
        return True
    else:
        if arr[0] != 1:
            return False
        elif len(arr) > 1:
            # checks if the numbers pressed are "correct"
            # by checking if the last element is 1 higher than the second to last element

            # this only works because the game resets when this returns false,
            # so we don't need to loop, also making this O(1) hehe
            last = arr[len(arr) - 1]
            before_last = arr[len(arr) - 2]
            return last - before_last == 1
        elif arr[0] == 1:
            return True


indexes = get_random_indexes(DIGITS, 0, (GRID_WIDTH * GRID_HEIGHT) - 1)
print(indexes)

curr_num = 1
for i in range(0, GRID_WIDTH):
    for j in range(0, GRID_HEIGHT):
        index = (i * GRID_HEIGHT) + j
        if index in indexes:
            button_index = list(indexes).index(index) + 1
            button = Button(
                master=grid_frame,
                width=GRID_WIDTH,
                height=GRID_HEIGHT,
                text=f"{button_index}",
                cursor="hand2"
            )
            buttons[button_index] = button
            button.grid(row=j, column=i, sticky="ew")
            button.bind("<Button-1>", button_onclick)

window.mainloop()
