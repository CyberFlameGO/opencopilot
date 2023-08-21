from typing import List, Optional

import tqdm
import weaviate
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TextSplitter
from langchain.vectorstores import Weaviate

from opencopilot import settings
from opencopilot.logger import api_logger
from opencopilot.utils import get_embedding_model_use_case
from opencopilot.utils.get_embedding_model_use_case import CachedOpenAIEmbeddings

logger = api_logger.get()


class DocumentStore:
    document_embed_model = "text-embedding-ada-002"
    document_chunk_size = 2000

    def get_embeddings_model(self) -> CachedOpenAIEmbeddings:
        return get_embedding_model_use_case.execute(use_local_cache=True)

    def get_text_splitter(self) -> TextSplitter:
        return CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.document_chunk_size,
            model_name=self.document_embed_model,
            separator=" ",
            disallowed_special=(),
        )

    def ingest_data(self, documents: List[Document]):
        pass

    def find(self, query: str, **kwargs) -> List[Document]:
        return []


class WeaviateDocumentStore(DocumentStore):
    ingest_batch_size = 100

    weaviate_index_name = "LangChain"  # TODO: Weaviate specific?

    def __init__(self):
        self.documents = []
        self.embeddings = self.get_embeddings_model()
        self.weaviate_client = self._get_weaviate_client()
        self.vector_store = self._get_vector_store()

    def _get_weaviate_client(self):
        return weaviate.Client(
            url=settings.get().WEAVIATE_URL,
            timeout_config=(10, settings.get().WEAVIATE_READ_TIMEOUT)
        )

    def _get_vector_store(self):
        metadatas = [d.metadata for d in self.documents]
        attributes = list(metadatas[0].keys()) if metadatas else None
        return Weaviate(
            self.weaviate_client,
            index_name=self.weaviate_index_name,
            text_key="text",
            embedding=self.embeddings,
            attributes=attributes,
            by_text=False
        )

    def ingest_data(self, documents: List[Document]):
        self.documents = documents
        batch_size = self.ingest_batch_size
        print(f"Got {len(documents)} documents, embedding with batch size: {batch_size}")
        self.weaviate_client.schema.delete_all()

        for i in tqdm.tqdm(range(0, int(len(documents) / batch_size) + 1), desc="Embedding.."):
            batch = documents[i * batch_size: (i + 1) * batch_size]
            self.vector_store.add_documents(batch)

        self.embeddings.save_local_cache()
        self.vector_store = self._get_vector_store()

    def find(self, query: str, **kwargs) -> List[Document]:
        k = kwargs.get("k") or settings.get().MAX_CONTEXT_DOCUMENTS_COUNT
        documents = self.vector_store.similarity_search(
            query,
            k=k
        )
        return documents[:k]


class EmptyDocumentStore(DocumentStore):
    pass


DOCUMENT_STORE = Optional[DocumentStore]


def init_document_store(document_store: DocumentStore):
    global DOCUMENT_STORE
    DOCUMENT_STORE = document_store


def get_document_store() -> DocumentStore:
    return DOCUMENT_STORE
