import sqlalchemy

"""
ThrottleMethod: Default methods for throttling metrics.
"""

class ThrottleMethod(Object):
    """
    ThrottleMethod: Default methods for throttling metrics.
    """

    @classmethod
    def mysql_replica_lag(host, *args):
        """Check the mysql replica lag."""
        pass

    @classmethod
    def mysql_threads(host, *args):
        """Check the number of mysql threads."""
        pass
