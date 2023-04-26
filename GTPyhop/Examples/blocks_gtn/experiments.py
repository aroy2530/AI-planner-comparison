import gtpyhop
import csv
import time

# We must declare the current domain before importing methods and actions.
# To make the code more portable, we don't hard-code the domain name, but
# instead use the name of the package.
the_domain = gtpyhop.Domain(__package__)

from .methods import *
from .actions import *

print('-----------------------------------------------------------------------')
print(f"Created '{gtpyhop.current_domain}'. To run the examples, type this:")
print(f'{the_domain.__name__}.main()')


#############     beginning of tests     ################

def main(do_pauses=True):
    """
    Run various examples.
    main() will pause occasionally to let you examine the output.
    main(False) will run straight through to the end, without stopping.
    """

    # If we've changed to some other domain, this will change us back.
    print(f"Changing current domain to {the_domain}, if it isn't that already.")
    gtpyhop.current_domain = the_domain

    size_folders = ['size-7', 'size-9', 'size-11', 'size-12', 'size-13', 'size-14', 'size-15', 'size-16', 'size-17', 'size-18']

    for size in size_folders:
        prob_num = 1
        while prob_num <= 10:
            state, goal = bw_pddltopy(f'blocks_gtn\\problems\\{size}\\{prob_num}.txt') # starting in Examples dir
            
            # state.display('Initial state is')
            # goal.display('Goal state is')
            # gtpyhop.verbose = 2

            start = time.time()

            plan = gtpyhop.find_plan(state,[goal])
            
            end = time.time()
            cpu_time = end - start

            plan_len = len(plan)
            print("Plan Length", plan_len, "CPU Time", cpu_time)

            with open("results.csv", "a", encoding="UTF8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([size, prob_num, plan_len, cpu_time])

            prob_num += 1


def bw_pddltopy(problem_file):
    # problem_file = 'blocks_htn\\bw-3.txt' # change to take in vars
    f = open(problem_file, "r")
    lines = f.readlines()
    init = False # keep track of whether we're seeing init stuff
    goal = False # keep track of whether we're seeing goal stuff

    istate = gtpyhop.State('state1')
    gstate = gtpyhop.Multigoal('goal1a')

    istate.pos = {}
    gstate.pos = {}
    istate.clear = {}
    istate.holding = {'hand': False}

    for line in lines:
        # get rid of parens and colons
        nline = line.replace('(', '').replace(')', '').replace(':', '')
        # split line up by words
        words = nline.split()
        # print(words)

        if 'init' in words:
            # we know the next set of lines until goal is our initial state
            init = True
        elif 'goal' in words:
            init = False
            goal = True
        elif init:
            # pos -> on, on-table
            if 'on-table' in words:
                istate.pos[words[1]] = 'table'
            elif 'on' in words:
                istate.pos[words[1]] = words[2]
                istate.clear[words[2]] = False # we can figure out which blocks aren't clear if smth is stacked on it
            # clear
            elif 'clear' in words:
                istate.clear[words[1]] = True
        elif goal:
            # goal only has on and on-table
            if 'on-table' in words:
                gstate.pos[words[1]] = 'table'
            elif 'on' in words:
                gstate.pos[words[1]] = words[2]

    return istate, gstate


# It's tempting to make the following call to main() unconditional, to run the
# examples without making the user type an extra command. But if we do this
# and an error occurs while main() is executing, we get a situation in which
# the actions, methods, and examples files have been imported but the module
# hasn't been - which causes problems if we try to import the module again.

if __name__=="__main__":
    main()
