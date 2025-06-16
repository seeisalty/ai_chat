FROM localai/localai:latest

# Copy your model files into the image
COPY ./models /models

# Expose the API port
EXPOSE 5000

# Start LocalAI, serving models from /models
CMD ["run", "--models-path", "/models", "--address", "0.0.0.0:5000"]