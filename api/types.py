"""
Типы нужные
"""


import enum


class REQUEST_TYPE(int, enum.Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4
    PATCH = 5
