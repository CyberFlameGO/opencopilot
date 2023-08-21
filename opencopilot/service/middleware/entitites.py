from enum import Enum


class RequestStateKey(str, Enum):
    """
    Keys for using request store to transfer information between http middlewares
    """
    REQUEST_ID = "request_id"
    REQUEST_SOURCE = "request_source"
    REQUEST_ORIGIN = "request_origin"
    REQUEST_USER_AGENT = "request_user_agent"
    IP_ADDRESS = "ip_address"
    COUNTRY = "country"
