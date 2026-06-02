from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:

        message = "Request failed"

        if isinstance(response.data, dict):

            if "detail" in response.data:
                message = response.data["detail"]

            else:
                first_error = next(iter(response.data.values()))

                if isinstance(first_error, list):
                    message = first_error[0]

        response.data = {
            "status": False,
            "message": message,
            "data": response.data
        }

    return response