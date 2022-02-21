from random import randint

num_sa = 36  # Number of appliances put to test
num_slots = 1440  # Number of time slots, 1 minute each, demonstrating a full day
all_sa = range(num_sa)
all_slots = range(num_slots)
remaining_slots = num_slots
appliances = [  # [Appliance, LOC, OTPs, OTPe]
              ['dw', 105, 540, 780], ['dw', 105, 840, 1080], ['dw', 105, 1200, 1440], ['ac', 30, 1, 120],
              ['ac', 30, 120, 240], ['ac', 30, 240, 360], ['ac', 30, 360, 480], ['ac', 30, 480, 600],
              ['ac', 30, 600, 720], ['ac', 30, 720, 840], ['ac', 30, 840, 960], ['ac', 30, 960, 1080],
              ['ac', 30, 1080, 1200], ['ac', 30, 1200, 1320], ['ac', 30, 1320, 1440], ['wm', 55, 60, 300],
              ['cd', 60, 300, 480], ['ref', 1440, 1, 1440], ['deh', 30, 1, 120], ['deh', 30, 120, 240],
              ['deh', 30, 240, 360], ['deh', 30, 360, 480], ['deh', 30, 480, 600], ['deh', 30, 600, 720],
              ['deh', 30, 720, 840], ['deh', 30, 840, 960], ['deh', 30, 960, 1080], ['deh', 30, 1080, 1200],
              ['deh', 30, 1200, 1320], ['deh', 30, 1320, 1440], ['ewh', 35, 300, 420], ['ewh', 35, 1100, 1440],
              ['cm', 10, 300, 450], ['cm', 10, 1020, 1140], ['pf', 180, 1, 540], ['pf', 180, 900, 1440]]


positions = []

# randomize appliance within LB & (UB - l)
for x in all_sa:
    found = False
    while not found:
        if (appliances[x][3] - appliances[x][1]) >= appliances[x][2]:
            slotter = randint(appliances[x][2], (appliances[x][3]-appliances[x][1]))
        else:
            slotter = appliances[x][2]
        #  print(slotter)
        positions.append([x, slotter, appliances[x]])
        found = True


print(positions)
# Electricity bill = sum of power required for appliance * power consumption profile tariff at that slot of time PC =
# a if  0 <= ps <= C || h if ps > C where C is consumption threshold between a & h, lambda positive ratio between 2
#
# tariffs h = lambda * a C = 0.0333 per time slot, lambda = 1.543 ps = {} pc = {} EB = sum(ps*pc)

# prices per hour every 60 slots
# 0-60 0.028
# 61-120 0.023
# 121-180 0.018
# 181-240 0.013
# 241-300 0.015
# 301-360 0.022
# 361-420 0.025
# 421-480 0.035** 0.054
# 481-540 0.04 0.062
# 541-600 0.0416666 0.065
# 601-660 0.045 0.069
# 661-720 0.05 0.077
# 721-780 0.051666 0.08
# 781-840 0.053333 0.082
# 841-900 0.055 0.085
# 901-960 0.065 0.1
# 961-1040 0.068 0.105
# 1041-1100 0.06166 0.096
# 1101-1160 0.053333 0.082
# 1161-1200 0.051666 0.08
# 1201-1260 0.05 0.077
# 1261-1320 0.046666 0.073
# 1321-1380 0.04 0.062
# 1381-1440 0.031666**

ap_cost = []
# sum_cost = 0
# fix boundaries

for x in positions:
    # print(x)
    for s in range(x[1], x[2][1]):
        print(s)


def price_calculate(minute):
    sum_cost = 0
    if 0 < minute <= 60:
        sum_cost = sum_cost + 1
    elif 60 < minute <= 120:
        ap_cost.append(3)
    elif 120 < minute < 180:
        ap_cost.append(3)
    elif 180 < minute <= 240:
        ap_cost.append(3)
    elif 240 < minute < 300:
        ap_cost.append(3)
    elif 300 < minute <= 360:
        ap_cost.append(3)
    elif 360 < minute < 420:
        ap_cost.append(3)
    elif 420 < minute <= 480:
        ap_cost.append(3)
    elif 480 < minute < 540:
        ap_cost.append(3)
    elif 540 < minute <= 600:
        ap_cost.append(3)
    elif 600 < minute < 660:
        ap_cost.append(3)
    elif 660 < minute <= 720:
        ap_cost.append(3)
    elif 720 < minute < 780:
        ap_cost.append(3)
    if 780 < minute <= 840:
        ap_cost.append(3)
    elif 840 < minute <= 900:
        ap_cost.append(3)
    elif 900 < minute < 960:
        ap_cost.append(3)
    elif 960 < minute <= 1020:
        ap_cost.append(3)
    elif 1020 < minute < 1080:
        ap_cost.append(3)
    elif 1080 < minute <= 1140:
        ap_cost.append(3)
    elif 1140 < minute < 1200:
        ap_cost.append(3)
    elif 1200 < minute <= 1260:
        ap_cost.append(3)
    elif 1260 < minute < 1320:
        ap_cost.append(3)
    elif 1320 < minute <= 1380:
        ap_cost.append(3)
    else:
        ap_cost.append(3)
    return sum_cost
