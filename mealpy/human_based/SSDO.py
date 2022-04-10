# !/usr/bin/env python
# Created by "Thieu" at 11:17, 18/03/2020 ----------%
#       Email: nguyenthieu2102@gmail.com            %
#       Github: https://github.com/thieu1995        %
# --------------------------------------------------%

import numpy as np
from copy import deepcopy
from mealpy.optimizer import Optimizer


class BaseSSDO(Optimizer):
    """
    The original version of: Social Ski-Driver Optimization (SSDO)

    Links:
       1. https://doi.org/10.1007/s00521-019-04159-z
       2. https://www.mathworks.com/matlabcentral/fileexchange/71210-social-ski-driver-ssd-optimization-algorithm-2019

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.human_based.SSDO import BaseSSDO
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
    >>> model = BaseSSDO(problem_dict1, epoch, pop_size)
    >>> best_position, best_fitness = model.solve()
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")

    References
    ~~~~~~~~~~
    [1] Tharwat, A. and Gabel, T., 2020. Parameters optimization of support vector machines for imbalanced
    data using social ski driver algorithm. Neural Computing and Applications, 32(11), pp.6925-6938.
    """

    ID_VEL = 2
    ID_LOC = 3

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

    def create_solution(self, lb=None, ub=None):
        """
        To get the position, fitness wrapper, target and obj list
            + A[self.ID_POS]                  --> Return: position
            + A[self.ID_TAR]                  --> Return: [target, [obj1, obj2, ...]]
            + A[self.ID_TAR][self.ID_FIT]     --> Return: target
            + A[self.ID_TAR][self.ID_OBJ]     --> Return: [obj1, obj2, ...]

        Returns:
            list: wrapper of solution with format [position, target, velocity, best_local_position]
        """
        position = self.generate_position(lb, ub)
        position = self.amend_position(position, lb, ub)
        target = self.get_target_wrapper(position)
        velocity = np.random.uniform(lb, ub)
        pos_local = deepcopy(position)
        return [position, target, velocity, pos_local]

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        c = 2 - epoch * (2.0 / self.epoch)  # a decreases linearly from 2 to 0

        ## Calculate the mean of the best three solutions in each dimension. Eq 9
        _, pop_best3, _ = self.get_special_solutions(self.pop, best=3)
        pos_mean = np.mean(np.array([item[self.ID_POS] for item in pop_best3]))

        pop_new = deepcopy(self.pop)
        # Updating velocity vectors
        for i in range(0, self.pop_size):
            r1 = np.random.uniform()  # r1, r2 is a random number in [0,1]
            r2 = np.random.uniform()
            if r2 <= 0.5:  ## Use Sine function to move
                vel_new = c * np.sin(r1) * (self.pop[i][self.ID_LOC] - self.pop[i][self.ID_POS]) + np.sin(r1) * (pos_mean - self.pop[i][self.ID_POS])
            else:  ## Use Cosine function to move
                vel_new = c * np.cos(r1) * (self.pop[i][self.ID_LOC] - self.pop[i][self.ID_POS]) + np.cos(r1) * (pos_mean - self.pop[i][self.ID_POS])
            pop_new[i][self.ID_VEL] = vel_new

        ## Reproduction
        for idx in range(0, self.pop_size):
            pos_new = np.random.uniform() * pop_new[idx][self.ID_POS] + pop_new[idx][self.ID_VEL]
            pos_new = self.amend_position(pos_new, self.problem.lb, self.problem.ub)
            pop_new[idx][self.ID_POS] = pos_new
        pop_new = self.update_target_wrapper_population(pop_new)
        self.pop = self.greedy_selection_population(self.pop, pop_new)
