from .embeddings import vector_store
from .llm import llm
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from .prompts import main_prompt


rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

def pipeline(user, prev_conv, query):
    retriever = vector_store.as_retriever(search_kwargs={'k': 3, 'filter': {'user_id':user}})
    prompt_chain = (
        {
            "input": lambda _:query,
            "chat_history": lambda _: prev_conv
        }
        | rephrase_prompt
        | llm
    )

    final_chain = (
        prompt_chain
        | RunnableLambda(
            lambda out: {
                "input": out,
                "chat_history": prev_conv,
                "context": retriever.invoke(out)
            }
        )
        | main_prompt
        | llm
        | StrOutputParser()
    )

    return final_chain