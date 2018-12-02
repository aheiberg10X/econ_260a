import matplotlib.pyplot as plt
import numpy as np
import random as random
from math import floor 

#states
WILD = 0
DEVEL = 1
BURNT = 2

class Cell :
    def __init__(self) :
        self.state = WILD

    def update(self, neighbors) :

        pass

    def get_state(self) :
        return self.state

def get_neighbors(row, col, num_rows, num_cols) :
    possible = [(row-1, col-1),
            (row-1, col),
            (row-1, col+1),
            (row, col-1),
            (row, col+1),
            (row+1, col-1),
            (row+1, col),
            (row+1, col+1)]

    final = []
    for (r,c) in possible :
        if r < 0 or r >= num_rows or c < 0 or c >= num_cols :
            pass
        else :
            final.append((r,c))

    return final


def init_cells(num_rows, num_cols) :
    cells = [[Cell() for i in range(num_cols)] for j in range(num_rows)]
    num_rows = len(cells)
    if num_rows == 0 : 
        assert False
    num_cols = len(cells[0])

    average_density = .01
    num_devel = 0
    for row in range(num_rows) :
        row_modulator = 2 * float(row) / num_rows
        num_to_sample = int(round(num_cols * row_modulator * average_density))
        sample = random.sample(range(num_cols), num_to_sample)
        for col in sample :
            cells[row][col].state = DEVEL
        num_devel += len(sample)
    
    print "Number of cells develeoped during init: %d" % (num_devel)
    return cells

def display(cells) :
    num_rows = len(cells)
    num_cols = len(cells[0])
    field = np.zeros((num_rows,num_cols))
    for row in range(num_rows) :
        for col in range(num_cols) :
            field[row][col] = cells[row][col].get_state()

    plt.imshow(field)
    plt.show()



def main() :
    num_rows = 250
    num_cols = 1000
    cells = init_cells(num_rows, num_cols)

    time_steps = 2
    for time_step in range(time_steps) :
        for row in range(num_rows) :
            for col in range(num_cols) :
                cell = cells[row][col]
                neighbor_coords = get_neighbors(row, col, num_rows, num_cols)
                neighbor_cells = [cells[neighb_row][neighb_col] for (neighb_row, neighb_col) in neighbor_coords]
                cell.update(neighbor_cells)
        display(cells)

if __name__ == "__main__" :
    main()
