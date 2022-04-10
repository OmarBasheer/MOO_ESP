# !/usr/bin/env python
# Created by "Thieu" at 10:21, 18/03/2020 ----------%
#       Email: nguyenthieu2102@gmail.com            %
#       Github: https://github.com/thieu1995        %
# --------------------------------------------------%

import numpy as np
from copy import deepcopy
from mealpy.optimizer import Optimizer


class BaseQSA(Optimizer):
    """
    My changed version of: Queuing Search Algorithm (QSA)

    Notes
    ~~~~~
    All third loop is removed, the global best solution is used in business 3 instead of random solution

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.human_based.QSA import BaseQSA
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
    >>> model = BaseQSA(problem_dict1, epoch, pop_size)
    >>> best_position, best_fitness = model.solve()
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")
    """

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
        self.nfe_per_epoch = 3 * self.pop_size
        self.sort_flag = True

    def _calculate_queue_length__(self, t1, t2, t3):
        """
        Calculate length of each queue based on  t1, t2,t3
            + t1 = t1 * 1.0e+100
            + t2 = t2 * 1.0e+100
            + t3 = t3 * 1.0e+100
        """
        if t1 > 1.0e-6:
            n1 = (1 / t1) / ((1 / t1) + (1 / t2) + (1 / t3))
            n2 = (1 / t2) / ((1 / t1) + (1 / t2) + (1 / t3))
        else:
            n1 = 1.0 / 3
            n2 = 1.0 / 3
        q1 = int(n1 * self.pop_size)
        q2 = int(n2 * self.pop_size)
        q3 = self.pop_size - q1 - q2
        return q1, q2, q3

    def _update_business_1(self, pop=None, current_epoch=None):
        A1, A2, A3 = pop[0][self.ID_POS], pop[1][self.ID_POS], pop[2][self.ID_POS]
        t1, t2, t3 = pop[0][self.ID_TAR][self.ID_FIT], pop[1][self.ID_TAR][self.ID_FIT], pop[2][self.ID_TAR][self.ID_FIT]
        q1, q2, q3 = self._calculate_queue_length__(t1, t2, t3)
        case = None
        for i in range(self.pop_size):
            if i < q1:
                if i == 0:
                    case = 1
                A = deepcopy(A1)
            elif q1 <= i < q1 + q2:
                if i == q1:
                    case = 1
                A = deepcopy(A2)
            else:
                if i == q1 + q2:
                    case = 1
                A = deepcopy(A3)
            beta = np.power(current_epoch, np.power(current_epoch / self.epoch, 0.5))
            alpha = np.random.uniform(-1, 1)
            E = np.random.exponential(0.5, self.problem.n_dims)
            F1 = beta * alpha * (E * np.abs(A - pop[i][self.ID_POS])) + np.random.exponential(0.5) * (A - pop[i][self.ID_POS])
            F2 = beta * alpha * (E * np.abs(A - pop[i][self.ID_POS]))
            if case == 1:
                pos_new = A + F1
                pos_new = self.amend_position(pos_new, self.problem.lb, self.problem.ub)
                target = self.get_target_wrapper(pos_new)
                if self.compare_agent([pos_new, target], pop[i]):
                    pop[i] = [pos_new, target]
                else:
                    case = 2
            else:
                pos_new = pop[i][self.ID_POS] + F2
                pos_new = self.amend_position(pos_new, self.problem.lb, self.problem.ub)
                target = self.get_target_wrapper(pos_new)
                if self.compare_agent([pos_new, target], pop[i]):
                    pop[i] = [pos_new, target]
                else:
                    case = 1
        pop, _ = self.get_global_best_solution(pop)
        return pop

    def _update_business_2(self, pop=None):
        A1, A2, A3 = pop[0][self.ID_POS], pop[1][self.ID_POS], pop[2][self.ID_POS]
        t1, t2, t3 = pop[0][self.ID_TAR][self.ID_FIT], pop[1][self.ID_TAR][self.ID_FIT], pop[2][self.ID_TAR][self.ID_FIT]
        q1, q2, q3 = self._calculate_queue_length__(t1, t2, t3)
        pr = [i / self.pop_size for i in range(1, self.pop_size + 1)]
        if t1 > 1.0e-005:
            cv = t1 / (t2 + t3)
        else:
            cv = 1.0 / 2
        pop_new = []
        for i in range(self.pop_size):
            if i < q1:
                A = deepcopy(A1)
            elif q1 <= i < q1 + q2:
                A = deepcopy(A2)
            else:
                A = deepcopy(A3)
            if np.random.random() < pr[i]:
                i1, i2 = np.random.choice(self.pop_size, 2, replace=False)
                if np.random.random() < cv:
                    X_new = pop[i][self.ID_POS] + np.random.exponential(0.5) * (pop[i1][self.ID_POS] - pop[i2][self.ID_POS])
                else:
                    X_new = pop[i][self.ID_POS] + np.random.exponential(0.5) * (A - pop[i1][self.ID_POS])
            else:
                X_new = self.generate_position(self.problem.lb, self.problem.ub)
            pos_new = self.amend_position(X_new, self.problem.lb, self.problem.ub)
            pop_new.append([pos_new, None])
        pop_new = self.update_target_wrapper_population(pop_new)
        pop = self.greedy_selection_population(pop, pop_new)
        pop, _ = self.get_global_best_solution(pop)
        return pop

    def _update_business_3(self, pop, g_best):
        pr = np.array([i / self.pop_size for i in range(1, self.pop_size + 1)])
        pop_new = []
        for i in range(self.pop_size):
            X_new = deepcopy(pop[i][self.ID_POS])
            id1 = np.random.choice(self.pop_size)
            temp = g_best[self.ID_POS] + np.random.exponential(0.5, self.problem.n_dims) * (pop[id1][self.ID_POS] - pop[i][self.ID_POS])
            X_new = np.where(np.random.random(self.problem.n_dims) > pr[i], temp, X_new)
            pos_new = self.amend_position(X_new, self.problem.lb, self.problem.ub)
            pop_new.append([pos_new, None])
        pop_new = self.update_target_wrapper_population(pop_new)
        pop_new = self.greedy_selection_population(pop, pop_new)
        return pop_new

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        pop = self._update_business_1(self.pop, epoch + 1)
        pop = self._update_business_2(pop)
        self.pop = self._update_business_3(pop, self.g_best)


