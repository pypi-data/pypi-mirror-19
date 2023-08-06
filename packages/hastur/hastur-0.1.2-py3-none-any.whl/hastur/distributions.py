# -*- coding: utf-8 -*-
"""
This module provides classes that provide functionality for different
statistical distributions.
"""
import random
from hastur.exceptions import InsufficientObservationsError


class BetaDistribution(object):

    def __init__(self, alpha=1, beta=1):
        """
        A distribution over probabilities.
        Instantiante with alpha equal to the number of
        observed successes and beta equal to the number of
        observed failures.

        :param alpha: Alpha (or `a`) parameter of a beta distribution. The number
                    of 'successful' observations.
        :type alpha: int
        :param beta: Beta (or `b`) parameter of a beta distribution. The number of
                    'failed' observations.
        :type beta: int
        """
        self.alpha = alpha
        self.beta = beta

    @property
    def n_obs(self):
        """Return the total number of observations (alpha + beta)."""
        return self.alpha+self.beta

    @property
    def mode(self):
        """
        Attribute that returns the highest density
        probability from the distribution.

        Finds the likeliest single value for a random draw
        from the beta distribution. Calculated by (alpha-1 / n_obs-2).

        :return: The most probable value from the beta distribution.
        :rtype: float
        :raises: InsufficientObservationsError. Raised if n_obs is less than 3.
        """

        if self.n_obs < 3:
            raise InsufficientObservationsError

        return float((self.alpha - 1)/(self.n_obs - 2))

    def update(self, value):
        """
        Update the prior with a new observation.
        Increments the alpha or beta parameter of the
        distribution as appropriate.

        :param value: An integer describing the success or failure (0 or 1).
        :type value: int
        """
        assert isinstance(value, int)
        assert value == 1 or value == 0

        if value == 1:
            self.alpha += 1
        if value == 0:
            self.beta += 1

    @property
    def random_draw(self):
        """
        Return a single random sample from the distribution.

        Uses the current alpha and beta values of the distribution
        to return a single draw from a parameterized beta distribution.

        :return: The value returned from a single random sample from
                 the distribution
        :rtype: int
        :raises: InsufficientObservationsError. Raised when either alpha
                 or beta are 0.
        """

        if self.alpha == 0 or self.beta == 0:
            raise InsufficientObservationsError("Alpha \
            and beta must both be strictly positive.")

        draw = random.betavariate(alpha=self.alpha, beta=self.beta)
        return draw

if __name__ == "__main__":
    pass
