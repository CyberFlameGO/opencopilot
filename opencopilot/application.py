from typing import Callable

from langchain.schema import Document


# from .app import app


class OpenCopilot:

    def __init__(
            self,
            copilot_name: str = "default",
            api_base_url: str = "http://127.0.0.1/",
            api_port: int = 3000,
            llm_model_name: str = "gpt-4",
            llm_embeddings_name: str = "gpt-4-0613",
            weaviate_url: str = "http://localhost:8080/",
            max_document_size_mb: int = 50,
            helicone_api_key: str = ""
    ):
        self.copilot_name = copilot_name
        self.api_port = api_port
        self.data_loaders = []
        self.documents = []

    def __call__(self, *args, **kwargs):
        print("__call__, data_loaders:", self.data_loaders)
        for data_loader in self.data_loaders:
            self.documents.extend(data_loader())

        print("All Docs:", self.documents)

        # uvicorn.run(app, port=self.api_port)

    def data_loader(
            self,
            function: Callable[[], Document]
    ):
        self.data_loaders.append(function)

    def add_local_files_dir(self, files_dir: str) -> None:
        pass
