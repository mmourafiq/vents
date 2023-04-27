import abc


class BaseService(abc.ABC):
    def __init__(self, connection=None, **kwargs):
        self._connection = connection
        self._connection_type = kwargs.get("connection_type")

    @property
    def connection_type(self):
        return self._connection_type

    @property
    def connection(self):
        if self._connection is None:
            # Create connection with defaults
            self.set_connection()
        return self._connection

    @abc.abstractmethod
    def set_connection(self, **kwargs):
        raise NotImplementedError
