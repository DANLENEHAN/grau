from werkzeug.exceptions import HTTPException


class GrauException(HTTPException):
    """Base class for all exceptions raised by Grau."""

    code = 500
    description = "An error occurred."

    def __init__(self, message=None, data=None, response=None):
        """Initializes the exception."""
        self.message = message
        self.data = data

    def to_dict(self):
        """Returns a dictionary representation of the exception."""
        return {
            "message": self.message or self.description,
            "data": self.data,
        }

    def __str__(self):
        """Returns the string representation of the exception."""
        return self.message

    def __repr__(self) -> str:
        return super().__repr__()


class ResourceNotFound(GrauException):
    """Exception raised when a resource is not found."""

    code = 404
    description = "Resource not found."

    def __init__(self, message=None, data=None):
        """Initializes the exception."""
        super().__init__(message, data)


class ResourceAlreadyExists(GrauException):
    """Exception raised when a resource already exists."""

    code = 409
    description = "Resource already exists."

    def __init__(self, message=None, data=None):
        """Initializes the exception."""
        super().__init__(message, data)


class BadRequest(GrauException):
    """Exception raised when a bad request is made."""

    code = 400
    description = "Bad request."

    def __init__(self, message=None, data=None):
        """Initializes the exception."""
        super().__init__(message, data)
