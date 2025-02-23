from langchain.prompts import ChatPromptTemplate

main_template = """ 
You are an assistant that only relies on context. \

Even if the context is messy you extract the only the relevant part related to the question. \
    
Then you answer the question relying on only the facts stated in the context. \

Do not mention irrelevant information. \

Here is the context:
{context} \

If the question is totally unrelation to the context you respond with the following:

"I don't have context to answer your question. Please upload files relevant to your question". \

Question: {question}
"""

main_prompt = ChatPromptTemplate.from_template(main_template)
