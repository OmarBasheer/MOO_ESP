import json

# read file
with open('lookup.json', 'r') as myfile:
    data=myfile.read()

# parse file
obj = json.loads(data)

# show values

for x in obj:
    print(str(x))


def price_calculate(minute, price): # change price to power consumption
    sum_cost = 0
    if minute <= 60:
        sum_cost = (price * 0.028)
    elif minute <= 120:
        sum_cost = (price * 0.023)
    elif minute <= 180:
        sum_cost = (price * 0.018)
    elif minute <= 240:
        sum_cost = (price * 0.013)
    elif minute <= 300:
        sum_cost = (price * 0.015)
    elif minute <= 360:
        sum_cost = (price * 0.022)
    elif minute <= 420:
        sum_cost = (price * 0.025)
    elif minute <= 480:
        sum_cost = (price * 0.054)
    elif minute <= 540:
        sum_cost = (price * 0.062)
    elif minute <= 600:
        sum_cost = (price * 0.065)
    elif minute <= 660:
        sum_cost = (price * 0.069)
    elif minute <= 720:
        sum_cost = (price * 0.077)
    elif minute <= 780:
        sum_cost = (price * 0.08)
    elif minute <= 840:
        sum_cost = (price * 0.082)
    elif minute <= 900:
        sum_cost = (price * 0.085)
    elif minute <= 960:
        sum_cost = (price * 0.1)
    elif minute <= 1020:
        sum_cost = (price * 0.105)
    elif minute <= 1080:
        sum_cost = (price * 0.096)
    elif minute <= 1140:
        sum_cost = (price * 0.082)
    elif minute <= 1200:
        sum_cost = (price * 0.08)
    elif minute <= 1260:
        sum_cost = (price * 0.077)
    elif minute <= 1320:
        sum_cost = (price * 0.073)
    elif minute <= 1380:
        sum_cost = (price * 0.062)
    else:
        sum_cost = (price * 0.032)
    return sum_cost