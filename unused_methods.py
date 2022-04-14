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