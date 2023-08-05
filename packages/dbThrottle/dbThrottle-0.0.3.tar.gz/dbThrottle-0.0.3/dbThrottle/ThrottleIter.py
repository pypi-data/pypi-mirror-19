"""
ThottleIter: Throttle execution through an iterable.
"""

from dbThrottle.ThrottleObject import ThrottleObject

class ThrottleIter(ThrottleObject):
    """
    ThottleIter: Throttle execution through an iterable.
    Inputs:
        iterable - the iterable to act on
        performer - the function to take action on the iterator
        throttle - arguments to parent ThrottleObject

    Call the parent ThrottleObject to perform throttling.
    Throttle can be either a list or a dict,
    and should align with arguments for ThrottleObject.
    The iterator will return -1 if no action is taken.
    """

    def __init__(self, iterable, performer, throttle):
        """
        Initalize the Throttle Iterator Object.
        """
        # get parent
        self.parent = super(ThrottleIter, self)
        # call parent __init__ using all in throttle
        if type(throttle) is dict:
            self.parent.__init__(**throttle)
        else:
            self.parent.__init__(*throttle)
        # figure out if I want throttle to be list or list/dict.
        self.iterable = iterable
        self.performer = performer

    def __iter__(self):
        """Return the iterator object."""
        return self

    def __next__(self):
        """
        Throttled iterator, get next where applicable.
        Returns -1 to represent no action taken.
        """
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
