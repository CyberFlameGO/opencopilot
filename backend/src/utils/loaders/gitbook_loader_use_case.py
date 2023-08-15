from typing import Any
from typing import List
from typing import Optional

import os
from urllib import parse
from bs4 import BeautifulSoup
from langchain.document_loaders import GitbookLoader
from langchain.schema import Document


def execute(urls: List[str]) -> List[Document]:
    documents = []
    for url in urls:
        loader = CustomGitbookLoader(url, load_all_paths=True)
        documents.extend(loader.load())
    return documents


class CustomGitbookLoader(GitbookLoader):

    def __init__(
        self,
        web_page: str,
        load_all_paths: bool = False,
        base_url: Optional[str] = None,
        content_selector: str = "main",
    ):
        super().__init__(web_page, load_all_paths, base_url, content_selector)
        self.parsed_url = parse.urlparse(web_page)

    def _get_document(
            self, soup: Any, custom_url: Optional[str] = None
    ) -> Optional[Document]:
        """Fetch content from page and return Document."""
        page_content_raw = soup.find(self.content_selector)
        i = 0
        last_child: Optional[Any] = None
        for child in page_content_raw.children:
            last_child = child
            i = i + 1
        if i > 2:
            print("Unexpected page content")
        else:
            """
            Pages have this format:
            <main>
                <div>title</div>
                <div>
                    <div>content here</div>
                    <div>navigation and other info</div>
                </div>
            </main>
            This removes the navigation part from the html
            """
            if last_child:
                i = 0
                for child in last_child.children:
                    if i == 1:
                        child.decompose()
                    i = i + 1
        if not page_content_raw:
            return None

        # Find all the 'a' tags in the HTML and convert them into Markdown links
        for link in page_content_raw.find_all("a"):
            href = link.get("href")
            if href is not None and link.text is not None:
                if href.startswith("/"):
                    absolute_path = os.path.join(self.parsed_url.netloc, href.lstrip("/"))
                    href = parse.urlunparse((self.parsed_url.scheme, absolute_path, '', '', '', ''))
                link_md = f"[{link.text}]({href})"
                link.replace_with(BeautifulSoup(link_md, "html.parser"))

        content = page_content_raw.get_text(separator="\n").strip()
        title_if_exists = page_content_raw.find("h1")
        title = title_if_exists.text if title_if_exists else ""
        metadata = {"source": custom_url or self.web_path, "title": title}
        return Document(page_content=content, metadata=metadata)
