from support_methods import *
import numpy as np
from mealpy.swarm_based.SSA import BaseSSA
from mealpy.swarm_based.PSO import BasePSO

###############
for x in range(1, 8):
    for i in range(1, 16):
        ###
        scenario = x
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

        a = getBill(app_st, scenario)
        b = getPAR(app_st, scenario)

        problem_dict1 = {
            "fit_func": multiobjective,
            "lb": lb.tolist(),
            "ub": ub.tolist(),
            "minmax": "min",
            "loc": loc.tolist(),
            "a": a,
            "b": b,
            "s": scenario
        }
        epoch = 5
        pop_size = 20
        ST = 0.8
        PD = 0.2
        SD = 0.1
        c1 = 2.05
        c2 = 2.05
        w_min = 0.4
        w_max = 1

        model = BaseSSA(problem_dict1, epoch, pop_size, ST, PD, SD, a=a, b=b, s=scenario)
        best_position, best_fitness = model.solve()

        model2 = BasePSO(problem_dict1, epoch, pop_size, c1, c2, w_min, w_max, a=a, b=b, s=scenario)
        best_position2, best_fitness2 = model2.solve()

        print("*" * 50)

        print(f"Solution: {best_position}, Fitness: {best_fitness}")
        eb_sumSSA = getBill(best_position, scenario)
        par_valSSA = getPAR(best_position, scenario)
        wtr_avg_valSSA = getWTR(best_position, scenario)
        cpr_valSSA = getCPR(best_position, scenario)
        ucSSA = getUC(wtr_avg_valSSA, cpr_valSSA)
        lastvalSSA = objfun(best_position, a, b, scenario)
        print("SSA Electricity Price: ", eb_sumSSA)
        print("SSA PAR value: ", par_valSSA)
        print("SSA WTR Average time: ", wtr_avg_valSSA)
        print("SSA CPR value is: ", cpr_valSSA)
        print("SSA uc val is:", ucSSA)
        print("SSA Multi-objective value is: ", lastvalSSA)

        print("*" * 50)
        print(f"Solution: {best_position2}, Fitness: {best_fitness2}")
        eb_sumPSO = getBill(best_position2, scenario)
        par_valPSO = getPAR(best_position2, scenario)
        wtr_avg_valPSO = getWTR(best_position2, scenario)
        cpr_valPSO = getCPR(best_position2, scenario)
        ucPSO = getUC(wtr_avg_valPSO, cpr_valPSO)
        lastvalPSO = objfun(best_position2, a, b, scenario)
        print("*" * 50)

        print("PSO Electricity Price: ", eb_sumPSO)
        print("PSO PAR value: ", par_valPSO)
        print("PSO WTR Average time: ", wtr_avg_valPSO)
        print("PSO CPR value is: ", cpr_valPSO)
        print("PSO uc val is:", ucPSO)
        print("PSO Multi-objective value is: ", lastvalPSO)
        print("*" * 50)

        eb_sum = getBill(app_st, scenario)
        par_val = getPAR(app_st, scenario)
        wtr_avg_val = getWTR(app_st, scenario)
        cpr_val = getCPR(app_st, scenario)
        uc = getUC(wtr_avg_val, cpr_val)
        lastval = objfun(app_st, a, b, scenario)
        print("initial random solution: ", app_st)
        print("Electricity Price: ", eb_sum)
        print("PAR value: ", par_val)
        print("WTR Average time: ", wtr_avg_val)
        print("CPR value is: ", cpr_val)
        print("uc val is:", uc)
        print("Multi-objective value is: ", lastval)
        print("*" * 50)
        with open("results.txt", "a") as file:
            content = ["\n \n Run #: ", str(i),
                       "\n Scenario #: ", str(scenario),
                       "\n Initial solution", str(app_st),
                       "\n Electricity Price: ", str(eb_sum),
                       "\n PAR: ", str(par_val),
                       "\n WTR avg: ", str(wtr_avg_val),
                       "\n CPR value: ", str(cpr_val),
                       "\n UC value: ", str(uc),
                       "\n multi-objective value: ", str(lastval),
                       "\n ***************************************",
                       "\n SSA Initial solution", str(best_position),
                       "\n SSA Electricity Price: ", str(eb_sumSSA),
                       "\n SSA PAR: ", str(par_valSSA),
                       "\n SSA WTR avg: ", str(wtr_avg_valSSA),
                       "\n SSA CPR value: ", str(cpr_valSSA),
                       "\n SSA UC value: ", str(ucSSA),
                       "\n SSA multi-objective value: ", str(lastvalSSA),
                       "\n ***************************************",
                       "\n PSO Initial solution", str(best_position2),
                       "\n PSO Electricity Price: ", str(eb_sumPSO),
                       "\n PSO PAR: ", str(par_valPSO),
                       "\n PSO WTR avg: ", str(wtr_avg_valPSO),
                       "\n PSO CPR value: ", str(cpr_valPSO),
                       "\n PSO UC value: ", str(ucPSO),
                       "\n PSO multi-objective value: ", str(lastvalPSO)]
            file.writelines(content)
            file.close()

