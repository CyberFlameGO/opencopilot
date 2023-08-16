from unittest.mock import MagicMock
from uuid import UUID

import pytest

import opencopilot.src.domain.chat.validate_urls_use_case as use_case

TEST_UUID = UUID("e69053ac-4ffa-4aeb-8db1-dea5bc7d2b02")


@pytest.fixture(autouse=True)
def run_around_tests():
    use_case.requests = MagicMock()
    use_case.logger = MagicMock()
    yield


def test_no_urls():
    use_case.execute("random text without urls", TEST_UUID)
    use_case.requests.get.assert_not_called()


def test_one_url():
    url = "https://url.url"
    use_case.execute(f"random text {url} with 1 url", TEST_UUID)
    use_case.requests.get.assert_called_with(url)


def test_multiple_urls():
    url1 = "https://url.com"
    url2 = "https://url2.custom/epic-custom/path"
    use_case.execute(f"random text {url1}😀 with multiple urls `{url2}`", TEST_UUID)
    assert use_case.requests.get.call_args_list[0][0][0] == url1
    assert use_case.requests.get.call_args_list[1][0][0] == url2
