import os
from langchain_core.documents import Document
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader

from typing import List
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from src.database.vector_store import VECTOR_STORE, INDEX_NAME

def read_doc(file_path:Path)->List[Document]:
    loader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=os.environ["AZURE_DOC_INTEL_ENDPT"],
        api_key=os.environ["AZURE_DOC_INTEL_KEY"],
        file_path=file_path.as_posix(),
        api_model="prebuilt-layout" # This model is essential for table/header detection
    )
    try:
        documents=loader.load()
        return documents
    except Exception as e:
        print(f"❌ Error reading {file_path.name}: {e}")
        return []

def split_doc(content:List[Document],file_name:str)->List[Document]:
    headers_to_split_on = [
        ("#", "Header_1"),
        ("##", "Header_2"),
        ("###", "Header_3"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on, 
        strip_headers=False # Keep headers in text so LLM sees them
    )

    joined_docs = "\n\n".join([doc.page_content for doc in content])
    header_splits = markdown_splitter.split_text(joined_docs)


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " "] # Priority: Para -> Line -> Sentence
    )

    final_chunks = text_splitter.split_documents(header_splits)
    for chunk in final_chunks:
        chunk.metadata={"file_name":file_name} # Add original metadata to each chunk
    return final_chunks

def ingest_docs():
    DATA_DIR = Path("./data")
    SUPPORTED_EXTENSIONS = {
        '.pdf', '.jpeg', '.jpg', '.png', '.bmp', '.tiff', '.heif', 
        '.docx', '.xlsx', '.pptx', '.html'
    }
    all_docs = []
    for file in DATA_DIR.iterdir():
        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            print(f"🚀 Processing: {file.name}...")
            docs = read_doc(file)
            split_chunks = split_doc(docs,file.name)
            all_docs.extend(split_chunks)
            print(f"✅ Completed: {file.name}, Chunks: {len(split_chunks)}")

    try:
        VECTOR_STORE.add_documents(all_docs)
        print(f"🎉 Ingestion complete! Total {len(all_docs)} documents stored in vector store index {INDEX_NAME}")
    except Exception as e:
        print(f"❌ Error during vector store ingestion: {e}")
        