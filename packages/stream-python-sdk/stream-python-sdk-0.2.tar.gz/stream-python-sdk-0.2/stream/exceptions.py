# -*- coding:utf8 -*-

class StreamException(Exception):
    """
    Base class for all exceptions raised by this package's operations.
    """

class ClientException(StreamException):
    """
    Exception raised when there was an exception while SDK client working.
    """
    @property
    def error(self):
        return self.args[0]

    @property
    def info(self):
        return self.args[1]

    @property
    def message(self):
        return '%s(%s) caused by: %s(%s)' % (
            self.__class__.__name__,
            self.error,
            self.info.__class__.__name__,
            self.info
        )

    def __str__(self):
        return self.message

class ServiceException(StreamException):
    """
    Exception raised when NOS returns a non-OK (>=400) HTTP status code.
    """
    @property
    def status_code(self):
        return self.args[0]

    @property
    def error_type(self):
        return self.args[1]

    @property
    def error_code(self):
        return self.args[2]

    @property
    def request_id(self):
        return self.args[3]

    @property
    def message(self):
        return self.args[4]

    def __str__(self):
        return '%s(%s, %s, %s, %s, %s)' % (
            self.__class__.__name__,
            self.status_code,
            self.error_type,
            self.error_code,
            self.request_id,
            self.message
        )

class InvalidParameter(ClientException):
    """
    Exception raised when subscription name is invalid.
    """

    def __init__(self, parameter_name):
        self.parameter_name = parameter_name
        
    @property
    def error(self):
        pass

    @property
    def info(self):
        pass

    @property
    def message(self):
        return 'InvalidParameter caused by: %s is illegal.' \
            % self.parameter_name

    def __str__(self):
        return self.message

class ConnectionError(ClientException):
    """
    Error raised when there was an exception while talking to Stream server.
    """

class ConnectionTimeout(ConnectionError):
    """ A network timeout. """

class SerializationError(ClientException):
    """
    Data passed in failed to serialize properly in the Serializer being
    used.
    """