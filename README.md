# Vector Embeddings + LangChain Test

## Introduction

A question and answer system that uses vector embeddings to find the most similar question to the user's input.
The system is built using the [LangChain](https://python.langchain.com/docs/integrations/toolkits/python) library.

The embeddings are stored in an AstraDB Vector database.

## Setup

1. Create an account in OpenAPI and get the API key.
2. Create a vector database in Datastax and get the connection details
3. Download the database's Secure Connect Bundle and place it in the root of the project.
4. Setup the environment variables in `main.py`
5. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the program:

    ```bash
    python main.py
    ```

## Usage

```txt
Loading data from huggingface

Generating embeddings and storing in AstraDB

Inserted 50 headlines.

Enter your question (or type 'quit' to exit): What is an amoeba?

QUESTION: "What is an amoeba?"

ANSWER: "An amoeba is a single-celled organism."

DOCUMENTS BY RELEVANCE
 0.9274 "Biologists Torture Amoeba For Information On Where Life Came ..."
 0.9274 "Biologists Torture Amoeba For Information On Where Life Came ..."
 0.9274 "Biologists Torture Amoeba For Information On Where Life Came ..."
 0.9274 "Biologists Torture Amoeba For Information On Where Life Came ..."

What's your next question (or type 'quit' to exit): quit

Process finished with exit code 0
```
