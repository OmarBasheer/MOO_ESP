import numpy as np

import main


def Average(lst):
    return sum(lst) / len(lst)


def getBill(x):
    c = 0.0333
    l = 1.543
    app_sum, total = 0, 0
    loc, lb, ub, cost = get_appliances()
    price = getPricePerMin()
    for i in range(len(x)):
        temp = round(x[i])
        appliance_length = temp + loc[i] - x[i]
        if appliance_length > ub[i]:
            appliance_length -= 1
        for j in range(appliance_length+1):
            if cost[i] > c:
                app_sum += (cost[i] * price[temp+j] * l)
            else:
                app_sum += (cost[i] * price[temp+j])
        total += app_sum

    return total


def get_appliances():
    appliances = [  # [Appliance, LOC, OTPs, OTPe, power usage in kW]
        ['dw', 105, 540, 780, 1.5 / 60], ['dw', 105, 840, 1080, 1.5 / 60], ['dw', 105, 1200, 1440, 1.5 / 60], ['ac', 30, 1, 120, 1.2 / 60], ['ac', 30, 120, 240, 1.2 / 60], ['ac', 30, 240, 360, 1.2 / 60], ['ac', 30, 360, 480, 1.2 / 60],
        ['ac', 30, 480, 600, 1.2 / 60],
        ['ac', 30, 600, 720, 1.2 / 60], ['ac', 30, 720, 840, 1.2 / 60], ['ac', 30, 840, 960, 1.2 / 60],
        ['ac', 30, 960, 1080, 1.2 / 60],
        ['ac', 30, 1080, 1200, 1.2 / 60], ['ac', 30, 1200, 1320, 1.2 / 60], ['ac', 30, 1320, 1440, 1.2 / 60],
        ['wm', 55, 60, 300, 1.15 / 60],
        ['cd', 60, 300, 480, 5.4 / 60], ['ref', 1440, 0, 1439, 0.5 / 60], ['deh', 30, 1, 120, 0.65 / 60],
        ['deh', 30, 120, 240, 0.65 / 60],
        ['deh', 30, 240, 360, 0.65 / 60], ['deh', 30, 360, 480, 0.65 / 60], ['deh', 30, 480, 600, 0.65 / 60],
        ['deh', 30, 600, 720, 0.65 / 60],
        ['deh', 30, 720, 840, 0.65 / 60], ['deh', 30, 840, 960, 0.65 / 60], ['deh', 30, 960, 1080, 0.65 / 60],
        ['deh', 30, 1080, 1200, 0.65 / 60],
        ['deh', 30, 1200, 1320, 0.65 / 60], ['deh', 30, 1320, 1440, 0.65 / 60], ['ewh', 35, 300, 420, 4 / 60],
        ['ewh', 35, 1100, 1440, 4 / 60],
        ['cm', 10, 300, 450, 1.5 / 60], ['cm', 10, 1020, 1140, 1.5 / 60], ['pf', 180, 1, 540, 1 / 60],
        ['pf', 180, 900, 1440, 1 / 60]]
    loc = np.array([105, 105, 105, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 55, 60, 1440, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 35, 35, 10, 10, 180, 180])
    lb = np.array([539, 839, 1199, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 59, 299, 0, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 299, 1099, 299, 1019, 0, 899])
    ub = np.array([779, 1079, 1439, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 299, 479, 1439, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 419, 1439, 449, 1139, 539, 1439])
    cost = np.array([1.5/60, 1.5/60, 1.5/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.15/60, 5.4/60, 0.5/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 4/60, 4/60, 1.5/60, 1.5/60, 1/60, 1/60])
    return loc, lb, ub, cost


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


def getnsa():
    ns = ['light','afan', 'tfan','iron','toaser', 'ccharger',
           'cleaner', 'tv', 'hairdryer', 'hand drill', 'water pump',
           'blender', 'microwave', 'e vehicle']
    pns = np.array([0.6/60, 0.3/60, 0.8/60, 1.5/60, 2/60, 1.5/60, 1.5/60, 1.5/60, 0.3/60, 1.2/60, 0.6/60, 2.5/60, 0.3/60, 1.18/60, 1/60])
    return ns, pns


def getPricePerMin():
    price_per_min = np.zeros(1440)
    price_per_min[0:60], price_per_min[61:120], price_per_min[121:180], price_per_min[
                                                                        181:240] = 1.7/60, 1.4/60, 1.1/60, 0.8/60
    price_per_min[241:300], price_per_min[301:360], price_per_min[361:420], price_per_min[
                                                                            421:480] = 0.9/60, 1.3/60, 1.5/60, 2.1/60
    price_per_min[481:540], price_per_min[541:600], price_per_min[601:660], price_per_min[
                                                                            661:720] = 2.4/60, 2.5/60, 2.7/60, 3/60
    price_per_min[721:780], price_per_min[781:840], price_per_min[841:899], price_per_min[
                                                                            901:959] = 3.1/60, 3.2/60, 3.3/60, 3.9/60
    price_per_min[961:1020], price_per_min[1021:1080], price_per_min[1081:1140], price_per_min[
                                                                                 1141:1200] = 4.1/60, 3.7/60, 3.2/60, 3.1/60
    price_per_min[1201:1260], price_per_min[1261:1320], price_per_min[1321:1380], price_per_min[
                                                                                  1381:1439] = 3/60, 2.8/60, 2.4/60, 1.9/60
    return price_per_min


# Electricity bill = sum of power required for appliance * power consumption profile tariff at that slot of time PC =
# a if  0 <= ps <= C || h if ps > C where C is consumption threshold between a & h, lambda positive ratio between 2
#
# tariffs h = lambda * a C = 0.0333 per time slot, lambda = 1.543 ps = {} pc = {} EB = sum(ps*pc)

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

# calculate wtr average as per the equation


def wtr_calc(st):
    val1, val2 = 0, 0
    loc, lb, ub, cost = get_appliances()
    for x in range(36):
        val1 += (st[0][x] - lb[x])
        val2 += (ub[x] - lb[x] - loc[x])
    return val1 / val2


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


def calc_cpr(st):
    nsa, pns = getnsa()
    total_cpr = 0
    cpr_per_minute = np.zeros(1440)
    c = 0.0333
    q = len(st)
    n = 1440
    loc, lb, ub, cost = get_appliances()
    consumption = getconsumptionpermin()
    for x in consumption:
        for p in pns:
            if not p < (c-x[1]):
                total_cpr += 1
    return total_cpr / (q*n)

def getconsumptionpermin():
    main.consumption_mins.sort()
    return main.consumption_per_min

def uc_calculate(wtr, cpr):
    return (1 - (wtr + cpr / 2)) * 100


def calculate_par(st):
    ps_max = main.ps_max_list[np.argmax(main.ps_max_list)]
    ps_avg = Average(main.ps_max_list)
    return ps_max/ps_avg


def multiobjective(eb, par, wtr, cpr):
    return 0.4 * (eb/eb+1) + 0.2 * (par/par+1) + 0.2 * wtr + 0.2 * cpr # cost for the initial solution are a & b