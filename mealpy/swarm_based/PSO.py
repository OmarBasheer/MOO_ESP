# !/usr/bin/env python
# Created by "Thieu" at 09:49, 17/03/2020 ----------%
#       Email: nguyenthieu2102@gmail.com            %
#       Github: https://github.com/thieu1995        %
# --------------------------------------------------%

import numpy as np
from copy import deepcopy

import support_methods
from mealpy.optimizer import Optimizer
from support_methods import *

class BasePSO(Optimizer):
    ID_POS = 0
    ID_TAR = 1
    ID_VEC = 2  # Velocity
    ID_LOP = 3  # Local position
    ID_LOF = 4  # Local fitness

    def __init__(self, problem, epoch=10000, pop_size=100, c1=2.05, c2=2.05, w_min=0.4, w_max=0.9, **kwargs):
        """
        Args:
            problem (dict): The problem dictionary
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
            c1 (float): [0-2] local coefficient
            c2 (float): [0-2] global coefficient
            w_min (float): Weight min of bird, default = 0.4
            w_max (float): Weight max of bird, default = 0.9
        """
        super().__init__(problem, kwargs)
        self.epoch = self.validator.check_int("epoch", epoch, [1, 100000])
        self.pop_size = self.validator.check_int("pop_size", pop_size, [10, 10000])
        self.c1 = self.validator.check_float("c1", c1, (0, 5.0))
        self.c2 = self.validator.check_float("c2", c2, (0, 5.0))
        self.w_min = self.validator.check_float("w_min", w_min, (0, 0.5))
        self.w_max = self.validator.check_float("w_max", w_max, [0.5, 2.0])
        self.nfe_per_epoch = self.pop_size
        self.sort_flag = False
        self.v_max = 0.5 * (self.problem.ub - self.problem.lb)
        self.v_min = -self.v_max
        self.s = kwargs["s"]
        self.a = kwargs["a"]
        self.b = kwargs["b"]

    def create_solution(self, lb=None, ub=None, loc=None, a=None, b=None, s=None):
        """
        To get the position, fitness wrapper, target and obj list
            + A[self.ID_POS]                  --> Return: position
            + A[self.ID_TAR]                  --> Return: [target, [obj1, obj2, ...]]
            + A[self.ID_TAR][self.ID_FIT]     --> Return: target
            + A[self.ID_TAR][self.ID_OBJ]     --> Return: [obj1, obj2, ...]

        Returns:
            list: wrapper of solution with format [position, target, velocity, local_pos, local_fit]
        """
        position = support_methods.pso_position_initalize(lb, ub, loc)
        position = self.amend_position(position, lb, ub, loc)
        #a = getBill(position, s)
        #b = getPAR(position, s)
        target = self.get_target_wrapper(position, a, b, s)
        velocity = np.random.uniform(self.v_min, self.v_max)
        local_pos = deepcopy(position)
        local_fit = deepcopy(target)
        return [position, target, velocity, local_pos, local_fit]

    def amend_position(self, position=None, lb=None, ub=None, loc=None):
        """
        Depend on what kind of problem are we trying to solve, there will be an different amend_position
        function to rebound the position of agent into the valid range.

        Args:
            position: vector position (location) of the solution.
            lb: list of lower bound values
            ub: list of upper bound values
            loc: list of LOCs

        Returns:
            Amended position (make the position is in bound)
        """
        # solution = np.clip(lb, abs(ub - loc), position)
        # solution_int = solution.astype(int)
        positions = position.astype(int)
        for x in range(len(position)):
            if not positions[x] in range(lb[x], abs(ub[x] - loc[x])):
                positions[x] = np.random.randint(lb[x], abs(ub[x] - loc[x]))
        return positions

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        # Update weight after each move count  (weight down)
        w = (self.epoch - epoch) / self.epoch * (self.w_max - self.w_min) + self.w_min
        pop_new = []
        for idx in range(0, self.pop_size):
            agent = deepcopy(self.pop[idx])
            v_new = w * self.pop[idx][self.ID_VEC] + self.c1 * np.random.rand() * \
                    (self.pop[idx][self.ID_LOP] - self.pop[idx][self.ID_POS]) + \
                    self.c2 * np.random.rand() * (self.g_best[self.ID_POS] - self.pop[idx][self.ID_POS])
            x_new = self.pop[idx][self.ID_POS] + v_new  # Xi(new) = Xi(old) + Vi(new) * deltaT (deltaT = 1)
            pos_new = self.amend_position(x_new, self.problem.lb, self.problem.ub, self.problem.loc)
            agent[self.ID_POS] = pos_new
            agent[self.ID_VEC] = v_new
            pop_new.append(agent)
        pop_new = self.update_target_wrapper_population(pop_new, self.a, self.b, self.s)

        for idx in range(0, self.pop_size):
            if self.compare_agent(pop_new[idx], self.pop[idx]):
                self.pop[idx] = deepcopy(pop_new[idx])
                if self.compare_agent(pop_new[idx], [None, self.pop[idx][self.ID_LOF]]):
                    self.pop[idx][self.ID_LOP] = deepcopy(pop_new[idx][self.ID_POS])
                    self.pop[idx][self.ID_LOF] = deepcopy(pop_new[idx][self.ID_TAR])

