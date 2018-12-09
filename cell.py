import matplotlib.pyplot as plt
import random as random
import numpy as np
from math import pow
from states import WILD, DEVEL, BURNT, BURNING, NUM_STATES
import parameters as params

class Cell(object) :
    def __init__(self,
                 mean_cost_to_develop,
                 std_cost_to_develop,
                 mean_rent,
                 std_rent) :
        self.state = WILD
        self.burnable_value = 1
        self.cost_to_develop = np.random.normal(mean_cost_to_develop, std_cost_to_develop)
        self.rent = np.random.normal(mean_rent, std_rent)

    def estimate_destruction(self, neighbor_density) :
        #TODO: this is a placeholder. Peak at density=.5, zero at density=0 and 1
        #Not realistic, should never be 0
        shifted = neighbor_density - .5
        if shifted < 0 :
            shifted *= -1
        return params.MAX_EST_FIRE_PROB - (shifted * params.MAX_EST_FIRE_PROB/.5)

    def estimate_rent(self, horizon, devel_density, neighbor_density) :
        prob_survival = 1 - self.estimate_destruction(devel_density)
        expected_profit = 0
        for year in range(horizon) :
            expected_profit += self.rent * (1+neighbor_density*8) * pow(prob_survival, year)

        return expected_profit

    def estimate_cost(self,
                      horizon,
                      devel_density,
                      neighbor_density) :
        return self.cost_to_develop

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
        devel_density = (num_developed_neighbors + 1) / float(len(neighbors) + 1)
        neighbor_density = num_developed_neighbors / float(len(neighbors))
        expected_profit = self.estimate_rent(params.TIME_HORIZON,
                                             devel_density,
                                             neighbor_density)

        expected_cost = self.estimate_cost(params.TIME_HORIZON,
                                           devel_density,
                                           neighbor_density)

        if expected_profit > expected_cost :
            self.state = DEVEL
        else :
            self.state = WILD

        # if cell.state == WILD and num_developed_neighbors > 1 :
        #     self.state = DEVEL
        # else :
            # self.state = cell.state

    def is_burn_because_neighbors(self, n_burning_neighbors, prob_catch) :
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
            if not no_new_start and random.random() < params.FIRE_START_PROB_WILD * susceptibility :
                self.state = BURNING
                self.burn()
            else :
                neighbors_burning = sum([1 for n in neighbors if n.state == BURNING])
                catch_fire = self.is_burn_because_neighbors(neighbors_burning,
                                                         susceptibility * params.FIRE_CATCH_PROB_WILD)
                if catch_fire :
                    self.state = BURNING
                    self.burn()
                else :
                    self.state = WILD

        elif cell.state == DEVEL :
            neighbors_devel = sum([1 for n in neighbors if n.state == DEVEL])
            if not no_new_start and \
               random.random() < susceptibility * params.FIRE_START_PROB_DEVEL and \
               neighbors_devel < len(neighbors) :
                self.state = BURNING
                self.burn()
            else :
                neighbors_burning = sum([1 for n in neighbors if n.state == BURNING])
                catch_fire = self.is_burn_because_neighbors(neighbors_burning,
                                                         susceptibility * params.FIRE_CATCH_PROB_DEVEL)
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


