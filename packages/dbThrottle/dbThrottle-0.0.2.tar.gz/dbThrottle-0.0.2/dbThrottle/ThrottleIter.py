"""
ThottleIter: Throttle execution through an iterable.
"""

from dbThrottle.ThrottleObject import ThrottleObject

class ThrottleIter(ThrottleObject):
    """
    ThottleIter: Throttle execution through an iterable.
    """

    def __init__(self, iterable, performer, throttle):
        """
        Initalize the Throttle Iterator Object.
        Take in the iterable, function, and throttling settings.
        Call the parent ThrottleObject to perform throttling.
        """
        # get parent
        self.parent = "?"
        # call parent __init__ using all in throttle
        # figure out if I want throttle to be list or list/dict.
        self.iterable = iterable
        self.performer = performer

    def __iter__(self):
        """Python required to return self."""
        return self

    def __next__(self):
        """Throttled iterator, get next where applicable."""
        try:
            nextval = next(self.iterable)
            # if the db should be throttled, return a special value
            if not self.parent.okay():
                return -1  # make better return code?
            else:
                return self.perfomer(nextval)
        except StopIteration:
            # log this, then re-raise
            raise StopIteration("Iterable object in\
                                ThrottleIter has rached StopIteration")

    def __str__(self):
        """Return a stringification of this ThrottleIter instance."""
        # TODO make more like standard iterable
        strout = "<ThrottleIter object with iterable {0} and \
        performer {1}>".format(self.iterable, self.perfomer)
        return strout
