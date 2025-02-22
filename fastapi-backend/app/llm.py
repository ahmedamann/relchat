from langchain_ollama import OllamaLLM

# Load Llama 3.2 with Ollama
llm = OllamaLLM(model="llama3.2", temperature=0)