class OppoQSA(BaseQSA):
    """
    My Opposition-based learning version of: Queuing Search Algorithm (OQSA)

    Notes
    ~~~~~
    Added the opposition-based learning technique

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.human_based.QSA import OppoQSA
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
    >>> model = OppoQSA(problem_dict1, epoch, pop_size)
    >>> best_position, best_fitness = model.solve()
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")
    """

    def __init__(self, problem, epoch=10000, pop_size=100, **kwargs):
        """
        Args:
            problem (dict): The problem dictionary
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
        """
        super().__init__(problem, epoch, pop_size, **kwargs)
        self.nfe_per_epoch = 4 * self.pop_size
        self.sort_flag = True

    def _opposition_based(self, pop=None, g_best=None):
        pop, _ = self.get_global_best_solution(pop)
        pop_new = []
        for i in range(0, self.pop_size):
            X_new = self.create_opposition_position(pop[i], g_best)
            pos_new = self.amend_position(X_new, self.problem.lb, self.problem.ub)
            pop_new.append([pos_new, None])
        pop_new = self.update_target_wrapper_population(pop_new)
        return self.greedy_selection_population(pop, pop_new)

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        pop = self._update_business_1(self.pop, epoch + 1)
        pop = self._update_business_2(pop)
        pop = self._update_business_3(pop, self.g_best)
        self.pop = self._opposition_based(pop, self.g_best)


class LevyQSA(BaseQSA):
    """
    My Levy-flight version of: Queuing Search Algorithm (LQSA)

    Notes
    ~~~~~
    Added the Levy-flight technique to QSA

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.human_based.QSA import LevyQSA
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
    >>> model = LevyQSA(problem_dict1, epoch, pop_size)
    >>> best_position, best_fitness = model.solve()
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")
    """

    def __init__(self, problem, epoch=10000, pop_size=100, **kwargs):
        """
        Args:
            problem (dict): The problem dictionary
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
        """
        super().__init__(problem, epoch, pop_size, **kwargs)
        self.nfe_per_epoch = 3 * self.pop_size
        self.sort_flag = True

    def _update_business_2(self, pop=None, current_epoch=None):
        A1, A2, A3 = pop[0][self.ID_POS], pop[1][self.ID_POS], pop[2][self.ID_POS]
        t1, t2, t3 = pop[0][self.ID_TAR][self.ID_FIT], pop[1][self.ID_TAR][self.ID_FIT], pop[2][self.ID_TAR][self.ID_FIT]
        q1, q2, q3 = self._calculate_queue_length__(t1, t2, t3)
        pr = [i / self.pop_size for i in range(1, self.pop_size + 1)]
        if t1 > 1.0e-6:
            cv = t1 / (t2 + t3)
        else:
            cv = 1 / 2
        pop_new = []
        for i in range(self.pop_size):
            if i < q1:
                A = deepcopy(A1)
            elif q1 <= i < q1 + q2:
                A = deepcopy(A2)
            else:
                A = deepcopy(A3)
            if np.random.random() < pr[i]:
                id1 = np.random.choice(self.pop_size)
                if np.random.random() < cv:
                    levy_step = self.get_levy_flight_step(beta=1.0, multiplier=0.001, case=-1)
                    X_new = pop[i][self.ID_POS] + np.random.normal(0, 1, self.problem.n_dims) * levy_step
                else:
                    X_new = pop[i][self.ID_POS] + np.random.exponential(0.5) * (A - pop[id1][self.ID_POS])
                pos_new = self.amend_position(X_new, self.problem.lb, self.problem.ub)
            else:
                pos_new = self.generate_position(self.problem.lb, self.problem.ub)
            pos_new = self.amend_position(pos_new, self.problem.lb, self.problem.ub)
            pop_new.append([pos_new, None])
        pop_new = self.update_target_wrapper_population(pop_new)
        pop_new = self.greedy_selection_population(pop, pop_new)
        pop_new, _ = self.get_global_best_solution(pop_new)
        return pop_new

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        pop = self._update_business_1(self.pop, epoch + 1)
        pop = self._update_business_2(pop, epoch + 1)
        self.pop = self._update_business_3(pop, self.g_best)


