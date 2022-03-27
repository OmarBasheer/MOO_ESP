import numpy as np

def Average(lst):
    return sum(lst) / len(lst)

def getBill(x):
    total = 0
    loc, lb, ub, cost = getAppliances()
    price = getPricePerMin()
    for i in range(36):
        for j in range(x[i], x[i]+loc[i]):
            total += cost[i] * price[j]
    return total

def getAppliances():
    appliances = [  # [Appliance, LOC, OTPs, OTPe, power usage in kW]
        ['dw', 105, 540, 780, 1.5 / 60], ['dw', 105, 840, 1080, 1.5 / 60], ['dw', 105, 1200, 1440, 1.5 / 60],['ac', 30, 1, 120, 1.2 / 60], ['ac', 30, 120, 240, 1.2 / 60], ['ac', 30, 240, 360, 1.2 / 60], ['ac', 30, 360, 480, 1.2 / 60],
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
    lb = np.array([540, 840, 1200, 1, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 60, 300, 1, 1, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 300, 1100, 300, 1020, 1, 900])
    ub = np.array([780, 1080, 1440, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440, 300, 480, 1440, 120, 240, 360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440, 420, 1440, 450, 1140, 540, 1440])
    cost = np.array([1.5/60, 1.5/60, 1.5/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.2/60, 1.15/60, 5.4/60, 0.5/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 0.65/60, 4/60, 4/60, 1.5/60, 1.5/60, 1/60, 1/60])
    return loc, lb, ub, cost

def calculate_eb(appliances, price_per_min):
    eb_sum=0
    ps_list = []
    ps_min = []
    app_sum=0
    c = 0.0333
    l = 1.543
    for appliance in appliances:  # Loop through all appliances
        for minute in range(appliance[2]):  # Loop through durations of each appliance
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
    price_per_min = np.zeros(1442)
    price_per_min[0:61], price_per_min[61:121], price_per_min[121:181], price_per_min[
                                                                        181:241] = 1.7/60, 1.4/60, 1.1/60, 0.8/60
    price_per_min[241:301], price_per_min[301:361], price_per_min[361:421], price_per_min[
                                                                            421:481] = 0.9/60, 1.3/60, 1.5/60, 2.1/60
    price_per_min[481:541], price_per_min[541:601], price_per_min[601:661], price_per_min[
                                                                            661:721] = 2.4/60, 2.5/60, 2.7/60, 3/60
    price_per_min[721:781], price_per_min[781:841], price_per_min[841:901], price_per_min[
                                                                            901:961] = 3.1/60, 3.2/60, 3.3/60, 3.9/60
    price_per_min[961:1021], price_per_min[1021:1081], price_per_min[1081:1141], price_per_min[
                                                                                 1141:1201] = 4.1/60, 3.7/60, 3.2/60, 3.1/60
    price_per_min[1201:1261], price_per_min[1261:1321], price_per_min[1321:1381], price_per_min[
                                                                                  1381:1442] = 3/60, 2.8/60, 2.4/60, 1.9/60
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
def wtr_calc(lst):
    val1, val2 = 0, 0
    for appliance in lst:
        val1 += (appliance[1] - appliance[3])
        val2 += (appliance[4] - appliance[3] - appliance[2])
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


def uc_calculate(wtr, cpr):
    return (1 - (wtr + cpr / 2)) * 100

def multiobjective(eb, par, wtr, cpr):
    return 0.4 * (eb/eb+1) + 0.2 * (par/par+1) + 0.2 * wtr + 0.2 * cpr