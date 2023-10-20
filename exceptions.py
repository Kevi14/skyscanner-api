from datetime import datetime
from enum import Enum
from typing import List
from uuid import uuid4
from rest_framework import exceptions
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status as HttpStatus
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class ErrorStatus(Enum):
    """Defines error status based on API standards."""

    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    DEADLINE_EXCEEDED = "DEADLINE_EXCEEDED"
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    UNAUTHENTICATED = "UNAUTHENTICATED"
    RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"
    FAILED_PRECONDITION = "FAILED_PRECONDITION"
    ABORTED = "ABORTED"
    OUT_OF_RANGE = "OUT_OF_RANGE"
    UNIMPLEMENTED = "UNIMPLEMENTED"
    INTERNAL = "INTERNAL"
    UNAVAILABLE = "UNAVAILABLE"
    DATA_LOSS = "DATA_LOSS"


# mapping between error status and HTTP status according to API standards
MAP_ERROR_STAT_TO_HTTP_STAT = {
    ErrorStatus.CANCELLED: 499,  # no HttpStatus available
    ErrorStatus.UNKNOWN: HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR,
    ErrorStatus.INVALID_ARGUMENT: HttpStatus.HTTP_400_BAD_REQUEST,
    ErrorStatus.DEADLINE_EXCEEDED: HttpStatus.HTTP_504_GATEWAY_TIMEOUT,
    ErrorStatus.NOT_FOUND: HttpStatus.HTTP_404_NOT_FOUND,
    ErrorStatus.ALREADY_EXISTS: HttpStatus.HTTP_409_CONFLICT,
    ErrorStatus.PERMISSION_DENIED: HttpStatus.HTTP_403_FORBIDDEN,
    ErrorStatus.UNAUTHENTICATED: HttpStatus.HTTP_401_UNAUTHORIZED,
    ErrorStatus.RESOURCE_EXHAUSTED: HttpStatus.HTTP_429_TOO_MANY_REQUESTS,
    ErrorStatus.FAILED_PRECONDITION: HttpStatus.HTTP_400_BAD_REQUEST,
    ErrorStatus.ABORTED: HttpStatus.HTTP_409_CONFLICT,
    ErrorStatus.OUT_OF_RANGE: HttpStatus.HTTP_400_BAD_REQUEST,
    ErrorStatus.UNIMPLEMENTED: HttpStatus.HTTP_501_NOT_IMPLEMENTED,
    ErrorStatus.INTERNAL: HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR,
    ErrorStatus.UNAVAILABLE: HttpStatus.HTTP_503_SERVICE_UNAVAILABLE,
    ErrorStatus.DATA_LOSS: HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR,
}

MAP_DJANGO_DEFAULT_CODES_TO_API_STANDARDS_ERROR_STATUS = {
    "invalid": ErrorStatus.INVALID_ARGUMENT,
    "method_not_allowed": ErrorStatus.PERMISSION_DENIED,
    "not_found": ErrorStatus.NOT_FOUND,
    "error": ErrorStatus.INTERNAL,  # error is the default django APIException
}


class CustomAPIException(exceptions.APIException):
    pass


class CancelledException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.CANCELLED]
    default_code = ErrorStatus.CANCELLED.value
    default_detail = "The operation was cancelled."


class UnknownException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.UNKNOWN]
    default_code = ErrorStatus.UNKNOWN.value
    default_detail = "An unknown error occured."


class InvalidArgumentException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.INVALID_ARGUMENT]
    default_code = ErrorStatus.INVALID_ARGUMENT.value
    default_detail = "Invalid argument provided."


class DeadlineExceededException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.DEADLINE_EXCEEDED]
    default_code = ErrorStatus.DEADLINE_EXCEEDED.value
    default_detail = "The deadline expired before the operation could complete."


class NotFoundException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.NOT_FOUND]
    default_code = ErrorStatus.NOT_FOUND.value
    default_detail = "The requested entity was not found."


class AlreadyExistsException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.ALREADY_EXISTS]
    default_code = ErrorStatus.ALREADY_EXISTS.value
    default_detail = "The entity already exists."


class PermissionDeniedException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.PERMISSION_DENIED]
    default_code = ErrorStatus.PERMISSION_DENIED.value
    default_detail = "You do not have the permission to execute this operation."


class UnauthenticatedException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.UNAUTHENTICATED]
    default_code = ErrorStatus.UNAUTHENTICATED.value
    default_detail = (
        "The request does not have valid authentication credentials for the operation."
    )


class ResourceExhaustedException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.RESOURCE_EXHAUSTED]
    default_code = ErrorStatus.RESOURCE_EXHAUSTED.value
    default_detail = "The requested resource is exhausted."


class FailedPreconditionException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.FAILED_PRECONDITION]
    default_code = ErrorStatus.FAILED_PRECONDITION.value
    default_detail = (
        "the system is not in a state required for the operation's execution."
    )


