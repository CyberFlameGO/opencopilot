import os
from typing import Callable
from typing import Optional

import uvicorn
from langchain.schema import Document

from . import ingest_data
from . import settings


class OpenCopilot:

    def __init__(
            self,
            openai_api_key: Optional[str] = None,
            copilot_name: str = "default",
            api_base_url: str = "http://127.0.0.1/",
            api_port: int = 3000,
            llm_model_name: str = "gpt-4",
            llm_embeddings_name: str = "gpt-4-0613",
            weaviate_url: str = "http://localhost:8080/",
            max_document_size_mb: int = 50,
            helicone_api_key: str = ""
    ):
        if not openai_api_key:
            openai_api_key = os.getenv("OPENAI_API_KEY")
        assert openai_api_key, "OPENAI_API_KEY must be passed to OpenCopilot or be set in the environment."
        settings.set_openai_api_key(openai_api_key)

        settings.init_copilot(copilot_name)
        settings.WEAVIATE_URL = weaviate_url
        self.api_port = api_port
        self.data_loaders = []
        self.documents = []

    def __call__(self, *args, **kwargs):
        print("__call__, data_loaders:", self.data_loaders)
        for data_loader in self.data_loaders:
            self.documents.extend(data_loader())

        print("All Docs:", self.documents)

        from .app import app
        uvicorn.run(app, port=self.api_port)

    @staticmethod
    def add_prompt(prompt_file: str) -> None:
        settings.init_prompt_file_location(prompt_file)

    @staticmethod
    def add_data_dir(data_dir: str) -> None:
        settings.init_data_dir(data_dir)

    @staticmethod
    def ingest_data() -> None:
        print("Ingesting data")
        ingest_data.execute()

    def data_loader(
            self,
            function: Callable[[], Document]
    ):
        self.data_loaders.append(function)

    def add_local_files_dir(self, files_dir: str) -> None:
        pass
