async def add_response_headers(response, duration):
    if duration:
        response.headers["Response-Time"] = str(duration)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = \
        "Content-Type,Authorization,Response-Time,source"
    response.headers["Access-Control-Allow-Methods"] = \
        "GET,PUT,POST,DELETE,OPTIONS"
    return response
