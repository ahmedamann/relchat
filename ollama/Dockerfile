# Use Ollama official base image
FROM ollama/ollama

# Expose Ollama's default API port
EXPOSE 11434

# Run a shell command that starts Ollama and pulls the model
ENTRYPOINT ["/bin/sh", "-c", "ollama serve & sleep 5 && ollama pull llama3.2 && wait"]
