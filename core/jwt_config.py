from datetime import timedelta

JWT_SETTINGS = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=5),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