class ImprovedQSA(OppoQSA, LevyQSA):
    """
    The original version of: Improved Queuing Search Algorithm (QSA)

    Links:
       1. https://doi.org/10.1007/s12652-020-02849-4

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.human_based.QSA import ImprovedQSA
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
    >>> model = ImprovedQSA(problem_dict1, epoch, pop_size)
    >>> best_position, best_fitness = model.solve()
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")

    References
    ~~~~~~~~~~
    [1] Nguyen, B.M., Hoang, B., Nguyen, T. and Nguyen, G., 2021. nQSV-Net: a novel queuing search variant for
    global space search and workload modeling. Journal of Ambient Intelligence and Humanized Computing, 12(1), pp.27-46.
    """

    def __init__(self, problem, epoch=10000, pop_size=100, **kwargs):
        """
        Args:
            problem (dict): The problem dictionary
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
        """
        super().__init__(problem, epoch, pop_size, **kwargs)
        self.nfe_per_epoch = 4 * self.pop_size
        self.sort_flag = True

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        pop = self._update_business_1(self.pop, epoch + 1)
        pop = self._update_business_2(pop, epoch + 1)
        pop = self._update_business_3(pop, self.g_best)
        self.pop = self._opposition_based(pop, self.g_best)


class OriginalQSA(BaseQSA):
    """
    The original version of: Queuing Search Algorithm (QSA)

    Links:
       1. https://www.sciencedirect.com/science/article/abs/pii/S0307904X18302890

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.human_based.QSA import OriginalQSA
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
    >>> model = OriginalQSA(problem_dict1, epoch, pop_size)
    >>> best_position, best_fitness = model.solve()
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")

    References
    ~~~~~~~~~~
    [1] Zhang, J., Xiao, M., Gao, L. and Pan, Q., 2018. Queuing search algorithm: A novel metaheuristic algorithm
    for solving engineering optimization problems. Applied Mathematical Modelling, 63, pp.464-490.
    """

    def __init__(self, problem, epoch=10000, pop_size=100, **kwargs):
        """
        Args:
            problem (dict): The problem dictionary
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
        """
        super().__init__(problem, epoch, pop_size, **kwargs)
        self.nfe_per_epoch = 3 * self.pop_size
        self.sort_flag = True

    def _update_business_3(self, pop, g_best):
        pr = [i / self.pop_size for i in range(1, self.pop_size + 1)]
        pop_new = []
        for i in range(self.pop_size):
            pos_new = deepcopy(pop[i][self.ID_POS])
            for j in range(self.problem.n_dims):
                if np.random.random() > pr[i]:
                    i1, i2 = np.random.choice(self.pop_size, 2, replace=False)
                    e = np.random.exponential(0.5)
                    X1 = pop[i1][self.ID_POS]
                    X2 = pop[i2][self.ID_POS]
                    pos_new[j] = X1[j] + e * (X2[j] - pop[i][self.ID_POS][j])
            pos_new = self.amend_position(pos_new, self.problem.lb, self.problem.ub)
            pop_new.append([pos_new, None])
        pop_new = self.update_target_wrapper_population(pop_new)
        return self.greedy_selection_population(pop, pop_new)

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        pop = self._update_business_1(self.pop, epoch)
        pop = self._update_business_2(pop)
        self.pop = self._update_business_3(pop, self.g_best)