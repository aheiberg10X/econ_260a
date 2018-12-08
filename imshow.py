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

    outputfile = os.path.join(root, "log.txt")
    with open(outputfile, 'w') as fout :
        fout.write("%s\n" % "Time,Developed,Wild,Fires Started,Burn Iterations,Total Burnt")
        for time_step in range(time_steps) :

            name = "devel_%d" % (time_step)
            filename = os.path.join(root, "%s.png" % name)

            #render current state
            cells.display(filename)

            #decide to build or not
            num_developed = cells.update_developed_state()

            #See if anything catches fire
            burn_iteration = 0
            fire_susceptibility = random.uniform(.5,1.5)
            num_fires_started = 0
            while True :
                #random walk starting from the current susceptibility
                fire_susceptibility += random.uniform(-.1-burn_iteration/float(20),.1)
                cells.update_fire_state(susceptibility=fire_susceptibility,
                                        no_new_start=burn_iteration > 0)
                if cells.state_counts[cell.BURNING] > 0 :
                    if burn_iteration == 0 :
                        num_fires_started = cells.state_counts[cell.BURNING]

                    burn_name = "%s_burn_%d" % (name, burn_iteration)
                    filename = os.path.join(root, "%s.png" % burn_name)
                    cells.display(filename)
                else :
                    break

                burn_iteration += 1

            fout.write("%d,%d,%d,%d,%d,%d\n" % (time_step,
                                             cells.state_counts[cell.DEVEL],
                                             cells.state_counts[cell.WILD],
                                             num_fires_started,
                                             burn_iteration,
                                             cells.state_counts[cell.BURNT]))

if __name__ == "__main__" :
    main()


    # once initialized to DEVEL or WILD, a cell only can transition to burning/burned or not
    # ie nothign goes WILD to DEVEL
    # how do things go from WILD to devel
    # probabilisticaly?
    # or depending on neighbors?
    # if that ineq is true, always turn to develped?
    # or if conditions are met, then there is a chance to become DEVEL
