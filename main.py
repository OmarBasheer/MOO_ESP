from random import randint

import psoo
import ssa
from support_methods import *
#import matplotlib.pyplot as plt
import numpy as np
from mealpy.swarm_based.SSA import BaseSSA
from mealpy.swarm_based.PSO import BasePSO
from mealpy.utils.visualize import *


###############


num_sa = 36  # Number of appliances put to test
num_slots = 1440  # Number of time slots, 1 minute each, demonstrating a full day
all_sa = range(num_sa)
all_slots = range(num_slots)
remaining_slots = num_slots
loc, lb, ub, cost = get_appliances()
ps_max_list = np.zeros(1441)

consumption_per_min = []
final_consumption_list = np.zeros(1440)
c = 0.0333
# get price per minute list
price_per_min = getPricePerMin()

# randomize appliance within LB & (UB - l)
consumption_matrix = np.zeros((36, 1440))

consumption_per_min, app_st, app_et, bounds, consumption_matrix, positions = initialize()
## test multi objective ##
electricity = newBill(app_st)
a = newBill(app_st)
b = calculate_par(app_st)
par = calculate_par(app_st)
wtr = wtr_calc(app_st)
cpr = calc_cpr(app_st)
FF = objfun(electricity, par, wtr, cpr, a, b)
print("Objective value= ", FF)
#p = psoo.PSO(getBill, app_st, bounds=bounds, num_particles=20, maxiter=100)


problem_dict1 = {
         "fit_func": newBill,
         "lb": lb.tolist(),
         "ub": ub.tolist(),
         "minmax": "min",
         "loc": loc.tolist()
     }
epoch = 10
pop_size = 20
ST = 0.8
PD = 0.2
SD = 0.1
c1 = 2.05
c2 = 2.05
w_min = 0.4
w_max = 1

#model = BaseSSA(problem_dict1, epoch, pop_size, ST, PD, SD)
#best_position, best_fitness = model.solve()

model2 = BasePSO(problem_dict1, epoch, pop_size, c1, c2, w_min, w_max)
best_position2, best_fitness2 = model2.solve()
#best_position2 = np.round(best_position2)
#export_convergence_chart(model.history.list_population, title='Runtime chart', y_label="Second", x_label="Iteration")

#print(f"Solution: {best_position}, Fitness: {best_fitness}")

print(f"Solution: {np.round(best_position2)}, Fitness: {best_fitness2}")



eb_sum = newBill(app_st)


print("Electricity Price is", eb_sum)

# lower PAR is better
#par_val = ps_max / ps_avg

par_val = calculate_par(app_st)

# should be between 0 and 1
wtr_avg_val = wtr_calc(app_st)

nsas, pns = getnsa()
cpr_val = calc_cpr(app_st)
uc = uc_calculate(wtr_avg_val, cpr_val)
lastval = multiobjective(eb_sum, par_val, wtr_avg_val, cpr_val)
print("PAR value: ", par_val)
print("WTR Average time: ", wtr_avg_val)
print("CPR value is: ", cpr_val)
print("uc val is:", uc)
print("Multi-objective value is: ", lastval)
print(consumption_matrix)