class AbortedException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.ABORTED]
    default_code = ErrorStatus.ABORTED.value
    default_detail = "The operation was aborted."


class OutOfRangeException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.OUT_OF_RANGE]
    default_code = ErrorStatus.OUT_OF_RANGE.value
    default_detail = "The operation was attempted past the valid range."


class UnimplementedException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.UNIMPLEMENTED]
    default_code = ErrorStatus.UNIMPLEMENTED.value
    default_detail = (
        "The operation is not implemented or is not supported/enabled in this service."
    )


class InternalException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.INTERNAL]
    default_code = ErrorStatus.INTERNAL.value
    default_detail = "Internal."


class UnavailableException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.UNAVAILABLE]
    default_code = ErrorStatus.UNAVAILABLE.value
    default_detail = "The service is currently unavailable."


class DataLossException(CustomAPIException):
    status_code = MAP_ERROR_STAT_TO_HTTP_STAT[ErrorStatus.DATA_LOSS]
    default_code = ErrorStatus.DATA_LOSS.value
    default_detail = "Loss of data or corrupted data occured."


class APIStandardError:
    """Error message provided by API standards."""

    message: str
    status: str
    id: str
    timestamp: str
    code: int
    details: List[str]

    def __init__(self, message: str, status: ErrorStatus, details: List[str] = None):
        self.message = message
        self.status = status.value
        self.id = str(uuid4())
        self.timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.code = MAP_ERROR_STAT_TO_HTTP_STAT[status]
        if details:
            self.details = details


def custom_exception_handler(exc, context):
    """Tweaks exceptions into api standard conform error responses.

    Args:
        exc: The exception.
        context: Source of call.

    Returns:
        response: Response
    """
    response = exception_handler(exc, context)
    if response is not None:
        if isinstance(exc, CustomAPIException):
            # custom defined exceptions (should always have default code)

            custom_error = APIStandardError(
                message=str(exc), status=ErrorStatus(exc.default_code)
            )
        else:
            # django defined exception
            # map django exception to our allowed exceptions
            # problematic if we have more error codes with same status codes
            # -> mapping ambiguous
            # If we have no error code at all, returns unknown
            if (
                hasattr(exc, "default_code")
                and exc.default_code
                in MAP_DJANGO_DEFAULT_CODES_TO_API_STANDARDS_ERROR_STATUS
            ):
                # fist, try to make sense of default code provided by django
                error_status = MAP_DJANGO_DEFAULT_CODES_TO_API_STANDARDS_ERROR_STATUS[
                    exc.default_code
                ]
                custom_error = APIStandardError(message=str(exc), status=error_status)

            else:
                # If lookup by default code doesn't work, take status code as best guess
                # to estimate error status
                supported_error_status = [
                    k
                    for k, v in MAP_ERROR_STAT_TO_HTTP_STAT.items()
                    if int(v) == response.status_code
                ]

                if len(supported_error_status) == 1:
                    # If one status code matches, take its error status
                    custom_error = APIStandardError(
                        message=str(exc), status=supported_error_status[0]
                    )

                elif len(supported_error_status) > 1:
                    # If multiple error status have the same status code return the first
                    # and provide all possible status as detail
                    print(exc)
                    print("type of exc", type(exc))
                    details = [
                        (
                            "Couldn't clearly distinguish status. Can be one of "
                            + str([(elem.value) for elem in supported_error_status])
                            + "."
                        )
                    ]
                    custom_error = APIStandardError(
                        message=str(exc),
                        status=supported_error_status[0],
                        details=details,
                    )

                else:  # len(supported_error_status) == 0:
                    # If no status code equals, return unknown error code
                    custom_error = APIStandardError(
                        message=str(exc), status=ErrorStatus.UNKNOWN
                    )
    # validation errors
    elif isinstance(exc, ValidationError):
        # map validation errors to invalid argument error status
        # validation error are special since default exception_handler doesn't provide
        # response

        custom_error = APIStandardError(
            message=str(exc.message_dict).replace("{", "").replace("}", ""),
            status=ErrorStatus.INVALID_ARGUMENT,
        )
        response = Response()

    elif isinstance(exc, IntegrityError):
        msgs = ""
        if len(exc.args) > 1:
            for i, arg in enumerate(exc.args):
                msgs += f"Error {i+1}: {arg}\n"

        else:
            msgs += exc.args[0]
        custom_error = APIStandardError(
            message=msgs, status=ErrorStatus.INVALID_ARGUMENT
        )
        response = Response()
    elif isinstance(exc, AssertionError):
        msgs = exc.args[0]
        custom_error = APIStandardError(message=msgs, status=ErrorStatus.INTERNAL)
        response = Response()
    else:
        # return default error "unknown if we don't know whats going on"
        custom_error = APIStandardError(
            message=str(exc.message_dict),
            status=ErrorStatus.UNKNOWN,
        )
        response = Response()

    # update error dict and adjust status code
    response.data = {"error": vars(custom_error)}
    response.status_code = custom_error.code
    return response
