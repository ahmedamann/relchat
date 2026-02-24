from .embeddings import vector_store
from .llm import llm
from langsmith import Client
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from .prompts import main_prompt


client = Client()
rephrase_prompt = client.pull_prompt("langchain-ai/chat-langchain-rephrase")


def get_new_prompt(query, prev_conv):
    prompt_chain = (
    {
        "input": RunnablePassthrough(),
        "chat_history": lambda _: prev_conv
    }
    | rephrase_prompt
    | llm
    )

    prompt = prompt_chain.invoke(query)
    cleaned_prompt = prompt
    return cleaned_prompt


def retriever_chain(retriever):
    retriever_chain = (
        {
            "input": RunnablePassthrough(),
            "context": retriever
        }
        | main_prompt
        | llm
    )
    return retriever_chain

def pipeline(user, prev_conv, query):
    retriever = vector_store.as_retriever(search_kwargs={'filter': {'user_id':user}})

    if prev_conv:
        print(prev_conv)
        query = get_new_prompt(query, prev_conv)
        print(f"Query Refined to: {query}")
    else:
        print(f"No Past Convo Query is the same: {query}")
        # Do nothing
    
    return retriever_chain(retriever), query