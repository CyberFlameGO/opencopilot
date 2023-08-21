import json
import os
from typing import Callable
from typing import List

from opencopilot import settings
from langchain.schema import Document
from opencopilot.utils.loaders import fullstack_deeplearning_loader_use_case, \
    openai_docs_loader_use_case, url_loader_use_case, openai_api_docs_loader_use_case, \
    prompting_guide_docs_loader_use_case, html_loader_use_case, blog_loader_use_case, \
    anthropic_docs_loader_use_case, gitbook_loader_use_case

LOADERS_MAP = {
    "gitbook": gitbook_loader_use_case.execute,
    "url": url_loader_use_case.execute,
    "blog": blog_loader_use_case.execute,
    "html": html_loader_use_case.execute,
    "openai_docs": openai_docs_loader_use_case.execute,
    "openai_api_docs": openai_api_docs_loader_use_case.execute,
    "anthropic_docs": anthropic_docs_loader_use_case.execute,
    "prompting_guide_docs": prompting_guide_docs_loader_use_case.execute,
    "fullstack_deeplearning": fullstack_deeplearning_loader_use_case.execute,
}


def execute():
    if settings.get().copilot_config and settings.get().copilot_config.data.loaders:
        for data_group in settings.get().copilot_config.data.loaders:
            if loader := LOADERS_MAP.get(data_group):
                configuration = settings.get().copilot_config.data.loaders[data_group]
                _scrape(
                    os.path.join(
                        settings.get().DATA_DIR,
                        configuration["output"],
                    ),
                    loader,
                    configuration["sources"],
                    configuration.get("base_url"),
                )


def _scrape(
        file_dump_path: str,
        loader_function: Callable[[List[str]], List[Document]],
        urls: List[str],
        base_url: str = None,
) -> None:
    if not os.path.exists(file_dump_path):
        scraped_documents = loader_function(urls)
        if base_url:
            for doc in scraped_documents:
                doc.metadata["source"] = base_url + os.path.basename(doc.metadata['source'])

        json_docs = [d.json() for d in scraped_documents]
        formatted_docs = [json.loads(d) for d in json_docs]

        os.makedirs(settings.get().DATA_DIR, exist_ok=True)
        with open(file_dump_path, "w") as f:
            f.write(json.dumps(formatted_docs, indent=4))
