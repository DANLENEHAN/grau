from typing import Union

from flask import jsonify

from grau.db.enums import RequestType, StatusCode
from grau.handlers.grau_exceptions import GrauException


class APIResponseHandler:
    """
    This class handles API responses.
    """

    def __init__(
        self, request_type: RequestType, response_body: Union[dict, str] = ""
    ):
        self.request_type = request_type
        self.response_body = response_body
        self.response = self.get_response()

    def get_response(self) -> tuple[Union[dict, str], int]:
        """
        Creates a success response.
        Args:
                self (APIResponseHandler): APIResponseHandler object
        Returns:
                dict: Response dictionary
        """

        match self.request_type:
            case RequestType.GET:
                status_code = StatusCode.SUCCESS
            case RequestType.POST:
                match self.response_body:
                    case None:
                        status_code = StatusCode.ACCEPTED
                    case _:
                        status_code = StatusCode.CREATED
            case RequestType.PUT:
                match self.response_body:
                    case None:
                        status_code = StatusCode.ACCEPTED
                    case _:
                        status_code = StatusCode.CREATED
            case RequestType.DELETE:
                status_code = StatusCode.NO_CONTENT
            case _:
                status_code = StatusCode.SUCCESS

        return (
            jsonify(self.response_body)
            if isinstance(self.response_body, dict)
            else self.response_body,
            status_code.value,
        )


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
