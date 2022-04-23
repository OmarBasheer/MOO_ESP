from __future__ import division

from random import randint

import numpy as np

import main


def Average(lst):
    return sum(lst) / len(lst)

def initialize(s=None):
    loc, lb, ub, cost = getAppliances(s)
    price_per_min = getPricePerMin(s)
    sa_num = range(len(lb))
    positions = []
    app_st = []
    app_et = []
    bounds = []
    consumption_per_min = np.zeros(1440)
    consumption_matrix = np.zeros((len(lb), 1440))
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


def getBill(app_st, s=None):
    c = 0.0333
    l = 1.543
    loc, lb, ub, ps = getAppliances(s)
    consumption_per_min = np.zeros(1440)
    price = getPricePerMin(s)
    total_cost = 0
    for x in range(len(lb)): #0-35
        test = np.rint(app_st[x]).astype(int)
        for y in range(test, test+loc[x]): # appliance start time -> start time+LOC
            consumption_per_min[y] += ps[x]
    for i in range(len(consumption_per_min)): # loop from 0 - 1439
        if consumption_per_min[i] > c:
            total_cost += (price[i] * consumption_per_min[i] * l)
        else:
            total_cost += (price[i] * consumption_per_min[i])
    return total_cost



def getAppliances(s=None):
    if s==None:
        loc = np.array([105, 105, 105, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 55, 60, 10, 10, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 35, 35, 180, 180, 1440])
        lb = np.array([539, 839, 1199, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 59, 299, 299, 1019, 0, 120, 240, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 299, 1099, 0, 899, 0])
        ub = np.array([779, 1079, 1439, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 299, 479, 959, 1079, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 419, 1439, 539, 1439, 1439])
        ps = np.array([0.01, 0.01, 0.01, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166,
                       0.0166, 0.0166, 0.0063, 0.0133, 0.0133, 0.0133, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833,
                       0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.025, 0.025, 0.009, 0.009,
                       0.008])
    elif s==1:
        loc = np.array(
            [105, 105, 30, 30, 30, 30, 30, 10, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 35, 180, 1440])
        lb = np.array(
            [539, 1199, 0, 119, 239, 359, 1319, 299, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 299,
             0, 0])
        ub = np.array(
            [779, 1439, 119, 239, 359, 479, 1439, 449, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439,
             419, 539, 1439])
        ps = np.array([0.01, 0.01, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0133, 0.000833, 0.000833, 0.000833,
                       0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.025,
                       0.009, 0.008])
    elif s==2:
        loc = np.array([105, 105, 30, 30, 30, 30, 30, 30, 30, 10, 10, 30, 30, 30, 30, 30, 35, 35, 180, 1440])
        lb = np.array(
            [539, 839, 0, 119, 239, 359, 719, 839, 959, 299, 1019, 719, 839, 959, 1079, 1199, 299, 1099, 899, 0])
        ub = np.array(
            [779, 1079, 119, 239, 359, 479, 839, 959, 1079, 449, 1139, 839, 959, 1079, 1199, 1319, 419, 1439, 1439,
             1439])
        ps = np.array([0.01, 0.01, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0133, 0.0133, 0.000833,
                       0.000833, 0.000833, 0.000833, 0.000833, 0.025, 0.025, 0.009, 0.008])
    elif s==3:
        loc = np.array(
            [105, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 10, 10, 30, 30, 30, 30, 30, 30, 35, 35, 180, 1440])
        lb = np.array(
            [1199, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 299, 1019, 479, 599, 719, 839, 959, 1079,
             299, 1099, 0, 0])
        ub = np.array(
            [1439, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 959, 1079, 599, 719, 839, 959, 1079,
             1199, 419, 1439, 539, 1439])
        ps = np.array([0.01, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166,
                       0.0166, 0.0133, 0.0133, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.025, 0.025,
                       0.009, 0.008])
    elif s==4:
        loc = np.array([105, 105, 105, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 55, 60, 10, 10, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 35, 35, 180, 180, 1440])
        lb = np.array([539, 839, 1199, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 59, 299, 299, 1019, 0, 120, 240, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 299, 1099, 0, 899, 0])
        ub = np.array([779, 1079, 1439, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 299, 479, 959, 1079, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 419, 1439, 539, 1439, 1439])
        ps = np.array([0.01, 0.01, 0.01, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166,
                       0.0166, 0.0166, 0.0063, 0.0133, 0.0133, 0.0133, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833,
                       0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.025, 0.025, 0.009, 0.009,
                       0.008])
    elif s==5:
        loc = np.array(
            [105, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 10, 10, 30, 30, 30, 30, 30, 30, 35, 35, 180, 1440])
        lb = np.array(
            [1199, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 299, 1019, 479, 599, 719, 839, 959, 1079,
             299, 1099, 0, 0])
        ub = np.array(
            [1439, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 959, 1079, 599, 719, 839, 959, 1079,
             1199, 419, 1439, 539, 1439])
        ps = np.array([0.01, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166,
                       0.0166, 0.0133, 0.0133, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.025, 0.025,
                       0.009, 0.008])
    elif s==6:
        loc = np.array(
            [105, 105, 105, 30, 30, 30, 30, 30, 10, 10, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 35, 180, 1440])
        lb = np.array(
            [539, 839, 1199, 479, 599, 719, 839, 959, 299, 1019, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199,
             1319, 299, 0, 0])
        ub = np.array(
            [779, 1079, 1439, 599, 719, 839, 959, 1079, 449, 1079, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199,
             1319, 1439, 419, 539, 1439])
        ps = np.array([0.01, 0.01, 0.01, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0133, 0.0133, 0.000833, 0.000833,
                       0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833,
                       0.000833, 0.025, 0.009, 0.008])
    elif s==7:
        loc = np.array(
            [105, 105, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 55, 60, 10, 10, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
             30, 30, 35, 180, 180, 1440])
        lb = np.array(
            [539, 1199, 0, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 59, 299, 299, 1019, 0, 119,239, 359, 479,
             599, 719, 839, 959, 1079, 1199, 1319, 299, 0, 899, 0])
        ub = np.array(
            [779, 1439, 119, 239, 359, 479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 299, 479, 959, 1079, 119, 239, 359,
             479, 599, 719, 839, 959, 1079, 1199, 1319, 1439, 419, 539, 1439, 1439])
        ps = np.array([0.01, 0.01, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166, 0.0166,
                       0.0166, 0.0166, 0.0063, 0.0133, 0.0133, 0.0133, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833,
                       0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.000833, 0.025, 0.009, 0.009,
                       0.008])
    return loc, lb, ub, ps


