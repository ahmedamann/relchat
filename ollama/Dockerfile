FROM ollama/ollama

EXPOSE 11434

ENTRYPOINT ["/bin/sh", "-c", "ollama serve & sleep 5 && ollama pull llama3.2 && wait"]
