from pydantic import BaseModel
from pydantic import Field


class ApiResponse(BaseModel):
    response: str = Field(
        description="Response status, either OK or NOK."
    )

    class Config:
        schema_extra = {
            "example": {
                "response": "OK"
            }
        }
