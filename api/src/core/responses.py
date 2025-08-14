from fastapi import status

NOT_FOUND_RESPONSE = {
    404: {
        'description': 'Entity not found',
        'content': {
            'application/json': {
                'example': {'detail': 'User not found'},
            },
        },
    },
}

SERVICE_UNAVAILABLE_RESPONSE = {
    status.HTTP_503_SERVICE_UNAVAILABLE: {
        'description': 'Service is unavailable',
        'content': {
            'application/json': {
                'example': {'detail': 'Service temporary unavailable'},
            },
        },
    },
}

DEFAULT_RESPONSES = {
    **SERVICE_UNAVAILABLE_RESPONSE,
}
