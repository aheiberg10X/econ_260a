import matplotlib.pyplot as plt
import random as random
import numpy as np
from math import pow

#states
WILD = 2
DEVEL = 4
BURNT = 0
BURNING = 1

FIRE_START_PROB_DEVEL = .01
FIRE_CATCH_PROB_DEVEL = .3
FIRE_START_PROB_WILD = 0
FIRE_CATCH_PROB_WILD = .5
MAX_EST_FIRE_PROB = .04

DENSITY_OF_HOMES = .01
MEAN_COST_TO_DEVELOP = 1
MEAN_RENT = MEAN_COST_TO_DEVELOP / float(70)

TIME_HORIZON = 50 #years
BURNT_REGEN_TIME = 1

palette = np.array([[  0,   0,   0],   # black
                    [  255,   0,   0],   # red
                    [  0,   120,   0],   # green
                    [  0,   0,   255],   # blue
                    [  255,   255,   255]])  # white

class Cell :
    def __init__(self) :
        self.state = WILD
        self.burnable_value = 1
        self.cost_to_develop = np.random.normal(MEAN_COST_TO_DEVELOP, MEAN_COST_TO_DEVELOP/float(5))
        self.rent = np.random.normal(MEAN_RENT, MEAN_RENT/float(5))

    def estimate_destruction(self, neighbor_density) :
        #TODO: this is a placeholder. Peak at density=.5, zero at density=0 and 1
        #Not realistic, should never be 0
        shifted = neighbor_density - .5
        if shifted < 0 :
            shifted *= -1
        return MAX_EST_FIRE_PROB - (shifted * MAX_EST_FIRE_PROB/.5)

    def update_developed_state(self, cell, neighbors) :
        if cell.state == DEVEL:
            self.state = DEVEL
            return

        if cell.state == BURNT :
            self.state = BURNT
            return

        if cell.state == BURNING:
            self.state = BURNING
            return

        num_developed_neighbors = sum([1 for n in neighbors if n.state == DEVEL])
        expected_profit = 0
        devel_density = (num_developed_neighbors + 1) / float(len(neighbors) + 1)
        neighbor_density = num_developed_neighbors / float(len(neighbors))
        est_prob_destruction = self.estimate_destruction(devel_density)
        for year in range(TIME_HORIZON) :
            expected_profit += self.rent * (1+neighbor_density*8) * pow(1-est_prob_destruction, year)


        # if neighbor_density == 0 :
        #      print num_developed_neighbors
        #      print "discount : %f" % (1-est_prob_destruction)
        #     print "exp profit: %f, cost: %f" % (expected_profit, self.cost_to_develop)

        if num_developed_neighbors > 0 :
            print num_developed_neighbors
            print "discount : %f" % (1-est_prob_destruction)
            print "exp profit: %f, cost: %f" % (expected_profit, self.cost_to_develop)

        if expected_profit > self.cost_to_develop :
            if random.random() < .5 :
                self.state = DEVEL
        else :
            self.state = WILD

        # if cell.state == WILD and num_developed_neighbors > 1 :
        #     self.state = DEVEL
        # else :
            # self.state = cell.state

    def burn_because_neighbors(self, n_burning_neighbors, prob_catch) :
        for i in range(n_burning_neighbors) :
            if random.random() < prob_catch :
                return True
        return False

    def update_fire_state(self,
                          cell,
                          neighbors,
                          susceptibility=1.0,
                          no_new_start=False) :

        if cell.state == WILD :
            if not no_new_start and random.random() < FIRE_START_PROB_WILD * susceptibility :
                self.state = BURNING
                self.burn()
            else :
                neighbors_burning = sum([1 for n in neighbors if n.state == BURNING])
                catch_fire = self.burn_because_neighbors(neighbors_burning,
                                                         susceptibility * FIRE_CATCH_PROB_WILD)
                if catch_fire :
                    self.state = BURNING
                    self.burn()
                else :
                    self.state = WILD

        elif cell.state == DEVEL :
            neighbors_devel = sum([1 for n in neighbors if n.state == DEVEL])
            if not no_new_start and \
               random.random() < susceptibility * FIRE_START_PROB_DEVEL and \
               neighbors_devel < len(neighbors) :
                self.state = BURNING
                self.burn()
            else :
                neighbors_burning = sum([1 for n in neighbors if n.state == BURNING])
                catch_fire = self.burn_because_neighbors(neighbors_burning,
                                                         susceptibility * FIRE_CATCH_PROB_DEVEL)
                if catch_fire :
                    self.state = BURNING
                    self.burn()
                else :
                    self.state = DEVEL

        elif cell.state == BURNING :
            self.burnable_value = cell.burnable_value
            self.burn()
            if self.burnable_value <= 0 :
                self.state = BURNT
            else :
                self.state = BURNING

        elif cell.state == BURNT :
            self.state = BURNT

    def burn(self) :
        self.burnable_value -= 1

    def get_state(self) :
        return self.state


def get_neighbors_devel(row, col, num_rows, num_cols) :
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

        self.cells = [[[Cell() for i in range(num_cols)] for j in range(num_rows)],
                      [[Cell() for i in range(num_cols)] for j in range(num_rows)]]
        self.current_cells_ix = 0

        if self.nrows == 0 :
            assert False

        average_density = DENSITY_OF_HOMES
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

    def update_developed_state(self) :
        current_cells = self.cells[self.current_cells_ix]
        next_cells = self.cells[self.toggle_index(self.current_cells_ix)]

        for row in range(self.nrows) :
            for col in range(self.ncols) :
                cell = current_cells[row][col]
                neighbor_coords = get_neighbors_devel(row, col, self.nrows, self.ncols)
                neighbor_cells = [current_cells[neighb_row][neighb_col] for (neighb_row, neighb_col) in neighbor_coords]
                next_cells[row][col].update_developed_state(cell, neighbor_cells)

        self.current_cells_ix = self.toggle_index(self.current_cells_ix)

    def update_fire_state(self,
                          susceptibility=1.0,
                          no_new_start=False) :

        current_cells = self.cells[self.current_cells_ix]
        next_cells = self.cells[self.toggle_index(self.current_cells_ix)]

        burning_count = 0
        for row in range(self.nrows) :
            for col in range(self.ncols) :
                cell = current_cells[row][col]
                neighbor_coords = get_neighbors_fire(row, col, self.nrows, self.ncols)
                neighbor_cells = [current_cells[neighb_row][neighb_col] for (neighb_row, neighb_col) in neighbor_coords]
                next_cells[row][col].update_fire_state(cell,
                                                       neighbor_cells,
                                                       susceptibility,
                                                       no_new_start)

                if next_cells[row][col].state == BURNING :
                    burning_count += 1

        self.current_cells_ix = self.toggle_index(self.current_cells_ix)
        return burning_count

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

