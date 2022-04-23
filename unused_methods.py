def calculate_eb(appliances, price_per_min):
    eb_sum=0
    ps_list = []
    ps_min = []
    app_sum = 0
    c = 0.0333
    l = 1.543
    for appliance in appliances:  # Loop through all appliances
        for minute in range(appliance[2]+1):  # Loop through durations of each appliance
            if appliance[5] > c:
                app_sum = app_sum + ((price_per_min[appliance[1] + minute] * l) * appliance[5])
            else:
                app_sum = app_sum + (price_per_min[appliance[1] + minute] * appliance[5])
        eb_sum += app_sum
    return eb_sum


def price_calculate(min, power_consumption, ps_per_min, ps_min, price_per_min):
    c = 0.0333
    l = 1.543
    if power_consumption > c:
        sum_cost = price_per_min[min] * 1.543
    else:
        sum_cost = price_per_min[min] * power_consumption
    ps_per_min.append(power_consumption)
    ps_min.append(min)
    return sum_cost, ps_per_min, ps_min


def newBill(cons_matrix):
    c = 0.0333
    l = 1.543
    consumption_per_min = np.zeros(1440)
    loc, lb, ub, cost = get_appliances()
    price = getPricePerMin()
    total_cost = 0
    for i in range(1440):
        slot_total_cost = 0
        for y in range(36):
            if cons_matrix[y][i] == 1:
                if slot_total_cost <= c:
                    slot_total_cost += cost[y] * price[i]
                    consumption_per_min[i] += cost[y]
                else:
                    slot_total_cost += cost[y] * price[i] * l
                    consumption_per_min[i] += cost[y]
        total_cost += slot_total_cost
    return total_cost


# calculate CPR, get power consumption at all minutes & calculate accordingly
def cpr_calc(ps_list, nsas):
    total_cpr = 0
    c = 0.0333
    q = len(nsas)
    n = 1440
    for x in ps_list:
        for nsa in nsas:
            if not nsa < (c-x):
                total_cpr += 1
    return total_cpr / (q*n)

## old getBill, gets 200$
def getBill(x):
    c = 0.0333
    l = 1.543
    app_sum, total = 0, 0
    loc, lb, ub, cost = get_appliances()
    price = getPricePerMin()
    for i in range(len(x)):
        temp = round(x[i])
        appliance_length = loc[i]
        if appliance_length > ub[i]:
            appliance_length -= 1
        for j in range(appliance_length+1):
            if cost[i] > c:
                if not temp+j >= 1440:
                    app_sum += (cost[i] * price[temp+j] * l)
                else:
                    app_sum += (cost[i] * price[1439] * l)
            else:
                app_sum += (cost[i] * price[temp])

        total += app_sum
    return total

def getBill(x):
    c = 0.0333
    l = 1.543
    app_sum, total = 0, 0
    loc, lb, ub, cost = get_appliances()
    price = getPricePerMin()
    for i in range(len(x)):
        temp = round(x[i])
        appliance_length = loc[i]
        if appliance_length > ub[i]:
            appliance_length -= 1
        for j in range(appliance_length+1):
            if cost[i] > c:
                if not temp+j >= 1440:
                    app_sum += (cost[i] * price[temp+j] * l)
                else:
                    app_sum += (cost[i] * price[1439] * l)
            else:
                app_sum += (cost[i] * price[temp])
        total += app_sum
    return total


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

def getconsumptionpermin():
    main.consumption_mins.sort()
    return main.consumption_per_min