from werkzeug.exceptions import HTTPException

from grau.db.enums import StatusCode


class GrauException(HTTPException):
    """Base class for all exceptions raised by Grau."""

    code = StatusCode.INTERNAL_SERVER_ERROR.value
    description = "An error occurred."

    def __init__(self, message=None, data=None, response=None):
        """Initializes the exception."""
        self.message = message
        self.data = data
        super().__init__(self.description, response)

    def to_dict(self):
        """Returns a dictionary representation of the exception."""
        return {
            "message": self.message or self.description,
            "data": self.data,
        }

    def __str__(self):
        """Returns the string representation of the exception."""
        return self.message


class ResourceNotFound(GrauException):
    """Exception raised when a resource is not found."""

    code = StatusCode.NOT_FOUND.value
    description = "Resource not found."

    def __init__(self, message=None, data=None):
        """Initializes the exception."""
        super().__init__(message, data)


class ResourceAlreadyExists(GrauException):
    """Exception raised when a resource already exists."""

    code = StatusCode.CONFLICT.value
    description = "Resource already exists."

    def __init__(self, message=None, data=None):
        """Initializes the exception."""
        super().__init__(message, data)


class BadRequest(GrauException):
    """Exception raised when a bad request is made."""

    code = StatusCode.BAD_REQUEST.value
    description = "Bad request."

    def __init__(self, message=None, data=None):
        """Initializes the exception."""
        super().__init__(message, data)
