from unittest.mock import MagicMock

from src.domain.chat import get_token_count_use_case as use_case


def test_basic():
    llm = MagicMock()
    llm.get_num_tokens.return_value = 334
    result = use_case.execute("some text", llm)
    assert result == 334


def test_cache():
    llm = MagicMock()
    llm.get_num_tokens.return_value = 112
    result = use_case.execute("some text", llm, is_use_cache=True)
    assert result == 112
    result = use_case.execute("some text", llm, is_use_cache=True)
    assert result == 112
    assert llm.get_num_tokens.call_count == 1
    assert len(use_case.cache) == 1
