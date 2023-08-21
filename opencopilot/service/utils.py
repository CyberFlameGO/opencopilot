from uuid import UUID
from opencopilot.service.error_responses import ValidationAPIError


def get_uuid(_id: str, param: str = "") -> UUID:
    try:
        return UUID(_id)
    except:
        raise ValidationAPIError(
            param=param
        )
