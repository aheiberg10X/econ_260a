import matplotlib.pyplot as plt
import random as random
import numpy as np

#states
WILD = 0
DEVEL = 1
BURNT = 2

class Cell :
    def __init__(self) :
        self.state = WILD

    def get_new_state(self, neighbors) :
        if self.state == WILD : return DEVEL
        if self.state == DEVEL : return WILD

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

    for (r,c) in possible :
        if r < 0 or r >= num_rows or c < 0 or c >= num_cols :
            pass
        else :
            yield (r,c)

class CellGrid :
    def __init__(self, num_rows, num_cols) :
        self.nrows = num_rows
        self.ncols = num_cols

        self.cells = [[[Cell() for i in range(num_cols)] for j in range(num_rows)],
                      [[Cell() for i in range(num_cols)] for j in range(num_rows)]]
        self.current_cells_ix = 0

        if self.nrows == 0 :
            assert False

        average_density = .01
        num_devel = 0
        for row in range(num_rows) :
            row_modulator = 2 * float(row) / num_rows
            num_to_sample = int(round(num_cols * row_modulator * average_density))
            sample = random.sample(range(num_cols), num_to_sample)

            current_cells = self.cells[self.current_cells_ix]
            for col in sample :
                current_cells[row][col].state = DEVEL
            num_devel += len(sample)

        print "Number of cells develeoped during init: %d" % (num_devel)

    def toggle_index(self, index) :
        if index == 0 : return 1
        elif index == 1 : return 0
        else : assert False

    def update(self) :
        current_cells = self.cells[self.current_cells_ix]
        next_cells = self.cells[self.toggle_index(self.current_cells_ix)]

        for row in range(self.nrows) :
            for col in range(self.ncols) :
                cell = current_cells[row][col]
                neighbor_coords = get_neighbors(row, col, self.nrows, self.ncols)
                neighbor_cells = [current_cells[neighb_row][neighb_col] for (neighb_row, neighb_col) in neighbor_coords]
                next_cells[row][col].state = cell.get_new_state(neighbor_cells)

        self.current_cells_ix = self.toggle_index(self.current_cells_ix)


    def display(self, filename) :
        field = np.zeros((self.nrows, self.ncols))
        cells = self.cells[self.current_cells_ix]
        for row in range(self.nrows) :
            for col in range(self.ncols) :
                field[row][col] = cells[row][col].get_state()

        plt.imshow(field)
        plt.savefig(filename)
        plt.show()

