from starlette.responses import JSONResponse


def to_json_response(result):
    json_response = JSONResponse(result)
    return json_response
