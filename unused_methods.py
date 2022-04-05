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
