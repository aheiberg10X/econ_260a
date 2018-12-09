import matplotlib.pyplot as plt
import copy
import random as random
import numpy as np

#from cell import Cell as Cell
from cell_considerate import CellConsiderate as Cell

import parameters as params
from states import NUM_STATES, WILD, DEVEL, BURNING, BURNT

palette = np.array([[  0,   0,   0],   # black
                    [  255,   0,   0],   # red
                    [  0,   120,   0],   # green
                    [  255,   255,   255],   # white
                    [  0,   0,   255]])  # blue


def get_neighbors_devel(row, col, num_rows, num_cols, window=1) :
    for r in range(row-window, row+window+1) :
        if r < 0 or r >= num_rows :
            continue
        for c in range(col-window, col+window+1) :
            if c < 0 or c >= num_cols :
                continue
            if r == row and c == col :
                continue
            yield (r, c)

def get_neighbors_fire(row, col, num_rows, num_cols) :
    possible = [(row-1, col),
            (row, col-1),
            (row, col+1),
            (row+1, col)]

    for (r,c) in possible :
        if r < 0 or r >= num_rows or c < 0 or c >= num_cols :
            pass
        else :
            yield (r,c)

class CellGrid :
    def __init__(self, num_rows, num_cols) :
        self.nrows = num_rows
        self.ncols = num_cols

        self.state_counts = [0]*NUM_STATES
        self.state_counts[WILD] = num_rows * num_cols
        self.state_counts[DEVEL] = 0
        self.state_counts[BURNING] = 0
        self.state_counts[BURNT] = 0

        init_cells = [[Cell(params.MEAN_COST_TO_DEVELOP,
                            params.STD_COST_TO_DEVELOP,
                            params.MEAN_RENT,
                            params.STD_RENT) for i in range(num_cols)] for j in range(num_rows)]

        self.cells = [init_cells,
                      copy.deepcopy(init_cells)]
        self.current_cells_ix = 0

        if self.nrows == 0 :
            assert False

        average_density = params.DENSITY_OF_HOMES
        num_devel = 0
        for row in range(num_rows) :
            row_modulator = 2 * float(row) / num_rows
            num_to_sample = int(round(num_cols * row_modulator * average_density))
            sample = random.sample(range(num_cols), num_to_sample)

            current_cells = self.cells[self.current_cells_ix]
            for col in sample :
                current_cells[row][col].state = DEVEL

            self.state_counts[DEVEL] += len(sample)
            self.state_counts[WILD] -= len(sample)

    def toggle_index(self, index) :
        if index == 0 : return 1
        elif index == 1 : return 0
        else : assert False

    def update_developed_state(self) :
        current_cells = self.cells[self.current_cells_ix]
        next_cells = self.cells[self.toggle_index(self.current_cells_ix)]

        developed_count = 0
        for row in range(self.nrows) :
            for col in range(self.ncols) :
                cell = current_cells[row][col]
                neighbor_coords = get_neighbors_devel(row,
                                                      col,
                                                      self.nrows,
                                                      self.ncols,
                                                      params.NEIGHBOR_WINDOW)
                neighbor_cells = [current_cells[neighb_row][neighb_col] for (neighb_row, neighb_col) in neighbor_coords]
                next_cells[row][col].update_developed_state(cell, neighbor_cells)

                self.state_counts[next_cells[row][col].state] += 1
                self.state_counts[current_cells[row][col].state] -= 1

        self.current_cells_ix = self.toggle_index(self.current_cells_ix)
        return developed_count

    def update_fire_state(self,
                          susceptibility=1.0,
                          no_new_start=False) :

        current_cells = self.cells[self.current_cells_ix]
        next_cells = self.cells[self.toggle_index(self.current_cells_ix)]

        for row in range(self.nrows) :
            for col in range(self.ncols) :
                cell = current_cells[row][col]
                neighbor_coords = get_neighbors_fire(row, col, self.nrows, self.ncols)
                neighbor_cells = [current_cells[neighb_row][neighb_col] for (neighb_row, neighb_col) in neighbor_coords]
                next_cells[row][col].update_fire_state(cell,
                                                       neighbor_cells,
                                                       susceptibility,
                                                       no_new_start)

                self.state_counts[next_cells[row][col].state] += 1
                self.state_counts[current_cells[row][col].state] -= 1

        self.current_cells_ix = self.toggle_index(self.current_cells_ix)

    def display(self, filename) :
        field = np.zeros((self.nrows, self.ncols), dtype=np.uint8)
        cells = self.cells[self.current_cells_ix]
        for row in range(self.nrows) :
            for col in range(self.ncols) :
                field[row][col] = cells[row][col].get_state()


        RGB = palette[field]
        RGB = RGB.astype(np.uint8)
        plt.imshow(RGB)
        plt.savefig(filename)
        #plt.show()

def sample_profits(mean_cost_to_develop,
                          std_cost_to_develop,
                          mean_rent,
                   std_rent,
                          num_devel_neighbors,
                          horizon) :
    profits = []
    devel_density = (num_devel_neighbors + 1) / float(9)
    neighbor_density = (num_devel_neighbors) / float(8)
    for sample in range(1000) :
        c = Cell(mean_cost_to_develop,
                std_cost_to_develop,
                mean_rent,
                std_rent)

        rent = c.estimate_rent(horizon,
                               devel_density,
                               neighbor_density)

        cost = c.cost_to_develop
        profits.append(rent - cost)

    return profits

if __name__ == "__main__" :
    num_potential_neighbors = len(list(get_neighbors_devel(4, 4, 8, 8, params.NEIGHBOR_WINDOW)))
    fig, axes = plt.subplots(nrows=num_potential_neighbors,
                             ncols=1,
                             figsize=(12,num_potential_neighbors),
                             sharex=True,
                             sharey=True)

    for num_neighbors in range(num_potential_neighbors) :
        profits = sample_profits(params.MEAN_COST_TO_DEVELOP,
                                 params.STD_COST_TO_DEVELOP,
                                 params.MEAN_RENT,
                                 params.STD_RENT,
                                 num_neighbors,
                                 params.TIME_HORIZON)
        axes[num_neighbors].hist(profits)

    plt.show()
