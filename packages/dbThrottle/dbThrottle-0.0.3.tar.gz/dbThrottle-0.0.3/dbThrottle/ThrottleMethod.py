import sqlalchemy, random

"""
ThrottleMethod: Default methods for throttling metrics.
"""

class ThrottleMethod(object):
    """
    ThrottleMethod: Default methods for throttling metrics.
    """

    @staticmethod
    def test_metric(host, *args):
        """Return a random number to test against, (0,1)."""
        return random.random()

    @staticmethod
    def mysql_replica_lag(host, *args):
        """Check the mysql replica lag."""
        pass

    @staticmethod
    def mysql_threads(host, *args):
        """Check the number of mysql threads."""
        pass

    @staticmethod
    def postgresql_replica_lag(host, *args):
        """Check the postgresql replica lag."""
        pass

    @staticmethod
    def postgresql_threads(host, *args):
        """Check the number of postgresql threads."""
        pass

    @staticmethod
    def mssql_replica_lag(host, *args):
        """Check the mssql replica lag."""
        pass

    @staticmethod
    def mssql_threads(host, *args):
        """Check the number of mssql threads."""
        pass

    @staticmethod
    def oracle_replica_lag(host, *args):
        """Check the oracle replica lag."""
        pass

    @staticmethod
    def oracle_threads(host, *args):
        """Check the number of mssql threads."""
        pass
