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

    def estimate_rent(self,
                      horizon,
                      devel_density,
                      neighbor_density) :
        #TODO: compute how adding this cell will imporove the values of the lands around it

        #Below is just the placeholder, does the same as a regular "Cell"
        return super(CellConsiderate, self).estimate_rent(horizon,
                                                          devel_density,
                                                          neighbor_density)

    def estimate_cost(self,
                      horizon,
                      devel_density,
                      neighbor_density) :
        #TODO: compute the odds of destroying your neighbors by putting a house here

        #Below is just the placeholder, does the same as a regular "Cell"
        return super(CellConsiderate, self).estimate_rent(horizon,
                                                          devel_density,
                                                          neighbor_density)

