from datetime import datetime

import numpy as np

from support_methods import *


class funtion():
    def __init__(self):
        print("starting SSA")



def SSA(pop, lb, ub, loc, M, c, d, dim, f):
    # global fit
    P_percent = 0.2
    pNum = round(pop * P_percent)
    X = np.zeros((pop, dim))
    fit = np.zeros((pop, 1))
    initialEB = getBill(X[1, :])
    initialPAR = getPAR(X[1, :])
    for i in range(pop):
        X[i, :] = lb + (ub - lb-loc) * np.random.rand(1, dim)
        X[i, :] = ssa_validate_position(X[i, :], lb, ub, loc)
        cost = getBill(X[i, :])
        par = getPAR(X[i, :])
        cpr = getCPR(X[i, :])
        wtr = getWTR(X[i, :])
        fit[i, 0] = f(X[i, :])


    pFit = fit
    pX = X
    fMin = np.min(fit[:, 0])
    bestI = np.argmin(fit[:, 0])
    bestX = X[bestI, :]
    Convergence_curve = np.zeros((1, M))
    for t in range(M):
        start = datetime.now()
        sortIndex = np.argsort(pFit.T)
        fmax = np.max(pFit[:, 0])
        B = np.argmax(pFit[:, 0])
        worse = X[B, :]
        bestII = 0
        r2 = np.random.rand(1)

        if r2 < 0.6:
            for i in range(pNum):
                r1 = np.random.rand(1)
                X[sortIndex[0, i], :] = pX[sortIndex[0, i], :] * np.exp(-i / (r1 * M))
                X[sortIndex[0, i], :] = ssa_validate_position(X[sortIndex[0, i], :], lb, ub, loc)
                cost = getBill(X[sortIndex[0, i], :])
                par = getPAR(X[sortIndex[0, i], :])
                cpr = getCPR(X[sortIndex[0, i], :])
                wtr = getWTR(X[sortIndex[0, i], :])
                fit[sortIndex[0, i], 0] = f(X[sortIndex[0, i], :])
        elif r2 >= 0.6:
            for i in range(pNum):
                Q = np.random.rand(1)
                X[sortIndex[0, i], :] = pX[sortIndex[0, i], :] + Q * np.ones((1, dim))
                X[sortIndex[0, i], :] = ssa_validate_position(X[sortIndex[0, i], :], lb, ub, loc)
                cost = getBill(X[sortIndex[0, i], :])
                par = getPAR(X[sortIndex[0, i], :])
                cpr = getCPR(X[sortIndex[0, i], :])
                wtr = getWTR(X[sortIndex[0, i], :])
                fit[sortIndex[0, i], 0] = f(X[sortIndex[0, i], :])
                bestII = np.argmin(fit[:, 0])
        bestXX = X[bestII, :]

        for ii in range(pop - pNum):
            i = ii + pNum
            A = np.floor(np.random.rand(1, dim) * 2) * 2 - 1
            if i > pop / 2:
                Q = np.random.rand(1)
                X[sortIndex[0, i], :] = Q * np.exp(worse - pX[sortIndex[0, i], :] / np.square(i))
            else:
                X[sortIndex[0, i], :] = bestXX + np.dot(np.abs(pX[sortIndex[0, i], :] - bestXX),
                                                        1 / (A.T * np.dot(A, A.T))) * np.ones((1, dim))
            X[sortIndex[0, i], :] = ssa_validate_position(X[sortIndex[0, i], :], lb, ub, loc)
            cost = getBill(X[sortIndex[0, i], :])
            par = getPAR(X[sortIndex[0, i], :])
            cpr = getCPR(X[sortIndex[0, i], :])
            wtr = getWTR(X[sortIndex[0, i], :])
            fit[sortIndex[0, i], 0] = f(X[sortIndex[0, i], :])
        arrc = np.arange(len(sortIndex[0, :]))

        c = np.random.permutation(arrc)  # 随机排列序列
        b = sortIndex[0, c[0:20]]
        for j in range(len(b)):
            if pFit[sortIndex[0, b[j]], 0] > fMin:
                X[sortIndex[0, b[j]], :] = bestX + np.random.rand(1, dim) * np.abs(pX[sortIndex[0, b[j]], :] - bestX)
            else:
                X[sortIndex[0, b[j]], :] = pX[sortIndex[0, b[j]], :] + (2 * np.random.rand(1) - 1) * np.abs(
                    pX[sortIndex[0, b[j]], :] - worse) / (pFit[sortIndex[0, b[j]]] - fmax + 10 ** (-50))
            X[sortIndex[0, b[j]], :] = ssa_validate_position(X[sortIndex[0, b[j]], :], lb, ub, loc)
            cost = getBill(X[sortIndex[0, b[j]]])
            par = getPAR(X[sortIndex[0, b[j]]])
            cpr = getCPR(X[sortIndex[0, b[j]]])
            wtr = getWTR(X[sortIndex[0, b[j]]])
            fit[sortIndex[0, b[j]]] = f(X[sortIndex[0, b[j]]])
        for i in range(pop):
            if fit[i, 0] < pFit[i, 0]:
                pFit[i, 0] = fit[i, 0]
                pX[i, :] = X[i, :]
            if pFit[i, 0] < fMin:
                fMin = pFit[i, 0]
                bestX = pX[i, :]
        Convergence_curve[0, t] = fMin
        end = datetime.now()
        print(f'Iteration: {t}\terror = {fMin:.4f}, time taken: {str(end - start)[5:]}')

    return fMin, bestX, Convergence_curve
