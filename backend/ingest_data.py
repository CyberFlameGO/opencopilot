from src.repository.documents import document_store


def main():
    document_store.init_document_store()
    repository = document_store.get_document_store()
    repository.scrape_documents()
    repository.ingest_data()


if __name__ == '__main__':
    main()
