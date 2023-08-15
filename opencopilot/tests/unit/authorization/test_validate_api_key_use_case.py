import pytest
from unittest.mock import patch
from src.service import error_responses
import src.authorization.validate_api_key_use_case as use_case


@patch("src.authorization.validate_api_key_use_case.settings")
@pytest.mark.asyncio
async def test_execute_no_api_key(mock_settings):
    with pytest.raises(error_responses.AuthorizationMissingAPIError):
        await use_case.execute(api_key_header=None)


@patch("src.authorization.validate_api_key_use_case.settings")
@pytest.mark.asyncio
async def test_execute_invalid_api_key(mock_settings):
    mock_settings.API_KEY = "Valid key"
    with pytest.raises(error_responses.AuthorizationMissingAPIError):
        await use_case.execute(api_key_header="Invalid key")


@patch("src.authorization.validate_api_key_use_case.settings")
@patch("src.authorization.validate_api_key_use_case._validate_jwt")
@pytest.mark.asyncio
async def test_execute_bearer_api_key(mock_validate_jwt, mock_settings):
    mock_validate_jwt.return_value = "sub_value"
    result = await use_case.execute(api_key_header="Bearer valid_token")
    mock_validate_jwt.assert_called_once_with("valid_token")
    assert result == "sub_value"


@patch("src.authorization.validate_api_key_use_case.settings")
@patch("src.authorization.validate_api_key_use_case.jwt")
@pytest.mark.asyncio
async def test_validate_jwt_success(mock_jwt, mock_settings):
    mock_settings.JWT_CLIENT_SECRET = "secret"
    mock_jwt.decode.return_value = {"sub": "sub_value"}
    result = await use_case._validate_jwt("valid_payload")
    mock_jwt.decode.assert_called_once_with("valid_payload", "secret", algorithms=["HS256"])
    assert result == "sub_value"


@patch("src.authorization.validate_api_key_use_case.settings")
@patch("src.authorization.validate_api_key_use_case.jwt")
@pytest.mark.asyncio
async def test_validate_jwt_failure(mock_jwt, mock_settings):
    mock_settings.JWT_CLIENT_SECRET = "secret"
    mock_jwt.decode.side_effect = Exception("Error")
    with pytest.raises(error_responses.AuthorizationMissingAPIError):
        await use_case._validate_jwt("invalid_payload")
