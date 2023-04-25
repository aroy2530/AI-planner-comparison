# import gtpyhop
# state = gtpyhop.State('state1')

# read in the file
filename = 'problems\\sat-3.txt' # change to take in vars
f = open(filename, "r")
lines = f.readlines()
init = False # keep track of whether we're seeing init stuff
goal = False # keep track of whether we're seeing goal stuff

###TODO: add state back in
pointing = {}
fuel = {}
slew_time = {}
fuel_used = 0
on_board = {}
power_avail = {}
power_on = {}
calibration_target = {}
calibrated = {}
supports = {}
data_capacity = {}
data = {}
data_stored = 0
have_image = {}
gpointing = {}
ghave_image = {}

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
            if words[2] in supports:
                supports[words[2]].append(words[1])
            else:
                supports[words[2]] = [words[1]]
        elif 'calibration_target' in words:
            calibration_target[words[1]] = words[2]
        elif 'on_board' in words:
            on_board[words[1]] = words[2]
        elif 'power_avail' in words:
            power_avail[words[1]] = True
        elif 'pointing' in words:
            pointing[words[1]] = words[2]
        elif 'data_capacity' in words:
            data_capacity[words[2]] = float(words[3])
        elif 'fuel' in words:
            fuel[words[2]] = float(words[3])
        elif 'data' in words:
            data[(words[2], words[3])] = float(words[4])
        elif 'slew_time' in words:
            slew_time[(words[2], words[3])] = float(words[4])
   
    elif goal:
        # goal only has pointing and have_image
        if 'pointing' in words:
            gpointing[words[1]] = words[2]
        elif 'have_image' in words:
            ghave_image[(words[1], words[2])] = True