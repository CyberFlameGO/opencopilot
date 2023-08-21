from typing import List

import requests
from bs4 import BeautifulSoup

from langchain.schema import Document

from opencopilot.utils.loaders import url_loader_use_case


def execute(blog_urls: List[str]) -> List[Document]:
    documents: List[Document] = []
    for blog_url in blog_urls:
        urls = _get_urls(blog_url)
        documents.extend(url_loader_use_case.execute(urls))
    return documents


def _get_urls(blog_url: str) -> List[str]:
    session = requests.Session()
    html_doc = session.get(blog_url, timeout=10)
    html_doc.encoding = html_doc.apparent_encoding
    soup = BeautifulSoup(html_doc.text, "html.parser")
    links = soup.find_all("a")

    urls: List[str] = []
    for link in links:
        # Check if url points to blog and primitive date check
        if "/blog/" in link.attrs.get("href") and ("2022" in link.text or "2023" in link.text):
            urls.append(_get_formatted_url(link.attrs.get("href")))
    return urls


def _get_formatted_url(path: str) -> str:
    if path.startswith("https://"):
        return path
    return "https://readyplayerdev.me" + path
