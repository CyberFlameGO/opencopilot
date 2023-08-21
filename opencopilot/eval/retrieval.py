from opencopilot.eval.entities import (
    RetrievalExample,
    RetrievalResult,
    RetrievalSingleEvaluation,
    RetrievalSummaryEvaluation,
    RetrievalDataset,
)
from typing import List


def get_confusion_matrix(
    ground_truth: RetrievalExample, predicted: RetrievalResult
) -> RetrievalSingleEvaluation:
    """Compare a single ground-truth retrieval example with a single predicted result."""
    tp, fp, _, fn = [], [], [], []  # we won't calculate true-negatives

    for predicted_doc in predicted.documents:
        if predicted_doc in ground_truth.documents:
            tp.append(predicted_doc)
        else:
            fp.append(predicted_doc)

    for relevant_doc in ground_truth.documents:
        if relevant_doc not in predicted.documents:
            fn.append(relevant_doc)

    return tp, fp, fn


def get_summary_evaluation(
    single_evaluations: List[RetrievalSingleEvaluation],
) -> RetrievalSummaryEvaluation:
    """Roll up a list of single evaluations into a summary evaluation."""
    precisions = [e.precision for e in single_evaluations]
    recalls = [e.recall for e in single_evaluations]

    return RetrievalSummaryEvaluation(
        single_evaluations=single_evaluations,
        average_precision=sum(precisions) / len(precisions),
        average_recall=sum(recalls) / len(recalls),
    )


def evaluate_retrieval_single(
    ground_truth: RetrievalExample, predicted: RetrievalResult
) -> RetrievalSingleEvaluation:
    tp, fp, fn = get_confusion_matrix(ground_truth, predicted)
    n_tp, n_fp, n_fn = len(tp), len(fp), len(fn)

    if (n_tp + n_fp) == 0:
        print(f"Warning: No results from Weaviate for question: {ground_truth.query}")
        precision = 1.0
    else:
        precision = n_tp / (n_tp + n_fp)

    if (n_tp + n_fn) == 0:
        print(f"Warning: This example has zero expected URLs: {ground_truth.query}")
        recall = 1.0
    else:
        recall = n_tp / (n_tp + n_fn)

    return RetrievalSingleEvaluation(
        example=ground_truth,
        result=predicted,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
        precision=precision,
        recall=recall,
    )


def evaluate_retrieval_dataset(
    dataset: RetrievalDataset, predictions: List[RetrievalResult]
) -> RetrievalSummaryEvaluation:
    assert len(dataset.examples) == len(predictions)

    evals = []
    for i, prediction in enumerate(predictions):
        evals.append(evaluate_retrieval_single(dataset.examples[i], prediction))

    return get_summary_evaluation(evals)
