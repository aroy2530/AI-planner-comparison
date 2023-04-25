import gtpyhop

################################################################################
# Helper functions 

def find_instrument(state, d, m):
    # first, get the list of instruments that support mode m
    # state.supports[m] returns a list of instruments that supports it
    supp_instr = state.supports[m]
    # of these instruments, we want to choose one that will require the least fuel to calibrate and turn
    min_fuel = float("inf")
    best_sat = ""
    best_instr = ""
    for curr_i in supp_instr:
        curr_fuel = 0
        # figure out what sat it's on
        curr_sat = state.on_board[curr_i]

        # how much fuel to calibrate?
        curr_ct = state.calibration_target[curr_i]
        # first check if its calibrated
        if curr_i not in state.calibrated or not state.calibrated[curr_i]:
            if state.pointing[curr_sat] != curr_ct:
                # get fuel/slew-time
                curr_fuel += state.slew_time[(curr_ct, state.pointing[curr_sat])]

        # how much fuel to take image?
        # is the calibration target same as d? then we're all set
        if curr_ct != d:
            # get fuel/slew-time
            curr_fuel += state.slew_time[(d, curr_ct)]

        # check if min fuel so far AND if the satellite has enough fuel for these operations AND if it has enough data
            # may need to come back and account for future operations (like if this sat needs to point elsewhere at the end)
        if curr_fuel < min_fuel and state.fuel[curr_sat] >= curr_fuel and state.data_capacity[curr_sat] >= state.data[(d, m)]:
             min_fuel = curr_fuel
             best_sat = curr_sat
             best_instr = curr_i
    
    return (best_instr, best_sat)

def find_powered_instrument(state, sat):
     # get list of instruments on this sat
     instr_on_sat = list(state.on_board.keys())
     print("List of instruments on sat ", sat, instr_on_sat)
     for i in instr_on_sat:
        if i in state.power_on:
            if state.power_on[i] == True:
                return i
        
################################################################################
### method for multigoals

def m_img_move(state, mgoal):
    # two situations: satellite is not pointing in the right direction
        # OR an image has not been taken

    # goal.have_image = {'(Star3, thermograph4)': True, '(Planet4, thermograph2)': True}
    # goal.pointing = {'Satellite8': 'GS2', 'Satellite9': 'GS2'}

    # look for an image that hasn't been taken
    for (d, m) in mgoal.have_image:
        if (d,m) not in state.have_image:
            return [('m_take_image', d, m), mgoal]
        
    # look for sat not pointing in right dir
    for sat in mgoal.pointing:
        if state.pointing[sat] != mgoal.pointing[sat]:
            return [('point', sat, mgoal.pointing[sat]), mgoal]
    
    # if we get here, we are at goal state
    return []

gtpyhop.declare_multigoal_methods(m_img_move)


################################################################################
### methods for tasks

# Given a direction and mode, take an image
def m_take_image(state, d, m):
    i, sat = find_instrument(state, d, m) # find best instrument (in terms of fuel and data)
    # if no instrument was found, we fail
    if i == "":
        return False
    # switch on instrument, calibrate instrument, point sat in direction d, then take image
    return [('power', i, sat), ('m_calibrate', i, sat), ('point', sat, d), ('take_image', sat, d, i, m)]

gtpyhop.declare_task_methods('m_take_image', m_take_image)

def m_power(state, i, sat):
    """
    Give power to instrument i.
    """
    # only do this stuff if the instrument isnt already on! otherwise we have to recalibrate
    if i not in state.power_on or state.power_on[i] == False:
        if state.power_avail[sat] == True:
            return [('switch_on', i, sat)]
        else:
            # find instrument w power and turn off
            powered_i = find_powered_instrument(state, sat)
            return [('switch_off', powered_i, sat), ('switch_on', i, sat)]
    else:
        return [] # need to return something to keep it going
    
gtpyhop.declare_task_methods('power', m_power)

def m_calibrate(state, i, sat):
    # i not in state.calibrated -- can stick w below since calibrated is set to False when i is turned on which is always before this
    if state.calibrated[i] == False:
        # if not pointing in direction of cal target
        if state.calibration_target[i] != state.pointing[sat]:
            return [('turn_to', sat, state.calibration_target[i], state.pointing[sat]), ('calibrate', sat, i, state.calibration_target[i])]
        else:
            return [('calibrate', sat, i, state.calibration_target[i])]
    else:
        return []
    
gtpyhop.declare_task_methods('m_calibrate', m_calibrate)

def m_point(state, sat, target_d):
    # check fuel
    if state.fuel[sat] >= state.slew_time[(target_d, state.pointing[sat])]:
        return [('turn_to', sat, target_d, state.pointing[sat])]
    else:
        print("low fuel")
        return False
    
gtpyhop.declare_task_methods('point', m_point)