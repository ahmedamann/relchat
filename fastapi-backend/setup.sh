#!/bin/bash

MODEL_DIR="/tmp/model_cache"
mkdir -p $MODEL_DIR

# Check if model exists before pulling
if [ ! -f "$MODEL_DIR/mistral" ]; then
    echo "Model not found, pulling..."
    OLLAMA_MODELS=$MODEL_DIR ollama pull mistral
else
    echo "Model found, skipping download."
fi

# Start Ollama only if it's not already running
if pgrep -x "ollama" > /dev/null
then
    echo "Ollama is already running."
else
    echo "Starting Ollama..."
    OLLAMA_MODELS=$MODEL_DIR ollama serve &
    sleep 5
fi