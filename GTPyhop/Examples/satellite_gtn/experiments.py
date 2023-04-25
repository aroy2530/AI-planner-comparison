import gtpyhop

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
    size = 3

    initial, goal = sat_pddltopy(f'satellite_gtn\\problems\\sat-{size}.txt') # starting in Examples dir

    # initial.display('Initial state is')
    # goal.display('Goal state is')
    # gtpyhop.verbose = 2

    plan = gtpyhop.find_plan(initial,[goal])
    print(len(plan))

def sat_pddltopy(problem_file):
    # read in the file
    f = open(problem_file, "r")
    lines = f.readlines()
    init = False # keep track of whether we're seeing init stuff
    goal = False # keep track of whether we're seeing goal stuff

    istate = gtpyhop.State('state1')
    gstate = gtpyhop.Multigoal('goal1a')

    istate.pointing = {}
    istate.fuel = {}
    istate.slew_time = {}
    istate.fuel_used = 0
    istate.on_board = {}
    istate.power_avail = {}
    istate.power_on = {}
    istate.calibration_target = {}
    istate.calibrated = {}
    istate.supports = {}
    istate.data_capacity = {}
    istate.data = {}
    istate.data_stored = 0
    istate.have_image = {}
    gstate.pointing = {}
    gstate.have_image = {}

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
            if 'supports' in words:
                if words[2] in istate.supports:
                    istate.supports[words[2]].append(words[1])
                else:
                    istate.supports[words[2]] = [words[1]]
            elif 'calibration_target' in words:
                istate.calibration_target[words[1]] = words[2]
            elif 'on_board' in words:
                istate.on_board[words[1]] = words[2]
            elif 'power_avail' in words:
                istate.power_avail[words[1]] = True
            elif 'pointing' in words:
                istate.pointing[words[1]] = words[2]
            elif 'data_capacity' in words:
                istate.data_capacity[words[2]] = float(words[3])
            elif 'fuel' in words:
                istate.fuel[words[2]] = float(words[3])
            elif 'data' in words:
                istate.data[(words[2], words[3])] = float(words[4])
            elif 'slew_time' in words:
                istate.slew_time[(words[2], words[3])] = float(words[4])
    
        elif goal:
            # goal only has pointing and have_image
            if 'pointing' in words:
                gstate.pointing[words[1]] = words[2]
            elif 'have_image' in words:
                gstate.have_image[(words[1], words[2])] = True

    return istate, gstate

# It's tempting to make the following call to main() unconditional, to run the
# examples without making the user type an extra command. But if we do this
# and an error occurs while main() is executing, we get a situation in which
# the actions, methods, and examples files have been imported but the module
# hasn't been - which causes problems if we try to import the module again.

if __name__=="__main__":
    main()
