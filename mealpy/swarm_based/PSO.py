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
    """
    The original version of: Particle Swarm Optimization (PSO)

    Hyper-parameters should fine tuned in approximate range to get faster convergen toward the global optimum:
        + c1 (float): [1, 3], local coefficient, default = 2.05
        + c2 (float): [1, 3], global coefficient, default = 2.05
        + w_min (float): [0.1, 0.5], Weight min of bird, default = 0.4
        + w_max (float): [0.8, 2.0], Weight max of bird, default = 0.9

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.swarm_based.PSO import BasePSO
    >>>
    >>> def fitness_function(solution):
    >>>     return np.sum(solution**2)
    >>>
    >>> problem_dict1 = {
    >>>     "fit_func": fitness_function,
    >>>     "lb": [-10, -15, -4, -2, -8],
    >>>     "ub": [10, 15, 12, 8, 20],
    >>>     "minmax": "min",
    >>> }
    >>>
    >>> epoch = 1000
    >>> pop_size = 50
    >>> c1 = 2.05
    >>> c2 = 2.05
    >>> w_min = 0.4
    >>> w_max = 0.9
    >>> model = BasePSO(problem_dict1, epoch, pop_size, c1, c2, w_min, w_max)
    >>> best_position, best_fitness = model.solve()
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")

    References
    ~~~~~~~~~~
    [1] Kennedy, J. and Eberhart, R., 1995, November. Particle swarm optimization. In Proceedings of
    ICNN'95-international conference on neural networks (Vol. 4, pp. 1942-1948). IEEE.
    """
    ID_POS = 0
    ID_TAR = 1
    ID_VEC = 2  # Velocity
    ID_LOP = 3  # Local position
    ID_LOF = 4  # Local fitness
    a=0
    b=0
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


    def create_solution(self, lb=None, ub=None, loc=None, a=None, b=None):
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
        a = getBill(position)
        b = getPAR(position)
        target = self.get_target_wrapper(position, a, b)
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
        position = position.astype(int)
        for x in range(len(position)):
            if x == 17:
                position[x] = 0
            if position[x] in range(lb[x], abs(ub[x]-loc[x])):
                position[x] = position[x]
            else:
                position[x] = lb[x]
        return position

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
        pop_new = self.update_target_wrapper_population(pop_new, 62, 3.2)

        for idx in range(0, self.pop_size):
            if self.compare_agent(pop_new[idx], self.pop[idx]):
                self.pop[idx] = deepcopy(pop_new[idx])
                if self.compare_agent(pop_new[idx], [None, self.pop[idx][self.ID_LOF]]):
                    self.pop[idx][self.ID_LOP] = deepcopy(pop_new[idx][self.ID_POS])
                    self.pop[idx][self.ID_LOF] = deepcopy(pop_new[idx][self.ID_TAR])


class PPSO(Optimizer):
    """
    The original version of: Phasor Particle Swarm Optimization (P-PSO)

    Notes
    ~~~~~
    + This code is converted from matlab code (sent from author: Ebrahim Akbari)

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.swarm_based.PSO import PPSO
    >>>
    >>> def fitness_function(solution):
    >>>     return np.sum(solution**2)
    >>>
    >>> problem_dict1 = {
    >>>     "fit_func": fitness_function,
    >>>     "lb": [-10, -15, -4, -2, -8],
    >>>     "ub": [10, 15, 12, 8, 20],
    >>>     "minmax": "min",
    >>> }
    >>>
    >>> epoch = 1000
    >>> pop_size = 50
    >>> model = PPSO(problem_dict1, epoch, pop_size)
    >>> best_position, best_fitness = model.solve()
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")

    References
    ~~~~~~~~~~
    [1] Ghasemi, M., Akbari, E., Rahimnejad, A., Razavi, S.E., Ghavidel, S. and Li, L., 2019.
    Phasor particle swarm optimization: a simple and efficient variant of PSO. Soft Computing, 23(19), pp.9701-9718.
    """

    ID_VEC = 2  # Velocity
    ID_LOP = 3  # Local position
    ID_LOF = 4  # Local fitness

    def __init__(self, problem, epoch=10000, pop_size=100, **kwargs):
        """
        Args:
            problem (dict): The problem dictionary
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
        """
        super().__init__(problem, kwargs)
        self.epoch = self.validator.check_int("epoch", epoch, [1, 100000])
        self.pop_size = self.validator.check_int("pop_size", pop_size, [10, 10000])
        self.nfe_per_epoch = self.pop_size
        self.sort_flag = False
        self.v_max = 0.5 * (self.problem.ub - self.problem.lb)
        self.v_min = -self.v_max

        # Dynamic variable
        self.dyn_delta_list = np.random.uniform(0, 2 * np.pi, self.pop_size)

    def create_solution(self, lb=None, ub=None, loc=None, a=None, b=None):
        """
        To get the position, fitness wrapper, target and obj list
            + A[self.ID_POS]                  --> Return: position
            + A[self.ID_TAR]                  --> Return: [target, [obj1, obj2, ...]]
            + A[self.ID_TAR][self.ID_FIT]     --> Return: target
            + A[self.ID_TAR][self.ID_OBJ]     --> Return: [obj1, obj2, ...]

        Returns:
            list: wrapper of solution with format [position, target, velocity, local_pos, local_fit]
        """
        position = self.generate_position(lb, ub, loc)
        position = self.amend_position(position, lb, ub)
        target = self.get_target_wrapper(position, a, b)
        velocity = np.random.uniform(self.v_min, self.v_max)
        local_pos = deepcopy(position)
        local_fit = deepcopy(target)
        return [position, target, velocity, local_pos, local_fit]

    def evolve(self, epoch, **kwargs):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        pop_new = []
        for i in range(0, self.pop_size):
            agent = deepcopy(self.pop[i])
            aa = 2 * (np.sin(self.dyn_delta_list[i]))
            bb = 2 * (np.cos(self.dyn_delta_list[i]))
            ee = np.abs(np.cos(self.dyn_delta_list[i])) ** aa
            tt = np.abs(np.sin(self.dyn_delta_list[i])) ** bb

            v_new = ee * (self.pop[i][self.ID_LOP] - self.pop[i][self.ID_POS]) + tt * (self.g_best[self.ID_POS] - self.pop[i][self.ID_POS])
            v_new = np.minimum(np.maximum(v_new, -self.v_max), self.v_max)
            agent[self.ID_VEC] = deepcopy(v_new)

            pos_new = self.pop[i][self.ID_POS] + v_new
            agent[self.ID_POS] = self.amend_position(pos_new, self.problem.lb, self.problem.ub)

            self.dyn_delta_list[i] += np.abs(aa + bb) * (2 * np.pi)
            self.v_max = (np.abs(np.cos(self.dyn_delta_list[i])) ** 2) * (self.problem.ub - self.problem.lb)
            pop_new.append(agent)
        # Update fitness for all solutions
        pop_new = self.update_target_wrapper_population(pop_new, kwargs["a"], kwargs["b"])

        # Update current position, current velocity and compare with past position, past fitness (local best)
        for idx in range(0, self.pop_size):
            if self.compare_agent(pop_new[idx], self.pop[idx]):
                self.pop[idx] = deepcopy(pop_new[idx])
                if self.compare_agent(pop_new[idx], [None, self.pop[idx][self.ID_LOF]]):
                    self.pop[idx][self.ID_LOP] = deepcopy(pop_new[idx][self.ID_POS])
                    self.pop[idx][self.ID_LOF] = deepcopy(pop_new[idx][self.ID_TAR])