def getnsa():
    ns = ['light','afan', 'tfan','iron','toaser', 'ccharger',
           'cleaner', 'tv', 'hairdryer', 'hand drill', 'water pump',
           'blender', 'microwave', 'e vehicle']
    pns = np.array([0.01, 0.005, 0.0133, 0.025, 0.0160, 0.025, 0.025, 0.005, 0.02, 0.01, 0.041, 0.005, 0.019, 0.0166])
    return ns, pns


def getPricePerMin(s=None):
    p = np.zeros(1440)
    if s == None:
        p[0:60], p[60:120], p[120:180], p[180:240] = 1.8, 1.4, 1.2, 0.8
        p[240:300], p[300:360], p[360:420], p[420:480] = 0.6, 0.5, 0.4, 1.3
        p[480:540], p[540:600], p[600:660], p[660:720] = 1.8, 2.2, 2.4, 2.6
        p[720:780], p[780:840], p[840:899], p[900:959] = 2.7, 2.9, 2.9, 3
        p[960:1020], p[1020:1080], p[1080:1140], p[1140:1200] = 3, 3, 2.8, 2.6
        p[1200:1260], p[1260:1320], p[1320:1380], p[1380:1440] = 2.7, 2.7, 2.3, 2
    elif s == 1:
        p[0:60], p[60:120], p[120:180], p[180:240] = 1.7, 1.4, 1.1, 0.8
        p[240:300], p[300:360], p[360:420], p[420:480] = 0.9, 1.3, 1.5, 2.1
        p[480:540], p[540:600], p[600:660], p[660:720] = 2.4, 2.5, 2.7, 3
        p[720:780], p[780:840], p[840:899], p[900:959] = 3.1, 3.2, 3.3, 3.9
        p[960:1020], p[1020:1080], p[1080:1140], p[1140:1200] = 4.1, 3.7, 3.2, 3.1
        p[1200:1260], p[1260:1320], p[1320:1380], p[1380:1440] = 3, 2.8, 2.4, 1.9
    elif s == 2:
        p[0:60], p[60:120], p[120:180], p[180:240] = 2, 1.8, 1.6, 1.4
        p[240:300], p[300:360], p[360:420], p[420:480] = 1.5, 1.9, 2.1, 2.5
        p[480:540], p[540:600], p[600:660], p[660:720] = 2.6, 2.8, 3, 3.2
        p[720:780], p[780:840], p[840:899], p[900:959] = 3.2, 3.5, 3.5, 4.2
        p[960:1020], p[1020:1080], p[1080:1140], p[1140:1200] = 4.3, 3.7, 3.3, 3.1
        p[1200:1260], p[1260:1320], p[1320:1380], p[1380:1440] = 3.1, 2.9, 2.5, 2
    elif s == 3:
        p[0:60], p[60:120], p[120:180], p[180:240] = 2, 1.8, 1.6, 1.5
        p[240:300], p[300:360], p[360:420], p[420:480] = 1.6, 1.9, 2.1, 2.4
        p[480:540], p[540:600], p[600:660], p[660:720] = 2.6, 2.9, 3.2, 3.3
        p[720:780], p[780:840], p[840:899], p[900:959] = 3.6, 4.2, 4.5, 4.7
        p[960:1020], p[1020:1080], p[1080:1140], p[1140:1200] = 4.5, 4.1, 3.6, 3.2
        p[1200:1260], p[1260:1320], p[1320:1380], p[1380:1440] = 3.1, 3, 2.5, 2
    elif s == 4:
        p[0:60], p[60:120], p[120:180], p[180:240] = 1.8, 1.4, 1.2, 0.8
        p[240:300], p[300:360], p[360:420], p[420:480] = 0.6, 0.5, 0.4, 1.3
        p[480:540], p[540:600], p[600:660], p[660:720] = 1.8, 2.2, 2.4, 2.6
        p[720:780], p[780:840], p[840:899], p[900:959] = 2.7, 2.9, 2.9, 3
        p[960:1020], p[1020:1080], p[1080:1140], p[1140:1200] = 3, 3, 2.8, 2.6
        p[1200:1260], p[1260:1320], p[1320:1380], p[1380:1440] = 2.7, 2.7, 2.3, 2
    elif s == 5:
        p[0:60], p[60:120], p[120:180], p[180:240] = 1.8, 1.7, 1.5, 1.3
        p[240:300], p[300:360], p[360:420], p[420:480] = 1.2, 1.1, 0.8, 1.6
        p[480:540], p[540:600], p[600:660], p[660:720] = 1.9, 2.1, 2.3, 2.3
        p[720:780], p[780:840], p[840:899], p[900:959] = 2.3, 2.4, 2.4, 2.4
        p[960:1020], p[1020:1080], p[1080:1140], p[1140:1200] = 2.4, 2.5, 2.4, 2.4
        p[1200:1260], p[1260:1320], p[1320:1380], p[1380:1440] = 2.5, 2.5, 2.1, 1.9
    elif s == 6:
        p[0:60], p[60:120], p[120:180], p[180:240] = 1.5, 1.5, 1.3, 1.1
        p[240:300], p[300:360], p[360:420], p[420:480] = 1.3, 1.5, 1.8, 2.2
        p[480:540], p[540:600], p[600:660], p[660:720] = 2.2, 2.6, 2.8, 3
        p[720:780], p[780:840], p[840:899], p[900:959] = 3.1, 3, 3.1, 3.2
        p[960:1020], p[1020:1080], p[1080:1140], p[1140:1200] = 3.3, 3.7, 2.9, 2.9
        p[1200:1260], p[1260:1320], p[1320:1380], p[1380:1440] = 2.9, 3, 2.3, 2
    elif s == 7:
        p[0:60], p[60:120], p[120:180], p[180:240] = 1.8, 1.6, 1.4, 1.3
        p[240:300], p[300:360], p[360:420], p[420:480] = 1.4, 1.6, 2, 2.2
        p[480:540], p[540:600], p[600:660], p[660:720] = 2.4, 2.5, 2.6, 2.6
        p[720:780], p[780:840], p[840:899], p[900:959] = 2.7, 2.8, 2.8, 3
        p[960:1020], p[1020:1080], p[1080:1140], p[1140:1200] = 2.8, 2.7, 2.6, 2.5
        p[1200:1260], p[1260:1320], p[1320:1380], p[1380:1440] = 2.5, 2.5, 2.2, 1.8
    return p


