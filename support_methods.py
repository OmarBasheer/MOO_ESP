from __future__ import division

from random import randint

import numpy as np

import main


def Average(lst):
    return sum(lst) / len(lst)

def initialize():
    sa_num = range(36)
    loc, lb, ub, cost = get_appliances()
    price_per_min = getPricePerMin()
    positions = []
    app_st = []
    app_et = []
    bounds = []
    consumption_per_min = np.zeros(1440)
    consumption_matrix = np.zeros((36, 1440))
    for x in sa_num:
        bounds.append((lb[x], ub[x]))
        if ub[x] - loc[x] < lb[x]:
            slotter = 0
        else:
            slotter = randint(lb[x], ub[x] - loc[x])
        positions.append(
            [x, slotter, loc[x], lb[x], ub[x], cost[x]])  # [Appliance #, starting slot, lower bound, upper bound]
        app_st.append(slotter)
        app_et.append(slotter + loc[x])
        for mint in range(slotter, slotter + loc[x]):
            consumption_matrix[x][mint] = cost[x]
            consumption_per_min[mint] += cost[x]
    return consumption_per_min, app_st, app_et, bounds, consumption_matrix, positions

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

def newBill(app_st):
    c = 0.0333
    l = 1.543
    loc, lb, ub, ps = get_appliances()
    consumption_per_min = np.zeros(1440)
    price = getPricePerMin()
    total_cost = 0
    for x in range(36): #0-35
        test = np.rint(app_st[x]).astype("int32")
        for y in range(test, test+loc[x]): #appliance start time -> starttime+LOC
            consumption_per_min[y] += ps[x]
    for i in range(len(consumption_per_min)): #loop from 0 - 1439
        if consumption_per_min[i] > c:
            total_cost += price[i] * consumption_per_min[i] * l
        else:
            total_cost += price[i] * consumption_per_min[i]
    return total_cost

def getConsumptionMatrix(app_st):
    consumption_matrix = np.zeros((36, 1440))
    consumption_per_min = np.zeros(1440)
    loc, lb, ub, cost = get_appliances()
    price = getPricePerMin()
    for x in range(36):
        for j in range(round(app_st[x]), round(app_st[x])+loc[x]):
            consumption_matrix[x][j] = cost[x]
            consumption_per_min[j] = cost[x]
    return consumption_matrix, consumption_per_min

def get_appliances():
    loc = np.array([105, 105, 105, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 55, 60, 1440, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 35, 35, 10, 10, 180, 180])
    lb = np.array([539, 839, 1199, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 59, 299, 0, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 299, 1099, 299, 1019, 0, 899])
    ub = np.array([779, 1079, 1439, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 299, 479, 1439, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 419, 1439, 449, 1139, 539, 1439])
    #ps = np.array([1.5/60, 1.5/60, 1.5/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.15/60, 5.4/60, 0.5/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 4/60, 4/60, 1.5/60, 1.5/60, 1/60, 1/60])
    ps2 = np.array([0.6/60, 0.6/60, 0.6/60, 1/60, 1/60, 1/60, 1/60, 1/60, 1/60, 1/60, 1/60, 1/60, 1/60, 1/60, 1/60, 0.38/60, 0.8/60, 0.5/60, 0.05/60, 0.05/60, 0.05/60, 0.05/60, 0.05/60, 0.05/60, 0.05/60, 0.05/60, 0.05/60, 0.05/60, 0.05/60, 0.05/60, 1.5/60, 1.5/60, 0.8/60, 0.8/60, 0.54/60, 0.54/60])
    return loc, lb, ub, ps2



def getnsa():
    ns = ['light','afan', 'tfan','iron','toaser', 'ccharger',
           'cleaner', 'tv', 'hairdryer', 'hand drill', 'water pump',
           'blender', 'microwave', 'e vehicle']
    pns = np.array([0.6/60, 0.3/60, 0.8/60, 1.5/60, 2/60, 1.5/60, 1.5/60, 1.5/60, 0.3/60, 1.2/60, 0.6/60, 2.5/60, 0.3/60, 1.18/60, 1/60])
    return ns, pns


