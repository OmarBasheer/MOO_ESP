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
from psoe import PSOE

###
scenario = 5
###

num_sa = 36  # Number of appliances put to test
num_slots = 1440  # Number of time slots, 1 minute each, demonstrating a full day
all_sa = range(num_sa)
all_slots = range(num_slots)
remaining_slots = num_slots
loc, lb, ub, cost = getAppliances(scenario)
ps_max_list = np.zeros(1441)

consumption_per_min = []
final_consumption_list = np.zeros(1440)
c = 0.0333
# get price per minute list
price_per_min = getPricePerMin()

# randomize appliance within LB & (UB - l)
consumption_matrix = np.zeros((36, 1440))

consumption_per_min, app_st, app_et, bounds, consumption_matrix, positions = initialize(scenario)
## test multi objective ##
electricity = getBill(app_st, scenario)
a = getBill(app_st, scenario)
b = getPAR(app_st, scenario)

#k, best_params, error = PSOE(multiobjective, p_num=20, N=36, scale=0.1, w=1, r=0.99, c1=2, c2=2, a=a, b=b, eps=1e-5, lb=lb, ub=ub, loc=loc, early_stopping=100, max_iter=750, random_state=None)

#print(best_params)
#best_elect = getBill(best_params[len(best_params)-1])
#par = getPAR(best_params[len(best_params)-1])
#wtr = getWTR(best_params[len(best_params)-1])
#cpr = getCPR(best_params[len(best_params)-1])
#FF = objfun(best_params[len(best_params)-1], a, b)
#uc = getUC(wtr, cpr)
#print("best electricity", best_elect)
#print("best par", par)
#print("best WTR", wtr)
#print("best CPR", cpr)
#print("best UC", uc)
#print("Objective value= ", FF)

#fMin, bestX, Convergence_curve = ssa.SSA(10, lb, ub, loc, 750, 0.8, 0.2, 36, multiobjective)

#p = psoo.PSO(getBill, app_st, bounds=bounds, num_particles=20, maxiter=100)
#eb_sumssa = getBill(bestX)
#par_valssa = getPAR(bestX)
#wtr_avg_valssa = getWTR(app_st)
#cpr_valssa = getCPR(app_st)
#ucssa = getUC(wtr_avg_valssa, cpr_valssa)
#print("SSA Electricity Price: ", eb_sumssa)
#print("SSA PAR value: ", par_valssa)
#print("SSA WTR Average time: ", wtr_avg_valssa)
#print("SSA CPR value is: ", cpr_valssa)
#print("SSA uc val is:", ucssa)
#print("SSA Minimum obtained:", fMin)
problem_dict1 = {
         "fit_func": objfun,
         "lb": lb.tolist(),
         "ub": ub.tolist(),
         "minmax": "min",
         "loc": loc.tolist(),
         "a": a,
         "b": b
     }
epoch = 10
pop_size = 20
ST = 0.7
PD = 0.3
SD = 0.1
c1 = 2.05
c2 = 2.05
w_min = 0.4
w_max = 1

model = BaseSSA(problem_dict1, epoch, pop_size, ST, PD, SD, a, b)
best_position, best_fitness = model.solve()

model2 = BasePSO(problem_dict1, epoch, pop_size, c1, c2, w_min, w_max)
best_position2, best_fitness2 = model2.solve()

print(f"Solution: {best_position}, Fitness: {best_fitness}")
eb_sum1 = getBill(best_position, scenario)
par_val1 = getPAR(best_position)
wtr_avg_val1 = getWTR(best_position)
cpr_val1 = getCPR(best_position)
uc1 = getUC(wtr_avg_val1, cpr_val1)
lastval1 = multiobjective(eb_sum1, par_val1, wtr_avg_val1, cpr_val1, a, b)

print("SSA Electricity Price: ", eb_sum1)
print("SSA PAR value: ", par_val1)
print("SSA WTR Average time: ", wtr_avg_val1)
print(" SSA CPR value is: ", cpr_val1)
print("SSA uc val is:", uc1)
print("SSA Multi-objective value is: ", lastval1)
print(f"Solution: {best_position2}, Fitness: {best_fitness2}")

eb_sum2 = getBill(best_position2, 3)
par_val2 = getPAR(best_position2)
wtr_avg_val2 = getWTR(best_position2)
cpr_val2 = getCPR(best_position2)
uc2 = getUC(wtr_avg_val2, cpr_val2)
lastval2 = multiobjective(eb_sum2, par_val2, wtr_avg_val2, cpr_val2, a, b)

print("PSO Electricity Price: ", eb_sum2)
print("PSO PAR value: ", par_val2)
print("PSO WTR Average time: ", wtr_avg_val2)
print("PSO CPR value is: ", cpr_val2)
print("PSO uc val is:", uc2)
print("PSO Multi-objective value is: ", lastval2)



eb_sum = getBill(app_st,scenario)
par_val = getPAR(app_st)
wtr_avg_val = getWTR(app_st)
cpr_val = getCPR(app_st)
uc = getUC(wtr_avg_val, cpr_val)
lastval = objfun(app_st, a, b)
print("Electricity Price: ", eb_sum)
print("PAR value: ", par_val)
print("WTR Average time: ", wtr_avg_val)
print("CPR value is: ", cpr_val)
print("uc val is:", uc)
print("Multi-objective value is: ", lastval)
#print(consumption_matrix)