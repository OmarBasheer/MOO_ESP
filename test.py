import numpy as np
import matplotlib.pyplot as plt

from support_methods import *


def PSOE(obj, p_num, N, scale, w, r, c1, c2, a, b, eps, lb, ub, loc,
        early_stopping=100, max_iter=1000, verbose=True, random_state=None):
    """Main algorithm"""
    # initialize
    # np.random.seed(random_state)
    params_num = N
    p = position_initalize(p_num, lb, ub, loc)

    v = np.random.normal(scale=scale, size=(p_num, params_num))
    # t = np.linspace(0, 4 * np.pi, 101)
    error = obj(p[0], a, b)
    pbest = p.copy()
    gbest = p[error.argmin()]
    best_params = [gbest]
    e = [error.min()]
    iter_num = 0
    count = 0
    if verbose == True:
        if len(gbest) <= 7:
            print(f'Initial condition:   params = {gbest}\n\t\t     error = {e[-1]:.4f}\n')
        else:
            print(f'Initial condition:\terror = {e[-1]:.4f}\n')

    # main algorithm
    while error.min() > eps and iter_num < max_iter and count < early_stopping:
        # create random numbers, used for updating particle position
        r1 = np.random.uniform(size=(params_num))
        r2 = np.random.uniform(size=(params_num))
        r1 = np.tile(r1, p_num).reshape(p_num, -1)
        r2 = np.tile(r2, p_num).reshape(p_num, -1)
        for i in range(p_num):
            # update particle position
            v = w * v + c1 * r1 * (pbest - p) + c2 * r2 * (gbest - p)
            w = w * r
            p = p + v
        p = validate_position(p, lb, ub, loc)
        # calculate error
        error = obj(p[0], a, b)
        errorbest = obj(p[0], a, b)
        # update global best
        gbest = p[error.argmin()]
        # update personal best
        min_idx = np.array([error, errorbest]).argmin(axis=0)
        for i, idx in enumerate(min_idx):
            if idx == 0: pbest[i, :] = p[i, :].copy()
        # update tabulation
        iter_num += 1
        if error.min() >= e[-1]:
            count += 1
        else:
            count = 0
        e.append(error.min())
        best_params.append(gbest)
        # print result in terminal
        if verbose:
            if len(gbest) <= 7:
                print(f'Iteration: {iter_num}\tbest params = {gbest}\n\t\terror = {e[-1]:.4f}')
            else:
                print(f'Iteration: {iter_num}\terror = {e[-1]:.4f}')

    # in case max iteration reached
    if iter_num == max_iter:
        print(iter_num, 'maximum iterations reached!',
              'Try increasing max_iter or adjusting PSO parameters for better result.')

    # cut tabulation for early stopping
    if count == early_stopping:
        iter_num = iter_num - count
        best_params = best_params[:-early_stopping]
        e = e[:-early_stopping]

    # return the number of iterations needed, the best parameters, and error
    return iter_num, np.array(best_params), np.array(e)