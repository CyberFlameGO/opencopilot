from typing import List

import streamlit as st

from scripts import get_all_feedbacks
from scripts.analyse_feedback import UserFeedbackAnalytics
from scripts.get_all_feedbacks import UserFeedbackResult
from scripts import analyse_feedback


def _print_metrics(feedback: UserFeedbackAnalytics, all_feedbacks: List[UserFeedbackResult]) -> None:
    st.write("# Metrics")
    _print_metric("Correctness", feedback.correctness)
    _print_metric("Helpfulness", feedback.helpfulness)
    _print_metric("Easy to understand", feedback.easy_to_understand)
    st.write(f"### Messages with feedback:", len(all_feedbacks))


def _print_metric(label: str, metric: List[int]) -> None:
    st.write(f"### {label}")
    st.write(f"- len:", len(metric))
    st.write(f"- min:", min(metric))
    st.write(f"- max:", max(metric))
    st.write(f"- avg:", sum(metric) / len(metric))


def _print_all_feedbacks(all_feedbacks: List[UserFeedbackResult]) -> None:
    st.write("\n\n# Detailed feedbacks:")
    st.write("\nTo see the conversations in frontend need to be signed in with nftport email")
    for feedback in all_feedbacks:
        st.write(f"\n### Prompt: {feedback.prompt}")
        st.write(f"\nResponse: {feedback.response}")
        st.write(f"\n- correctness:", feedback.correctness)
        st.write(f"\n- helpfulness:", feedback.helpfulness)
        st.write(f"\n- easy_to_understand:", feedback.easy_to_understand)
        if feedback.free_form_feedback:
            st.write(f"\n- feedback: {feedback.free_form_feedback}")
        url = f"https://rpm.sidekik.ai/chat/{feedback.conversation_id}"
        st.write(f"\n[{url}]({url})")


def main():
    st.title('User feedbacks')
    data_load_state = st.text('Loading data...')
    feedback = analyse_feedback.execute()
    all_feedbacks = get_all_feedbacks.execute()
    data_load_state.text('Loading data...done!')
    _print_metrics(feedback, all_feedbacks)
    _print_all_feedbacks(all_feedbacks)


main()
