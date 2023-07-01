from flask import jsonify

from grau.exceptions.grau_exceptions import GrauException


def handle_grau_exception(exception: type[GrauException]):
    """
    Handles a GrauException.
    Args:
            exception (GrauException): Exception to handle
    Returns:
            dict: Response dictionary
    """
    return (
        jsonify(
            {
                "message": exception.message,
                "data": exception.data,
            }
        ),
        exception.code,
    )