def getWTR(app_st, s=None):
    val1, val2 = 0, 0
    loc, lb, ub, cost = getAppliances(s)
    for x in range(len(lb)):
        val1 += (app_st[x] - lb[x])
        val2 += (ub[x] - lb[x] - loc[x])
    return val1 / val2


def getCPR(app_st, s=None):
    nsa, pns = getnsa()
    loc, lb, ub, ps = getAppliances(s)
    consumption_per_min = np.zeros(1440)
    consumption_matrix = np.zeros((len(app_st), 1440))
    for x in range(len(app_st)):
        for y in range(app_st[x], app_st[x]+loc[x]):
            consumption_per_min[y] += ps[x]
            consumption_matrix[x][y] = 1
    c = 0.0333
    q = len(nsa)
    n = 1440
    AP = np.zeros(1440)
    count = 0
    a=0

    for x in range(n):
        AP[x] = c - consumption_per_min[x]
    for i in range(n):
        for p in pns:
            if p > AP[i]:
                count += 1
    return (count/(q*n))

def getConsumptionMatrix(app_st, s=None):
    consumption_per_min = np.zeros(1440)
    loc, lb, ub, ps = getAppliances(s)
    consumption_matrix = np.zeros((len(app_st), 1440))
    price = getPricePerMin(s)
    for x in range(len(app_st)):
        for y in range(app_st[x], app_st[x]+loc[x]):
            consumption_per_min[y] += ps[x]
            consumption_matrix[x][y] = 1
    return consumption_per_min, consumption_matrix

