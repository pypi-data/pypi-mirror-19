# coding: utf-8
from pypika import terms
from . import Database


class Trunc(terms.Function):
    # Wrapper for Vertica TRUNC function for truncating dates.

    def __init__(self, field, date_format, alias=None):
        super(Trunc, self).__init__('TRUNC', field, date_format, alias=alias)


class Vertica(Database):
    # Vertica client that uses the vertica_python driver.

    def __init__(self, host='localhost', port=5433, database='vertica',
                 user='vertica', password=None,
                 read_timeout=None):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.read_timeout = read_timeout

    def connect(self):
        import vertica_python

        return vertica_python.connect(
            host=self.host, port=self.port, database=self.database,
            user=self.user, password=self.password,
            read_timeout=self.read_timeout,
        )

    def trunc_date(self, field, interval):
        return Trunc(field, interval)
