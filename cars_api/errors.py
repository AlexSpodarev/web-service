from cars_api import app
from flask import request, abort


def reject_invalid_request(code=404):
    """
    +-------------------------------------------------------------------------------------------------------------------
    | This function is designed to reduce the lines of logic in the routes by
    | Having a generic method to abort requests, when needed, just call reject_invalid_request
    | A log message will be printed and the request rejected with a 404 not found by default
    | Can be changed by calling the function with a different code example: reject_invalid_request(500)
    +-------------------------------------------------------------------------------------------------------------------
    """
    app.logger.info(f"Invalid Request:{request} - Dropping with code: {code}")
    abort(code)
