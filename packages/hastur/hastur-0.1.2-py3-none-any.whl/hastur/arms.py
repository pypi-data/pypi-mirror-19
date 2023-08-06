# -*- coding: utf-8 -*-
"""
Arm objects for multi-armed bandit models. An arm is a container class
that holds observations (results from binary tests). It provides convenience
functions for handling and analyzing the observations it contains as well as some
control flows for constraining the maximum number of observations.
"""
import statistics
import math
from hastur.exceptions import InsufficientObservationsError
from hastur.exceptions import ExcessiveObservationsError


class Arm(object):
    """
    An arm is a container class that holds observations
    (results from binary tests). It provides convenience functions for
    handling and analyzing the observations it contains as well as some
    control flows for constraining the maximum number of observations.
    """
    def __init__(self, maxsize=None):
        self.observations = []

        if not maxsize:
            self.maxsize = math.inf
        else:
            self.maxsize = maxsize

    @property
    def size(self):
        """
        Returns the number of observations on the arm.

        :return: The number of observations on the arm.
        :rtype: int
        """
        return len(self.observations)

    @property
    def is_empty(self):
        """Return True if the arm contains no observations"""
        return len(self.observations) == 0

    @property
    def is_full(self):
        """Return True if the arm has observations >= its maxsize."""
        if self.size >= self.maxsize:
            return True
        else:
            return False

    def update(self, observation):
        """
        Used to update an arm with a single new observation.

        Just appends a new observation to the arm's observation list.
        If an arm is full, this will raise an ExcessiveObservationsError.

        :param observation: The new observation to add to the arm.
        :type observation: hastur.Observation
        :raises: ExcessiveObservationsError. Raised if the arm is full when
                 trying to update it.
        """
        if self.is_full:
            raise ExcessiveObservationsError('Arm is full and cannot accept observations.')

        self.observations.append(observation)

    def reset(self):
        """Clear all observations from the arm."""
        self.observations = []

    @property
    def values(self):
        """Return a list of all the values of the observations on the arm."""
        return [obv.value for obv in self.observations]

    @property
    def mean(self):
        """
        Returns the mean of the current observations.

        Calculates the mean of the observations currently on the arm. Will raise
        a InsufficientObservationsError if the arm is empty.

        :return: The mean of the observations on the arm.
        :rtype: float
        :raises: InsufficientObservationsError. Raised when the arm contains no observations.
        """
        if self.is_empty:
            raise InsufficientObservationsError("Cannot compute mean of an empty sequence")

        return float(statistics.mean(self.values))

    @property
    def variance(self):
        """
        Returns the variance of the current observations.

        Calculates the variance for all of the values of the observations
        currently on the arm. Will raise a InsufficientObservationsError if there
        are less than two observations on the arm.

        :return: The variance of the observations on the arm.
        :rtype: float
        :raises: InsufficientObservationsError. Raised when there are less
                 than two observations on the arm.
        """

        if self.size < 2:
            raise InsufficientObservationsError

        return float(statistics.variance(self.values))



if __name__ == '__main__':
    pass
