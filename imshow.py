from math import floor
import cell
import os
import random



def main() :
    root = "/home/dev/amelia_econ/output_test"

    if not os.path.exists(root) :
        os.mkdir(root)
    else :
        for listing in os.listdir(root) :
            fullpath = os.path.join(root, listing)
            if os.path.isfile(fullpath):
                os.unlink(fullpath)


    num_rows = 25
    num_cols = 100
    cells = cell.CellGrid(num_rows, num_cols)

    time_steps = 10
    for time_step in range(time_steps) :
        print "Time step %d" % (time_step)

        name = "devel_%d" % (time_step)
        filename = os.path.join(root, "%s.png" % name)

        #render current state
        cells.display(filename)

        #decide to build or not
        cells.update_developed_state()

        #See if anything catches fire
        burn_iteration = 0
        fire_susceptibility = random.uniform(.5,1.5)
        while True :
            #random walk starting from the current susceptibility
            fire_susceptibility += random.uniform(-.1-burn_iteration/float(10),.1)
            num_burning = cells.update_fire_state(susceptibility=fire_susceptibility,
                                                  no_new_start=burn_iteration > 0)
            if num_burning > 0 :
                print "    num burning: %d" % num_burning
                print "    susceptibility: %f" % fire_susceptibility
                burn_name = "%s_burn_%d" % (name, burn_iteration)
                filename = os.path.join(root, "%s.png" % burn_name)
                cells.display(filename)
            else :
                break

            burn_iteration += 1

if __name__ == "__main__" :
    main()


    # once initialized to DEVEL or WILD, a cell only can transition to burning/burned or not
    # ie nothign goes WILD to DEVEL
    # how do things go from WILD to devel
    # probabilisticaly?
    # or depending on neighbors?
    # if that ineq is true, always turn to develped?
    # or if conditions are met, then there is a chance to become DEVEL
