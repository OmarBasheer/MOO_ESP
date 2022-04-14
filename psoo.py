import sys
from copy import deepcopy

import numpy as np

from support_methods import *

ID_POS = 0
ID_TAR = 1
ID_VEC = 2  # Velocity
ID_LOP = 3  # Local position
ID_LOF = 4  # Local fitness
def use_pso(c1, c2, w_min,w_max, objf, maxIter, pop_size, lb, ub, loc, app_st):
    v_max = 0.5 * (ub - lb)
    v_min = -v_max
    app_st = validate(app_st, lb, ub, loc)
    currentIt = 0
    velocity = np.random.uniform(v_min, v_max)
    position = app_st
    local_pos = deepcopy(position)
    local_fit = deepcopy()
    global_best = pop_size[0]
    a = getBill(app_st)
    b = getPAR(app_st)
    #w = (currentIt - maxIter)/currentIt * (w_max - w_min) + w_min
    nextGenPop = []
    for i in range(0, pop_size):
        best_fit = objf(global_best)
        currentInd = deepcopy(pop_size[i])
        current_fit = objf(currentInd)
        if current_fit < best_fit:
            global_best = deepcopy(currentInd)
    for i in range(0, pop_size):
        v_new = velocity + c1 * np.random.rand() * (currentInd - pop_size[i]) + c2 \
        * np.random.rand() * (global_best - pop_size[i])
        x_new = pop_size[i] + v_new