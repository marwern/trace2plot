import os
import matplotlib.pyplot as plt
import numpy as np


def get_all_variables(path_dir, filename, vars_to_print, simu_drivers):
    f = open(os.path.join(path_dir, filename), "r")
    first_line = False
    last_line = False

    for x in f:
        # find first line
        if "SIMULATION STEP 0" in x:
            first_line = True
            last_line = False

        # find last line
        if "delayed assignments of driver are:" in x:
            first_line = False
            last_line = True

        # find simulation drivers
        if "with driver " in x:
            simu_drivers.append(x.split('with driver')[1])

        # fill signal list
        if (' : ' in x) and not ('__' in x) and not ('.' in x) and first_line and not last_line and len(
                simu_drivers) == 1:
            # print(">> variable added: ",x.split(' : ')[0])
            vars_to_print.append(x.split(' : ')[0])
    f.close()


def get_vars_vals(vars_to_print, path_dir, filename, vals_to_print, simu_drivers, x_axis, drivers_to_simulate):
    var1 = []

    # prepare dummy arrays
    for var in range(len(vars_to_print)):
        vars()['var' + str(var)] = []

    # fill lists with simulation vals_to_print
    f = open(os.path.join(path_dir, filename), "r")
    for x in f:
        for var in range(len(vars_to_print)):
            if vars_to_print[var] + ' : ' in x:  # TODO "t :", "xt :", "xxt :", ...
                vars()['var' + str(var)].append(x)

    for var in range(len(vars_to_print)):
        vals_to_print[0].append(vars_to_print[var])
        tmp = vars()['var' + str(var)]
        for el in range(len(tmp)):
            tmp[el] = tmp[el].replace(tmp[el].split(' : ')[0] + ' : ', '')
        vals_to_print[1].append(tmp)

    # length of x-axis
    total_length = len(var1)
    driver_length = total_length / len(simu_drivers)
    for e in range(int(driver_length)):
        x_axis.append(e)

    for a in range(len(simu_drivers)):  # TODO
        drivers_to_simulate.append(simu_drivers[a].split("\n")[0])

    f.close()


def plot_traces(vals_to_print, vars_to_print, x_axis):
    fig = plt.figure()

    col = ('b', 'k', 'g', 'y', 'r', 'b', 'k', 'g', 'y', 'r', 'b', 'k', 'g', 'y', 'r', 'b', 'k', 'g', 'y', 'r', 'b', 'k', 'g', 'y')  # TODO

    for i, y in enumerate(vals_to_print[1]):
        tmp = [len(vals_to_print[1]), 1, i + 1]  # TODO
        ax = fig.add_subplot(tmp[0], tmp[1], tmp[2])
        ax.step(x_axis, vals_to_print[1][i], where='post', color=col[i], label=vars_to_print[i])
        ax.set_xticks(np.arange(0, len(x_axis), 1))

        # sharex workaround
        if i != len(vals_to_print[1]) - 1:
            ax.set_xticklabels(())

        plt.legend(bbox_to_anchor=(1.1, 1.05))
        plt.grid(visible=True, which='major', color='#666666', linestyle='-', alpha=0.3)

    plt.show()


def main():
    path_dir: str = r""  # add your local path
    filename: str = r"trace.txt"

    vars_to_print = []
    simu_drivers = []  # TODO
    vals_to_print = [[], []]
    x_axis = []  # TODO

    get_all_variables(path_dir, filename, vars_to_print, simu_drivers)
    get_vars_vals(vars_to_print, path_dir, filename, vals_to_print, simu_drivers, x_axis, simu_drivers)
    plot_traces(vals_to_print, vars_to_print, x_axis)


if __name__ == '__main__':
    main()