def getPricePerMin():
    price_per_min = np.zeros(1440)
    price_per_min[0:60], price_per_min[60:120], price_per_min[120:180], price_per_min[
                                                                        180:240] = 1.7, 1.4, 1.1, 0.8
    price_per_min[240:300], price_per_min[300:360], price_per_min[360:420], price_per_min[
                                                                            420:480] = 0.9, 1.3, 1.5, 2.1
    price_per_min[480:540], price_per_min[540:600], price_per_min[600:660], price_per_min[
                                                                            660:720] = 2.4, 2.5, 2.7, 3
    price_per_min[720:780], price_per_min[780:840], price_per_min[840:899], price_per_min[
                                                                            900:959] = 3.1, 3.2, 3.3, 3.9
    price_per_min[960:1020], price_per_min[1020:1080], price_per_min[1080:1140], price_per_min[
                                                                                 1140:1200] = 4.1, 3.7, 3.2, 3.1
    price_per_min[1200:1260], price_per_min[1260:1320], price_per_min[1320:1380], price_per_min[
                                                                                  1380:1440] = 3, 2.8, 2.4, 1.9
    return price_per_min


# Electricity bill = sum of power required for appliance * power consumption profile tariff at that slot of time PC =
# a if  0 <= ps <= C || h if ps > C where C is consumption threshold between a & h, lambda positive ratio between 2
#
# tariffs h = lambda * a C = 0.0333 per time slot, lambda = 1.543 ps = {} pc = {} EB = sum(ps*pc)


# calculate wtr average as per the equation


def wtr_calc(app_st):
    val1, val2 = 0, 0
    loc, lb, ub, cost = get_appliances()
    for x in range(36):
        val1 += (app_st[x] - lb[x])
        val2 += (ub[x] - lb[x] - loc[x])
    return val1 / val2



## fixed
def calc_cpr(app_st):
    nsa, pns = getnsa()
    c = 0.0333
    q = len(nsa)
    n = 1440
    l = 1.543
    loc, lb, ub, cost = get_appliances()
    consumption_per_min = np.zeros(1440)
    price = getPricePerMin()
    total_cpr = 0
    for x in range(36):
        test = np.rint(app_st[x]).astype("int32")
        for y in range(test, test+loc[x]):
            consumption_per_min[y] += cost[x]
    for i in range(len(consumption_per_min)):
        for p in pns:
            if not p < (c-consumption_per_min[i]):
                total_cpr += 1
    return total_cpr / (q*n)

def getconsumptionpermin():
    main.consumption_mins.sort()
    return main.consumption_per_min

def uc_calculate(wtr, cpr):
    return (1 - (wtr + cpr / 2)) * 100


def calculate_par(app_st):
    c = 0.0333
    l = 1.543
    loc, lb, ub, cost = get_appliances()
    consumption_per_min = np.zeros(1440)
    price = getPricePerMin()
    total_cost = 0
    for x in range(36):
        test = np.rint(app_st[x]).astype("int32")
        for y in range(test, test+loc[x]):
            consumption_per_min[y] += cost[x]
    ps_max = np.max(consumption_per_min)
    ps_avg = Average(consumption_per_min)
    return ps_max/ps_avg


def multiobjective(eb, par, wtr, cpr):
    return 0.4 * (eb/eb+1) + 0.2 * (par/par+1) + 0.2 * wtr + 0.2 * cpr # cost for the initial solution are a & b

def objfun(eb, par, wtr, cpr, a,b):
    return 0.4 * (eb/eb+a) + 0.2 * (par/par+b) + 0.2 * wtr + 0.2 * cpr

def position_initalize(lb, ub, loc):
    positions = np.zeros(len(lb))
    for x in range(len(lb)):
        positions[x] = np.random.randint(lb[x], abs(ub[x]-loc[x]))
    return positions
