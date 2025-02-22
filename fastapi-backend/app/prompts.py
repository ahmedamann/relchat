from langchain.prompts import ChatPromptTemplate

main_template = """ 
You are a helpful assistant \
    
You answer questions only based on the following relevant context \
{context} \

If you don't know the answer you say that. \

Question: {question}
"""

main_prompt = ChatPromptTemplate.from_template(main_template)
