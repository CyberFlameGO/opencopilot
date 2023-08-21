from opencopilot.authorization import create_access_token
from opencopilot.service.authorization.entities import TokenRequest, TokenResponse


def execute(request: TokenRequest) -> TokenResponse:
    token = create_access_token.execute(
        request.client_id,
        request.client_secret,
        request.user_id
    )
    return TokenResponse(
        response="OK",
        token=token
    )
