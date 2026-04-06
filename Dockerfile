FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install the exact libraries we used
RUN pip install --no-cache-dir openenv-core pydantic openai fastapi uvicorn

# Copy all your project files into the container
COPY . /app

# Hugging Face Spaces require apps to run on port 7860
EXPOSE 7860

# Boot up the OpenEnv server 
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
