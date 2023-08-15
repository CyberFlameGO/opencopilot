from src.domain.evaluation import evaluate_prediction_use_case
from src.service.debug.entities import EvaluationInput
from src.service.debug.entities import EvaluationResponse


async def execute(request: EvaluationInput) -> EvaluationResponse:
    result = await evaluate_prediction_use_case.execute(
        EvaluationInput(
            query=request.query,
            answer=request.answer,
            expected_answer=request.expected_answer,
        )
    )
    return EvaluationResponse(
        response="OK",
        evaluation=result.evaluation,
    )
