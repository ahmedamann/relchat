from llama_cpp import Llama
import os

MODEL_PATH = "./models/llama-2-7b.Q4_K_M.gguf"

llm = Llama(model_path=MODEL_PATH, n_ctx=512)

def generate_response(prompt: str):
    """Generate response from Llama model."""
    response = llm(prompt, max_tokens=200, stop=["User:", "Assistant:"])
    return response["choices"][0]["text"].strip()