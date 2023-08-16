from typing import List, Optional

from opencopilot import settings
import tqdm
import weaviate
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TextSplitter
from langchain.vectorstores import Weaviate
from opencopilot.logger import api_logger
from opencopilot.src.repository.documents import document_loader, document_scraper
from opencopilot.src.utils import get_embedding_model_use_case
from opencopilot.src.utils.get_embedding_model_use_case import CachedOpenAIEmbeddings

logger = api_logger.get()


class DocumentStore:
    document_embed_model = "text-embedding-ada-002"
    document_chunk_size = 2000
    ingest_batch_size = 100

    weaviate_index_name = "LangChain"  # TODO: Weaviate specific?

    def __init__(self):
        self.weaviate_client = self._get_weaviate_client()
        self.vector_store = self._get_vector_store()

    def _get_weaviate_client(self):
        return weaviate.Client(
            url=settings.WEAVIATE_URL,
            timeout_config=(10, settings.WEAVIATE_READ_TIMEOUT)
        )

    def _get_vector_store(self):
        documents = self.load_documents()
        metadatas = [d.metadata for d in documents]
        attributes = list(metadatas[0].keys()) if metadatas else None
        return Weaviate(
            self.weaviate_client,
            index_name=self.weaviate_index_name,
            text_key="text",
            embedding=self.get_embeddings_model(),
            attributes=attributes,
            by_text=False
        )

    def scrape_documents(self):
        document_scraper.execute()

    def load_documents(
            self,
            data_dir=None,
            is_loading_deprecated=False
    ) -> List[Document]:
        if not data_dir:
            data_dir = settings.DATA_DIR
        return document_loader.execute(data_dir, is_loading_deprecated, self.get_text_splitter())

    # TODO: Return Base Embeddings Model?
    def get_embeddings_model(self) -> CachedOpenAIEmbeddings:
        return get_embedding_model_use_case.execute(use_local_cache=True)

    def get_text_splitter(self) -> TextSplitter:
        return CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.document_chunk_size,
            model_name=self.document_embed_model,
            separator=" ",
            disallowed_special=(),
        )

    def ingest_data(self):
        batch_size = self.ingest_batch_size
        documents = self.load_documents()
        print(f"Got {len(documents)} documents, embedding with batch size: {batch_size}")
        embeddings = self.get_embeddings_model()
        self.weaviate_client.schema.delete_all()

        for i in tqdm.tqdm(range(0, int(len(documents) / batch_size) + 1), desc="Embedding.."):
            batch = documents[i * batch_size: (i + 1) * batch_size]
            self.vector_store.add_documents(batch)

        embeddings.save_local_cache()

    def find(self, query: str, **kwargs) -> List[Document]:
        k = kwargs.get("k") or settings.MAX_CONTEXT_DOCUMENTS_COUNT
        documents = self.vector_store.similarity_search(
            query,
            k=k
        )
        return documents[:k]


DOCUMENT_STORE = Optional[DocumentStore]


def init_document_store():
    global DOCUMENT_STORE
    DOCUMENT_STORE = DocumentStore()


def get_document_store() -> DocumentStore:
    return DOCUMENT_STORE
