# LLM Communication Framework

This repository provides a private framework for setting up and testing local LLM communication. Using Docker, this framework allows you to deploy a FastAPI server and an Ollama LLM service, with a demonstration script (`demo.py`) to interact with the API. The default LLM is `llama3`, but you can change the configuration to use OpenAI's API if desired.

---

## Prerequisites

1. **Docker and Docker Compose**: Ensure that Docker is installed on your system.
2. **Python** (for running `demo.py`): Ensure Python 3.9+ is installed.

---

## Setup and Usage

### Step 1: Clone the Repository or download the files

```bash
git clone https://github.com/itskaj/LLM-comm.git
cd llm-communication-framework
```

### Step 2: Pull Docker Images and Start Containers
1. Log in to Docker Hub (if images are private):

    ```bash
    docker login
    ```
2. Start the Docker containers:

    ```bash
    compose up -d
    ```

    This will pull and start two containers:

    llm-api-fastapi - runs the FastAPI server on port 8000
    llm-api-ollama - runs the Ollama LLM server on port 11434

3. Pull the LLM model (if not pre-loaded):

    Enter the ollama container:
    ```bash
    docker-compose exec ollama bash
    ```
    Pull the llama3 model:
    ```bash
    ollama pull llama3:latest
    ```
    Exit the container:
    ```bash
    exit
    ```
### Step 3: Run demo.py to Test the API

1. Install Python dependencies (if not installed):
```bash
pip install -r requirements.txt
```

2. Run the demo script:
```bash
python demo.py
```
By default, demo.py is set to use ollama with the llama3 model.
To switch to OpenAI, edit demo.py and change the LLM provider and credentials:
```python
"provider": "openai",
"credentials": {
    "api_key": os.environ.get("OPENAI_API_KEY"),
    "model": "gpt-4o-mini"
}
```
Make sure to set the OpenAI API key:
```bash
export OPENAI_API_KEY="your_openai_api_key"
```

## Interacting with the API in demo.py

Once the demo starts, you’ll see prompts and available commands:

    /history: View the chat history.
    /raw: Retrieve raw JSON responses.
    /quit: Exit the demo.

## Stopping the Containers

When done, stop the containers with:
```bash
docker-compose down
```

## Troubleshooting

    Connection Errors: Ensure that Docker containers are running and accessible on localhost:8000 for FastAPI and localhost:11434 for Ollama.
    Model Not Found: Ensure the llama3 model is pulled within the ollama container.





