from cell import Cell

class CellConsiderate(Cell) :
    def __init__(self,
                 mean_cost_to_develop,
                 std_cost_to_develop,
                 mean_rent,
                 std_rent) :
        super(CellConsiderate, self).__init__(mean_cost_to_develop,
                                              std_cost_to_develop,
                                              mean_rent,
                                              std_rent)

    def estimate_destruction(self, neighbor_density) :
        return super(CellConsiderate, self).estimate_destruction(neighbor_density)

    def estimate_rent(self,
                      horizon,
                      devel_density,
                      neighbor_density) :
        return super(CellConsiderate, self).estimate_rent(horizon,
                                                          devel_density,
                                                          neighbor_density)

    def update_developed_state(self,
                               cell,
                               neighbors) :
        super(CellConsiderate, self).update_developed_state(cell, neighbors)

    def is_burn_because_neighbors(self,
                                  n_burning_neighbors,
                                  prob_catch) :
        return super(CellConsiderate, self).is_burn_because_neighbors(n_burning_neighbors,
                                                                      prob_catch)

    def update_fire_state(self,
                          cell,
                          neighbors,
                          susceptibility,
                          no_new_start) :
        return super(CellConsiderate, self).update_fire_state(cell,
                                                              neighbors,
                                                              susceptibility,
                                                              no_new_start)

    def burn(self) :
        super(CellConsiderate, self).burn()

    def get_state(self) :
        return super(CellConsiderate, self).get_state()
