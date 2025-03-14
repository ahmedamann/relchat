from langchain_ollama import OllamaLLM

llm = OllamaLLM(base_url="http://127.0.0.1:11434", model="mistral", temperature=0)
