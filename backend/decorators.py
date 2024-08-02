from functools import wraps
from flask import jsonify, make_response


def format_response(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Execute the original function and get the response and status code
        response = func(*args, **kwargs)

        # Check if the response is a tuple, if so, extract the status code
        if isinstance(response, tuple):
            data, status_code = response
        else:
            data = response
            status_code = 200  # Default status code

        # Define status messages
        status_messages = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
        }

        # Get the status message corresponding to the status code
        status_message = status_messages.get(status_code, "Unknown Status")

        # Create the formatted response
        formatted_response = {
            "Status": status_code,
            "State": status_message,
            "Data": data
        }

        # Return the formatted response
        return make_response(jsonify(formatted_response), status_code)

    return decorated_function
