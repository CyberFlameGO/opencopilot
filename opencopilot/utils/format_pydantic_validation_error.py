from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from dataclasses import dataclass


@dataclass
class PydanticErrorResponseModel:
    code: str
    message: Union[str, Dict]


def _value_error_number_not_le_ge(
        error: Dict) -> Optional[PydanticErrorResponseModel]:
    loc = _get_loc(error)
    if not loc:
        return
    message: str = error.get("msg")
    message = message.replace("ensure this value is", "must be")
    return PydanticErrorResponseModel(
        code="value_error", message=f"{loc} {message}.")


def _value_error_const(error: Dict) -> Optional[PydanticErrorResponseModel]:
    # Same as _type_error_enum but for POST requests
    loc = _get_loc(error)
    if not loc:
        return
    given_value = error.get("ctx", {}).get("given")
    allowed_values = error.get("ctx", {}).get("permitted")
    allowed_values = [allowed_value.value for allowed_value in allowed_values]
    return PydanticErrorResponseModel(
        code="invalid_enumeration",
        message=f"{loc} value {given_value} is not a valid enumeration "
                f"member. Allowed values: {allowed_values}.")


def _value_error_missing(error: Dict) -> Optional[PydanticErrorResponseModel]:
    loc = _get_loc(error)
    if not loc:
        return
    return PydanticErrorResponseModel(
        code="parameter_missing",
        message=f"Missing required parameter: {loc}.")


def _type_error_enum(error: Dict) -> Optional[PydanticErrorResponseModel]:
    # Same as _value_error_const but for Query params
    loc = _get_loc(error)
    if not loc:
        return
    message: str = error.get("msg")
    allowed_values = error.get("ctx", {}).get("enum_values")
    allowed_values = [allowed_value.value for allowed_value in allowed_values]
    message = message.replace("value", loc)
    message = message[: message.find(";")]
    return PydanticErrorResponseModel(
        code="invalid_enumeration",
        message=f"{message}. Allowed values: {allowed_values}.")


def _type_error_generic(error: Dict) -> Optional[PydanticErrorResponseModel]:
    loc = _get_loc(error)
    if not loc:
        return
    message: str = error.get("msg")
    message = message.replace("value", loc)
    return PydanticErrorResponseModel(
        code="invalid_type",
        message=f"{message}.")


def _type_error_str(error: Dict) -> Optional[PydanticErrorResponseModel]:
    loc = _get_loc(error)
    if not loc:
        return
    message: str = error.get("msg")
    return PydanticErrorResponseModel(
        code="invalid_type",
        message=f"{message} for {loc}.")


def _get_loc(error) -> Optional[str]:
    # Returns invalid parameter name
    for loc in reversed(error.get("loc")):
        if isinstance(loc, str):
            return loc


expected_errors = {
    "value_error.number.not_le": _value_error_number_not_le_ge,
    "value_error.number.not_ge": _value_error_number_not_le_ge,
    "value_error.const": _value_error_const,
    "value_error.missing": _value_error_missing,
    "type_error.enum": _type_error_enum,
    "type_error.integer": _type_error_generic,
    "type_error.float": _type_error_generic,
    "type_error.list": _type_error_generic,
    "type_error.bool": _type_error_generic,
    "type_error.str": _type_error_str
}


def execute(error: List[Dict]) -> Optional[PydanticErrorResponseModel]:
    error = error[0]
    try:
        code = error.get("type", "")
        if code in expected_errors:
            if response := expected_errors.get(code)(error):
                return response
    except:
        pass
    try:
        code = error.get("type", "unprocessable_entity").lower().replace(
            ".", "_")
        return PydanticErrorResponseModel(
            code=code,
            message=error
        )
    except:
        pass
    return
