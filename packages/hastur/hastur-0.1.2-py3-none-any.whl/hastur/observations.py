# -*- coding: utf-8 -*-
"""
This module provides observation classes that can be used
for multi-armed bandits.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""



import datetime


class Observation(object):
    """
    A single observation for a multi-armed bandit.

    Custom container class that holds the results of a binary
    experiment for a multi-armed bandit arm.

    :param value: The value of the observation. :math: value `\in [0,1]`
    :type value: int
    :param source: (optional) The source of the observation, possibly
                              a unique identifier for the person or
                              item that generated it. defaults to ''.
    :type source: str
    :param dt: (optional) When the observation was observed.
                          Defaults to today.
    :type dt: datetime.datetime
    """
    def __init__(self, value, source=None, dt=None):

        if not source:
            source = ''

        if not dt:
            dt = datetime.datetime.today()

        if value not in (0, 1):
            raise ValueError("Observation must be 0 or 1.")

        assert isinstance(dt, datetime.datetime)
        assert isinstance(value, int)
        assert isinstance(source, str)


        self.value = value
        self.source = source
        self.date = dt

    def __str__(self):
        return {'value': self.value,
                'source': self.source,
                'date': self.date}

    def __eq__(self, other):
        if (other.value == self.value and
                other.source == self.source and
                other.date == self.date):
            return True
        else:
            return False

    def __ne__(self, other):
        if not (other.value == self.value and
                other.source == self.source and
                other.date == self.date):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.value, self.source, self.date))

if __name__ == "__main__":
    pass
    