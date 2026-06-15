from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:

        error_message = "An error occurred"

        if isinstance(response.data, dict):

            if 'detail' in response.data:
                error_message = str(response.data['detail'])

            elif 'non_field_errors' in response.data:
                error_message = str(response.data['non_field_errors'][0])

            else:
                # handles field-level validation errors
                # e.g. {"email": ["This field is required"]}
                errors = []
                for field, messages in response.data.items():
                    if isinstance(messages, list):
                        errors.append(f"{field}: {messages[0]}")
                    else:
                        errors.append(f"{field}: {messages}")
                error_message = ", ".join(errors)

        elif isinstance(response.data, list):
            error_message = str(response.data[0])

        response.data = {
            "success": False,
            "message": error_message,
            "data": None
        }

    return response

def api_response(success, message, data, status):

    return Response(
        {
            "success": success,
            "message": message,
            "data": data
        },
        status=status
    )