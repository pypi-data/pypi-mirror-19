# -*- coding: utf-8 -*-
"""
A collection of multi-armed bandit classes that use different
decision functions to select the arm with the highest
valuation.
"""
import statistics
import random
import math
import logging
import uuid
from hastur.distributions import BetaDistribution
from hastur.exceptions import InsufficientObservationsError


class Bandit(object):
    """
    Generic bandit class for MAB. Don't use this directly.

    A base class for implementing other multi-armed bandits.
    When subclassing, focus on overwriting the `valuation` attribute and
    the `select_arm()` method. These control how each arm is valued and
    how that valuation is used for selection, respectively.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.arms = {}

    def select_arm(self):
        """
        Return the *correct* arm.

        Method used to evaluate and choose which arm the
        bandit should select. Usually used as a wrapper around
        the `_select_best_arm()` and the `_select_random_arm()`
        methods. Each bandit may have different implementations
        of exactly what this does.

        :return: The name of the selected arm.
        :rtype: str
        :raises: InsufficientObservationsError. Will raise if any arm on the
                                       bandit is empty.
        """

        return self._select_best_arm()

    def _select_random_arm(self):
        """
        Return a random arm from the bandit.

        Computes the valuation--as per the bandit--for each of the arms but then
        just returns a random one.

        :return: the name of a random arm.
        :rtype: str

        :raises: InsufficientObservationsError. Raises if any arm on the bandit is empty.
        """

        random_arm = random.choice([(k, v) for k, v in self.valuations.items()])

        return random_arm

    def _select_best_arm(self):
        """
        Select the 'best' arm on the bandit by whatever
        style of bandit-method you implement.

        Uses the bandit's underlying valuation method to place
        a value estimate on each arm and then return the name of the
        arm that has the highest value

        :return: The name of the arm with the highest value.
        :rtype: str
        """
        arms = [(k, self.valuations[k]) for k in sorted(self.valuations,
                                                        key=self.valuations.get,
                                                        reverse=True)]
        return arms[0]

    @property
    def n_arms(self):
        """Returns the number of arms on the bandits"""
        return len(self.arms)

    def add_arm(self, arm, arm_name=None):
        """
        Add an arm to the bandit.

        Add an Arm instance to the bandit and optinally specify a
        name for the arm. Arms can be accessed with dictionary notation
        from the bandit's `arms` attribute. Returns the name of the arm that
        was added.

        :param arm: An instance of a hastur Arm class to be added to a bandit.
        :type arm: hastur.Arm
        :param arm_name: (optional) A name by which to refer to the arm.
        :type arm_name: str
        :return: The name of the arm that was added.
        :rtype: str
        """

        if not arm_name:
            arm_name = str(uuid.uuid4())

        assert isinstance(arm_name, str)

        self.arms[arm_name] = arm
        return arm_name

    def amputate(self, arm_name):
        """
        Removes the specified arm from the bandit.

        :param arm_name: The name of the arm to be removed.
        :type arm_name: str

        :return: The name of the arm that was removed
        :rtype: str
        """
        self.arms.pop(arm_name)
        return arm_name

    def disarm(self):
        """Remove all arms from the bandit"""

        self.arms = {}

    def reset_arms(self):
        """
        Reset all arms on the bandit.

        Calls the reset method on each arm. This eliminates
        all observations on the arm.
        """
        for arm in self.arms.values():
            arm.reset()

    @property
    def means(self):
        """
        Return the mean for each arm on the bandit.

        Calculates the mean of the observations for each arm and then
        returns a dictionary of {arm_name : mean} pairs.

        :return: A dictionary of {arm_name : mean} pairs.
        :rtype: dict
        """

        return {arm :self.arms[arm].mean for arm in self.arms}

    @property
    def variances(self):
        """
        Get a dictionary of the bandit's arms and their
        current variances.

        Calculatse the variance of the observations on each arm
        and then returns a dictionary of {arm_name: variance} pairs.

        :return: A dictionary of {arm_name : variance} pairs.
        :rtype: dict
        """

        return {arm :self.arms[arm].variance for arm in self.arms}

    @property
    def valuations(self):
        """
        Return the valuation for each arm on the bandit.

        Calculates the *value* for each of the arms on the bandit.
        This valuation is implemented differently by each bandit based
        on its methodology.

        :return: A dictionary of {arm_name: value} pairs.
        :rtype: dict
        """
        # base bandit has no strategy to implement.

        for arm in self.arms.values():
            if arm.is_empty:
                raise InsufficientObservationsError

        return {arm:float(0) for arm in self.arms}


class GreedyBandit(Bandit):
    """
    A greedy bandit always selects the best arm,
    where best is defined as the arm with the highest mean.
    """
    def __init__(self):
        super().__init__()

    def select_arm(self):
        """
        Greedy bandit's select arm method just falls back to
        the selection of the best arm. Which in turn is the
        highest mean value.
        """
        return self._select_best_arm()

    @property
    def valuations(self):
        """Values each arm based on the mean of its observations.

        :return: A dictionary of {arm_name: mean} pairs.
        :rtype: dict
        """

        for arm in self.arms.values():
            if arm.is_empty:
                raise InsufficientObservationsError
        return self.means


class EpsilonGreedyBandit(GreedyBandit):
    """
    A slight modification to a GreedyBandit. An EpsilonGreedyBandit
    is instantiated with an epsilon parameter between 0 and 1.
    When selecting an arm, it randomly selects a number
    between 0 and 1--if the randomly selected
    value is lower than epsilon, it picks a random arm.
    Otherwise, it uses a normal greedy selection mechanism
    and finds the highest expected value arm.

    Used to exploit high value arms while stil allowing
    for exploration.

    TL;DR. For more randomness, use a higher epsilon.

    :param epsilon: A number between 0 and 1 that controls how
                    frequently the Bandit will select a random arm instead of
                    the highest valued one. A bandit with an epsilon of .7 will
                    select a random arm seventy percent of the time.
    :type epsilon: float

    """
    def __init__(self, epsilon=0.1):
        super().__init__()
        self.epsilon = epsilon

    def select_arm(self):
        """
        Return the name of the selected arm.

        Compares a random value between 0 and 1 to
        the instances epsilon value. If greater than
        epsilon, selects the best arm. If less,
        selects a random arm. For an EpsilonGreedyBandit, best
        means the arm with the highest mean.

        :return: The name of the selected arm.
        :rtype: str

        """
        draw = random.random()
        if draw > self.epsilon:
            return self._select_best_arm()
        else:
            return self._select_random_arm()


class BayesianBandit(Bandit):
    """
    Bandit that uses random draws from a beta distribution
    to find the arm with the highest expected payoff.

    This bandit treats each of its arms as independent beta
    distributions, where the number of successes on the arm is the `a`
    parameter of the distribution and the number of failures on the arm
    is the `b` parameter of the distribution. The bandit then takes
    a random draw from the resulting distribution and uses that as the
    value of the arm. This helps to refine the confidence in the
    valuation over time while allowing some early exploration while
    distributions are likelier to significantly overlap.

    """
    def __init__(self):
        super().__init__()

    @property
    def valuations(self):
        """
        Returns values representing a random draw from a beta
        distribution with parameters created by successful and failed
        observations on that arm.

        :return: A dictionary of {arm_name: value}
        :rtype: dict
        """

        for arm in self.arms.values():
            if arm.is_empty:
                raise InsufficientObservationsError

        _valuations = {}
        for arm_name, distribution in self.distributions.items():
            arm_valuation = distribution.random_draw
            _valuations[arm_name] = arm_valuation
        return _valuations

    @property
    def distributions(self):
        """
        Create and return beta distributions for each of the arms
        on the bandit.

        Creates a paramterized beta distribution for each arm on the bandit
        by using the number of successes and failures on the arm to inform
        the initial distribution.

        Generate a dictionary of arms and their beta distributions

        :return: A dictionary of {arm_name: beta_distribution}
        :rtype: dict
        """

        _distributions = {}
        for arm_name, arm in self.arms.items():
            vals = [obs.value for obs in arm.observations]
            alphas = sum([1 if val == 1 else 0 for val in vals])
            betas = sum([1 if val == 0 else 0 for val in vals])
            beta_distribution = BetaDistribution(alpha=alphas, beta=betas)
            _distributions[arm_name] = beta_distribution

        return _distributions


class EpsilonBayesianBandit(BayesianBandit):
    """
    A Bandit that values arms by random draws
    from a beta distribution of their observations,
    but that also pulls a random arm with probability
    epsilon.
    """
    def __init__(self, epsilon=0.1):
        super().__init__()
        self.epsilon = epsilon

    def select_arm(self):
        """
        Compares a random value between 0 and 1 to
        the instances epsilon value. If greater than
        epsilon, selects the best arm. If less,
        selects a random arm.

        :return: The name of the selected arm.
        :rtype: str
        """
        draw = random.random()
        if draw > self.epsilon:
            return self._select_best_arm()
        else:
            return self._select_random_arm()


class UpperConfidenceBoundBandit(Bandit):
    """
    Uses an upper confidence bound based approach
    to estimating the optimistic value of an arm.

    Calculate the upper confidence bound for each arm as
    referenced by _UCB1_ in::

        Auer, P., Cesa-Bianchi, N. & Fischer,
        P. Machine Learning (2002) 47: 235. doi:10.1023/A:1013689704352
    """

    def __init__(self):
        super().__init__()

    @property
    def plays(self):
        """
        Returns a dictionary of each arm and how many observations
        are associated with that arm.

        :return: A dictionary of {arm: number_of_observations}
        :rtype: dict
        """
        return {arm:arm.size for arm in self.arms}

    @property
    def total_plays(self):
        """
        Returns the total number of observations that the bandit
        has seen. Count of all observations on all arms.

        :return: The total number of times an arm on the bandit has been played.
        :rtype: int
        """
        return int(sum([arm.size for arm in self.arms.values()]))

    def _ucb(self, arm_name):
        """Return the upper confidence bound for the arm.

        Calculate the upper confidence bound for each arm as
        referenced by _UCB1_ in::

            Auer, P., Cesa-Bianchi, N. & Fischer,
            P. Machine Learning (2002) 47: 235. doi:10.1023/A:1013689704352

        for the observations contained on the arm. Acts as an optimistic point estimate
        of the distribution's *true* value.

        :param arm_name: the name of the arm for which to calculate the UCB
        :type arm_name: string
        :return: the upper confidence bound of the observations in the arm.
        :rtype: float
        """

        arm = self.arms[arm_name]
        x_j = arm.mean
        n_j = arm.size
        total_n = self.total_plays

        if n_j == 0 or total_n == 0:
            raise InsufficientObservationsError("At least one arm contains no observations.")

        numerator = 2*math.log(total_n)
        denominator = n_j

        val = float(x_j + math.sqrt(numerator/denominator))

        return val

    @property
    def valuations(self):
        """Creates a valuation dictionary for each arm by UCB.

        For each arm on the bandit, value it by the upper confidence
        bound of its observations.

        Raises a InsufficientObservationsError if at least one arm contains
        no observations.

        :return: a dictionary of {arm_name: ucb_value}
        :rtype: dict
        :raises: InsufficientObservationsError. At least one arm contains no observations
        """

        for arm in self.arms.values():
            if arm.size == 0:
                raise InsufficientObservationsError("Bandit owns at least one empty arm.")

        return {arm_name:self._ucb(arm_name) for arm_name in self.arms}

if __name__ == '__main__':
    pass
    