def getconsumptionpermin():
    main.consumption_mins.sort()
    return main.consumption_per_min


def getUC(wtr, cpr):
    return (1 - ((wtr + cpr) / 2)) * 100


def getPAR(app_st, s=None):
    c = 0.0333
    l = 1.543
    loc, lb, ub, cost = getAppliances(s)
    consumption_per_min = np.zeros(1440)
    price = getPricePerMin(s)
    total_cost = 0
    for x in range(len(lb)):
        test = np.rint(app_st[x]).astype(int)
        for y in range(test, test+loc[x]):
            consumption_per_min[y] += cost[x]
    ps_max = np.max(consumption_per_min)
    ps_avg = Average(consumption_per_min)
    return ps_max/ps_avg


def multiobjective(eb, par, wtr, cpr, a, b):
    return (0.4 * (eb/(eb+a))) + (0.2 * (par/(par+b))) + (0.2 * wtr) + (0.2 * cpr) # cost for the initial solution are a & b


def objfun(app_st, a, b, s=None):
    eb = getBill(app_st, s)
    par = getPAR(app_st, s)
    wtr = getWTR(app_st, s)
    cpr = getCPR(app_st, s)
    obj = (0.4 * (eb/(eb+a)) + 0.2 * (par/(par+b)) + (0.2 * wtr) + (0.2 * cpr))
    return obj


def position_initalize(p_num, lb, ub, loc):
    positions = np.zeros((p_num, len(lb)))
    for i in range(p_num):
        for x in range(len(lb)):
            positions[i][x] = np.random.randint(lb[x], abs(ub[x]-loc[x]))
    return positions


def validate_position(p_num, position, lb, ub, loc):
    positions = position.astype(int)
    for i in range(p_num):
        for x in range(len(lb)):
            if not positions[i][x] in range(lb[x], abs(ub[x] - loc[x])):
                positions[i][x] = np.random.randint(lb[x], abs(ub[x]-loc[x]))
    return positions

def pso_position_initalize(lb, ub, loc):
    positions = np.zeros(len(lb))
    for x in range(len(lb)):
            positions[x] = np.random.randint(lb[x], abs(ub[x]-loc[x]))
    return positions

def ssa_validate_position(position, lb, ub, loc):
    positions = position.astype(int)
    for x in range(len(position)):
            if not positions[x] in range(lb[x], abs(ub[x] - loc[x])):
                positions[x] = np.random.randint(lb[x], abs(ub[x]-loc[x]))
    return positions