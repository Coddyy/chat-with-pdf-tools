from typing import List

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
from models import Models

def add_posts(title: str = '', userId: int = 0) -> str:
    """ Create/Add posts with title and userId

    Args:
        title (str): Previous addresses as a list of strings.
        userId (int): the user ID.
    """
    
    ## API Call
    import requests
    import json

    url = "https://dummyjson.com/posts/add"
    payload = json.dumps({
        "title": title,
        "userId": userId
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def add_numbers(a: int, b: int) -> int:
    """ Add two numbers.

    Args:
        a (int): first number.
        b (int): second number.
    """
    return int(a) + int(b)


def substract_numbers(a: int, b: int) -> int:
    """ Substracts two numbers.

    Args:
        a (int): first number.
        b (int): second number.
    """
    return int(a) - int(b)

def general_query(query: str) -> str:
    """This function used to give answer based on vector database.

    Args:
        query (str): question asked by the user.
    """

    # Initialize the models
    models = Models()
    embeddings = models.embeddings_ollama
    llm = models.model_ollama

    # Initialize the vector store
    vector_store = Chroma(
        collection_name="documents",
        embedding_function=embeddings,
        persist_directory="./db/chroma_langchain_db",  # Where to save data locally
    )

    # Define the chat prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant (Co-Pilot). Answer the question based only the data provided."),
            ("human", "Use the user question {input} to answer the question. Use only the {context} to answer the question.")
        ]
    )

    # Define the retrieval chain
    retriever = vector_store.as_retriever(kwargs={"k": 10})
    combine_docs_chain = create_stuff_documents_chain(
        llm, prompt
    )
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    result = retrieval_chain.invoke({"input": query})
    #print("Assistant: ", result["answer"], "\n\n")
    return result["answer"]
