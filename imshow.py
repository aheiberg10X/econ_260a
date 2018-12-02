from math import floor
import cell
import os



def main() :
    root = "/home/dev/amelia_econ/output_test"
    if not os.path.exists(root) :
        os.mkdir(root)

    num_rows = 25
    num_cols = 100
    cells = cell.CellGrid(num_rows, num_cols)

    time_steps = 2
    for time_step in range(time_steps) :
        name = "r%d_c%d_step%d" % (num_rows, num_cols, time_step)
        filename = os.path.join(root, "%s.png" % name)
        cells.display(filename)
        cells.update()

if __name__ == "__main__" :
    main()
