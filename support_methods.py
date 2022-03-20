import numpy as np

def Average(lst):
    return sum(lst) / len(lst)


def getAppliances():
    appliances = [  # [Appliance, LOC, OTPs, OTPe, power usage in kW]
        ['dw', 105, 540, 780, 1.5 / 60], ['dw', 105, 840, 1080, 1.5 / 60], ['dw', 105, 1200, 1440, 1.5 / 60],
        ['ac', 30, 1, 120, 1.2 / 60],
        ['ac', 30, 120, 240, 1.2 / 60], ['ac', 30, 240, 360, 1.2 / 60], ['ac', 30, 360, 480, 1.2 / 60],
        ['ac', 30, 480, 600, 1.2 / 60],
        ['ac', 30, 600, 720, 1.2 / 60], ['ac', 30, 720, 840, 1.2 / 60], ['ac', 30, 840, 960, 1.2 / 60],
        ['ac', 30, 960, 1080, 1.2 / 60],
        ['ac', 30, 1080, 1200, 1.2 / 60], ['ac', 30, 1200, 1320, 1.2 / 60], ['ac', 30, 1320, 1440, 1.2 / 60],
        ['wm', 55, 60, 300, 1.15 / 60],
        ['cd', 60, 300, 480, 5.4 / 60], ['ref', 1440, 0, 1440, 0.5 / 60], ['deh', 30, 1, 120, 0.65 / 60],
        ['deh', 30, 120, 240, 0.65 / 60],
        ['deh', 30, 240, 360, 0.65 / 60], ['deh', 30, 360, 480, 0.65 / 60], ['deh', 30, 480, 600, 0.65 / 60],
        ['deh', 30, 600, 720, 0.65 / 60],
        ['deh', 30, 720, 840, 0.65 / 60], ['deh', 30, 840, 960, 0.65 / 60], ['deh', 30, 960, 1080, 0.65 / 60],
        ['deh', 30, 1080, 1200, 0.65 / 60],
        ['deh', 30, 1200, 1320, 0.65 / 60], ['deh', 30, 1320, 1440, 0.65 / 60], ['ewh', 35, 300, 420, 4 / 60],
        ['ewh', 35, 1100, 1440, 4 / 60],
        ['cm', 10, 300, 450, 1.5 / 60], ['cm', 10, 1020, 1140, 1.5 / 60], ['pf', 180, 1, 540, 1 / 60],
        ['pf', 180, 900, 1440, 1 / 60]]
    return appliances


def getnsa():
    nsa = [['light', 0.6/60],['afan', 0.3/60], ['tfan', 0.8/60], ['iron', 1.5/60], ['toaser', 1/60], ['ccharger', 1.5/60],
           ['cleaner', 1.5/60], ['tv', 0.3/60], ['hairdryer', 1.2/60], ['hand drill', 0.6/60], ['water pump', 2.5/60],
           ['blender', 0.3/60], ['microwave', 1.18/60], ['e vehicle', 1/60]]
    return nsa


def getPricePerMin():
    price_per_min = np.zeros(1440)
    price_per_min[0:61], price_per_min[61:121], price_per_min[121:181], price_per_min[
                                                                        181:241] = 0.028, 0.023, 0.018, 0.013
    price_per_min[241:301], price_per_min[301:361], price_per_min[361:421], price_per_min[
                                                                            421:481] = 0.015, 0.022, 0.025, 0.054
    price_per_min[481:541], price_per_min[541:601], price_per_min[601:661], price_per_min[
                                                                            661:721] = 0.062, 0.065, 0.069, 0.077
    price_per_min[721:781], price_per_min[781:841], price_per_min[841:901], price_per_min[
                                                                            901:961] = 0.08, 0.082, 0.085, 0.1
    price_per_min[961:1021], price_per_min[1021:1081], price_per_min[1081:1141], price_per_min[
                                                                                 1141:1201] = 0.105, 0.096, 0.082, 0.08
    price_per_min[1201:1261], price_per_min[1261:1321], price_per_min[1321:1381], price_per_min[
                                                                                  1381:1440] = 0.077, 0.073, 0.062, 0.032
    return price_per_min


# Electricity bill = sum of power required for appliance * power consumption profile tariff at that slot of time PC =
# a if  0 <= ps <= C || h if ps > C where C is consumption threshold between a & h, lambda positive ratio between 2
#
# tariffs h = lambda * a C = 0.0333 per time slot, lambda = 1.543 ps = {} pc = {} EB = sum(ps*pc)

def price_calculate(min, power_consumption, ps_per_min, ps_min, price_per_min):
    sum_cost = price_per_min[min] * power_consumption
    ps_per_min.append(power_consumption)
    ps_min.append(min)
    return sum_cost, ps_per_min, ps_min

# calculate wtr average as per the equation
def wtr_calc(lst):
    val1, val2 = 0, 0
    for appliance in lst:
        val1 = val1 + (appliance[1] - appliance[2][2])
        val2 = val2 + (appliance[2][3] - appliance[2][2] - appliance[2][1])
    return val1 / val2

# calculate CPR, get power consumption at all minutes & calculate accordingly
def cpr_calc(ps_list, nsas):
    total_cpr = 0
    c = 0.0333
    q = len(nsas)
    n = 1440
    for x in ps_list:
        for nsa in nsas:
            if not nsa[1] < (c-x):
                total_cpr = total_cpr + 1
    return total_cpr / (q*n)


def uc_calculate(wtr, cpr):
    return (1 - (wtr + cpr / 2)) * 100

