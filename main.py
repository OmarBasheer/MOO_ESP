from random import randint
from support_methods import *
import matplotlib.pyplot as plt
import numpy
import numpy as np
import matplotlib

###############


num_sa = 36  # Number of appliances put to test
num_slots = 1440  # Number of time slots, 1 minute each, demonstrating a full day
all_sa = range(num_sa)
all_slots = range(num_slots)
remaining_slots = num_slots
appliances = getAppliances()
ps_max_list = np.zeros(1441)

positions = []
consumption_per_min = []
# randomize appliance within LB & (UB - l)
for x in all_sa:
    slotter = randint(appliances[x][2], appliances[x][3] - appliances[x][1])
    positions.append([x, slotter, appliances[x]])  # [Appliance #, starting slot, appliance details]
    for mint in range(slotter, slotter + appliances[x][1] + 1):
        consumption_per_min.append([mint, appliances[x][4]])
consumption_per_min.sort()

print(positions)
print(consumption_per_min)

for x in consumption_per_min:
    ps_max_list[x[0]] = ps_max_list[x[0]] + x[1]

print(ps_max_list)

ps_max = ps_max_list[np.argmax(ps_max_list)]
ps_avg = Average(ps_max_list)


# get price per minute list
price_per_min = getPricePerMin()

eb_sum = 0
ps_list = []
ps_min = []
for appliance in positions:  # Loop through all appliances
    for minute in range(appliance[2][1]):  # Loop through durations of each appliance
        ans, ps_list, ps_min = price_calculate(appliance[1] + minute,
                                               appliance[2][4], ps_list, ps_min,
                                               price_per_min)  # calculate the price based on starting slot + duration
        eb_sum = eb_sum + ans
print("Electricity Price is", eb_sum)

par_val = ps_max / ps_avg
wtr_avg_val = wtr_calc(positions)
