import gtpyhop

"""
Each gtpyhop action is a Python function. The 1st argument is the current
state, and the others are the action's usual arguments. This is analogous to
how methods are defined for Python classes (where the first argument is
always the name of the class instance). For example, the function
pickup(s,b) implements the action ('pickup', b).

Useful relationship info:
- A satellite can only point in 1 direction
- An instrument only has 1 calibration target
- Multiple instruments can be on board a satellite, but an instrument can only be aboard 1 satellite
- Each satellite has a set data capacity and amount of fuel to start with
- An instrument can support multiple modes
- A satellite loses available power when an instrument is switched on ---
    meaning, only one instrument can be on at a time on a satellite
- Images can be taken of the same direction in multiple modes
"""

def turn_to(state, sat, d_new, d_prev):
    if state.pointing[sat] == d_prev and d_new != d_prev and state.fuel[sat] >= state.slew_time[(d_new, d_prev)]:
        state.pointing[sat] = d_new # point sat to d_new
        # skip not pointing to d_prev bc above line takes care of that
        state.fuel[sat] -= state.slew_time[(d_new, d_prev)]
        state.fuel_used += state.slew_time[(d_new, d_prev)]
        return state

def switch_on(state, i, sat):
    if state.on_board[i] == sat and state.power_avail[sat] == True:
        state.power_on[i] = True
        state.calibrated[i] = False
        state.power_avail[sat] = False
        return state

def switch_off(state, i, sat):
    if state.on_board[i] == sat and state.power_on[i] == True:
        state.power_on[i] = False
        state.power_avail[sat] = True
        return state

def calibrate(state, sat, i, d):
    if (state.on_board[i] == sat and state.calibration_target[i] == d 
            and state.pointing[sat] == d and state.power_on[i] == True):
        state.calibrated[i] = True
        return state

def take_image(state, sat, d, i, m):
    if (state.calibrated[i] == True and state.on_board[i] == sat and i in state.supports[m]
            and state.power_on[i] == True and state.pointing[sat] == d 
            and state.data_capacity[sat] >= state.data[(d, m)]):
        state.data_capacity[sat] -= state.data[(d, m)]
        state.have_image[(d, m)] = True
        state.data_stored += state.data[(d, m)]
        return state

# Tell Pyhop what the actions are
#
gtpyhop.declare_actions(turn_to, switch_on, switch_off, calibrate, take_image)