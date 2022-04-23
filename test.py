from support_methods import *


def getCPRt(app_st, s=None):
    nsa, pns = getnsa()
    c = 0.0333
    q = len(nsa)
    n = 1440
    l = 1.543
    loc, lb, ub, cost = getAppliances(s)
    consumption_per_min = np.zeros(1440)
    price = getPricePerMin(s)
    total_cpr = 0
    for x in range(len(app_st)):
        for y in range(app_st[x], app_st[x]+loc[x]):
            consumption_per_min[y] += cost[x]
    for i in range(len(consumption_per_min)):
        for p in pns:
            if not p < (c-consumption_per_min[i]):
                total_cpr += 1
    return total_cpr / (q*n)

def getConsumptionMatrix(app_st, s=None):
    consumption_per_min = np.zeros(1440)
    loc, lb, ub, cost = getAppliances(s)
    price = getPricePerMin(s)
    for x in range(len(app_st)):
        for y in range(app_st[x], app_st[x]+loc[x]):
            consumption_per_min[y] += cost[x]
    return consumption_per_min

test_array =[547, 1254, 20, 119, 241, 396, 480, 635, 719, 844, 959, 1126, 1208, 1319, 60, 334, 0, 0, 128, 240, 415, 481,
625, 720, 844, 959, 1091, 1199, 1330, 299, 342, 1044, 0, 903]

ans = getCPRt(test_array, 7)
print(ans)