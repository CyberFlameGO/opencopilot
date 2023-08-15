import pytest
from uuid import UUID, uuid4
from src.service.error_responses import ValidationAPIError
from src.service.utils import get_uuid


def test_get_valid_uuid():
    # Generate a random UUID and convert to string
    valid_uuid = str(uuid4())
    assert get_uuid(valid_uuid) == UUID(valid_uuid)


def test_get_invalid_uuid():
    # Test with an invalid UUID
    invalid_uuid = "not a uuid"
    with pytest.raises(ValidationAPIError):
        get_uuid(invalid_uuid)

