from langchain_ollama import OllamaLLM

# Load Llama 2 with Ollama
llm = OllamaLLM(model="llama3.2", temperature=0)

def generate_response(prompt: str):
    return llm.invoke(prompt)