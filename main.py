from random import randint
from support_methods import *
import matplotlib.pyplot as plt
import numpy
import numpy as np
from pymoo.algorithms.soo.nonconvex.pso import PSO, PSOAnimation
from pymoo.factory import *
from pymoo.optimize import minimize


###############


num_sa = 36  # Number of appliances put to test
num_slots = 1440  # Number of time slots, 1 minute each, demonstrating a full day
all_sa = range(num_sa)
all_slots = range(num_slots)
remaining_slots = num_slots
loc, lb, ub, cost = getAppliances()
ps_max_list = np.zeros(1441)

positions = []
consumption_per_min = []
final_consumption_list = np.zeros(1440)
c = 0.0333
# randomize appliance within LB & (UB - l)
for x in all_sa:
    if ub[x] - loc[x] < lb[x]:
        slotter = 0
    else:
        slotter = randint(lb[x], ub[x] - loc[x])
    positions.append([x, slotter, loc[x], lb[x], ub[x], cost[x]])  # [Appliance #, starting slot, lower bound, upper bound]
    for mint in range(slotter, slotter + loc[x]):
        consumption_per_min.append([mint, cost[x]])
consumption_per_min.sort()

print("Appliances & their start time", positions)
# print(consumption_per_min)

for x in consumption_per_min:
    ps_max_list[x[0]] = ps_max_list[x[0]] + x[1]

# print(ps_max_list)

ps_max = ps_max_list[np.argmax(ps_max_list)]
ps_avg = Average(ps_max_list)


# get price per minute list
price_per_min = getPricePerMin()


# fix to have all of appliances
eb_sum = calculate_eb(positions, price_per_min)

# get consumption for each minute to test.
consumption_mins = np.zeros(1441)
for x in consumption_per_min:
    consumption_mins[x[0]] = consumption_mins[x[0]] + x[1]

print("Electricity Price is", eb_sum)

# lower PAR is better
#par_val = ps_max / ps_avg

# should be between 0 and 1
wtr_avg_val = wtr_calc(positions)

nsas = getnsa()

cpr_val = cpr_calc(consumption_mins, nsas)
#lastval = multiobjective(eb_sum, par_val, wtr_avg_val, cpr_val)
#print("PAR value: ", par_val)
print("WTR Average time: ", wtr_avg_val)
print("CPR value is: ", cpr_val)
#print("Last value is: ", lastval)