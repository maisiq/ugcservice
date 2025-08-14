from os import getenv

# CORE SETTINGS
API_DEBUG = getenv('API_DEBUG', False)
LOGGER_LEVEL = getenv('LOGGER_LEVEL', 'DEBUG')

# MONITORING
SENTRY_DSN = getenv('SENTRY_DSN')
