
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
import os
from azure.search.documents.indexes.models import (
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
)

EMBEDDINGS = AzureOpenAIEmbeddings(azure_deployment="text-embedding-3-small")
INDEX_NAME = "document-index"
VECTOR_STORE = AzureSearch(
    azure_search_endpoint=os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"],
    azure_search_key=os.environ["AZURE_SEARCH_ADMIN_KEY"],
    index_name=INDEX_NAME,
    embedding_function=EMBEDDINGS.embed_query,
    semantic_configurations=[
        SemanticConfiguration(
            name="simple-config",
            prioritized_fields=SemanticPrioritizedFields(
                content_fields=[SemanticField(field_name="content")]
            )
        )
    ], 
    semantic_configuration_name="simple-config" 
)
