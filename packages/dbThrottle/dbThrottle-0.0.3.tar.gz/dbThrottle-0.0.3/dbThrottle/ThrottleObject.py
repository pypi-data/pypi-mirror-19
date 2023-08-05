"""
ThottleObject: Base class for throttable objects.
"""

class ThrottleObject(object):
    """
    ThrottleObject: Base class for throttable objects.

    Inputs:
        The address of a host to check
        The method to use for a metric
        Threshold to measure metric result against.

    If method() returns greater than threshold,
    the db is in "throttle mode".
    In "throttle mode", child objects should not act; just wait.

    """
    def __init__(self, host, method, threshold):
        """
        Initalize the Throttle Object.
        Take in the host to check, the method to use to monitor,
        and the threshold value for that metric.
        If method() returns greater than threshold,
        the db is in "throttle mode".
        In "throttle mode", child objects should not act; just wait.
        """
        self.host = host
        self.method = method
        self.threshold = threshold

    def okay(self, *args):
        """
        Return a bool if it is okay to procced.
        Can take in custom arguments for the method.
        """
        return self.method(self.host, *args) < self.threshold
