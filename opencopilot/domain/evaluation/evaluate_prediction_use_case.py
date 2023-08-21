from typing import List
from typing import Sequence

from langchain.callbacks.manager import Callbacks
from langchain.chat_models import ChatOpenAI
from langchain.evaluation import QAEvalChain

from opencopilot.domain.evaluation.entities import EvaluationOutput
from opencopilot.domain.evaluation.entities import EvaluationInput
from opencopilot.eval import endtoend


async def execute(domain_input: EvaluationInput) -> EvaluationOutput:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")

    eval_chain = AsyncQAEvalChain.from_llm(llm=llm, prompt=endtoend.PROMPT)
    eval_example = {"query": domain_input.query, "answer": domain_input.answer}
    eval_prediction = {"result": domain_input.expected_answer}

    graded_output = (await eval_chain.aevaluate([eval_example], [eval_prediction]))[0]

    return EvaluationOutput(evaluation=graded_output["text"])


class AsyncQAEvalChain(QAEvalChain):
    async def aevaluate(
            self,
            examples: Sequence[dict],
            predictions: Sequence[dict],
            question_key: str = "query",
            answer_key: str = "answer",
            prediction_key: str = "result",
            *,
            callbacks: Callbacks = None,
    ) -> List[dict]:
        """Evaluate question answering examples and predictions."""
        inputs = [
            {
                "query": example[question_key],
                "answer": example[answer_key],
                "result": predictions[i][prediction_key],
            }
            for i, example in enumerate(examples)
        ]

        return await self.aapply(inputs, callbacks=callbacks)
