import json
import os

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from webapp.repository.db_setup import get_schema_descriptions

def query_index(query):
    """Query the in-memory vector index."""
    if table_schema_vector_store is None:
        raise ValueError("Index has not been initialized. Please refresh the index first.")

    # Perform similarity search to find relevant documents
    results_table = table_schema_vector_store.similarity_search(query, k=10)
    results_query = query_vector_store.similarity_search(query, k=10)
    table_schema_results = [
        {
            "table_name": result.metadata['table_name'],
            "table_columns": result.metadata['columns'],
            "content": result.page_content
        }
        for result in results_table
    ]

    related_query_results = [
        {
            "query": result.metadata['query'],
            "content": result.page_content,
            "reasoning": result.metadata['reasoning']
        }
        for result in results_query
    ]

    return {"table_schemas": table_schema_results, "example_related_query": related_query_results}



def load_user_requests(filename="query_index.json"):
    with open("/Users/priyansh/Documents/work/git-work-agency/webapp/resource/query_index.json", "r") as file:
        return json.load(file)


def  refresh_vector_index():
    """Refresh the in-memory vector index with the latest schema descriptions."""
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.environ["OPENAI_API_KEY"])
    global table_schema_vector_store
    global query_vector_store
    schemas = get_schema_descriptions()
    user_query= load_user_requests()




    # Convert schema descriptions into LangChain Document objects
    documents_table = [
        Document(page_content=schema['table_description'], metadata={'table_name': schema['table_name'],'columns': schema['columns']})
        for schema in schemas
    ]

    documents_query = [
        Document(page_content=record['request'], metadata={'query': record['query'],'reasoning': record['reasoning']})
        for record in user_query
    ]

    # Create a new FAISS vector store with the embeddings and documents
    table_schema_vector_store = FAISS.from_documents(documents_table, embedding_model)
    query_vector_store = FAISS.from_documents(documents_query, embedding_model)

