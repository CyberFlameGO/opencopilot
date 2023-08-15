from typing import List
from typing import Dict
from typing import Union
import os

from bs4 import BeautifulSoup
from langchain.document_loaders import BSHTMLLoader
from langchain.schema import Document


def execute(paths: List[str]) -> List[Document]:
    documents: List[Document] = []
    for path in paths:
        if os.path.isdir(path):
            scraped_documents= _scrape_folder(path)
        else:
            scraped_documents = _scrape_html(path)
        documents.extend(scraped_documents)
    return documents


def _scrape_folder(folder: str) -> List[Document]:
    documents = []
    files = []
    for dir_path, dir_names, file_names in os.walk(folder):
        for file_name in file_names:
            if os.path.splitext(file_name)[1] in [".html", ".htm"]:
                files.append(os.path.join(dir_path, file_name))
    for file in files:
        documents.extend(_scrape_html(file))
    return documents


def _scrape_html(filename) -> List[Document]:
    try:
        loader = CustomHtmlLoader(filename)
        return loader.load()
    except:
        return []


class CustomHtmlLoader(BSHTMLLoader):

    def load(self) -> List[Document]:
        with open(self.file_path, "r", encoding=self.open_encoding) as f:
            soup = BeautifulSoup(f, **self.bs_kwargs)

        section = soup.find(class_="section")
        navigation = soup.find_all(class_="nextprev")
        breadcrumbs = soup.find_all(class_="breadcrumbs")
        for breadcrumb in breadcrumbs:
            breadcrumb.extract()
        for child in navigation:
            child.extract()
        text = section.get_text(self.get_text_separator)

        if soup.title:
            title = str(soup.title.string)
        else:
            title = ""

        metadata: Dict[str, Union[str, None]] = {
            "source": self.file_path,
            "title": title,
        }
        return [Document(page_content=text, metadata=metadata)]
