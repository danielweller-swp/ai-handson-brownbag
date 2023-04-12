# Demo App Backend

## Initial Setup

Prepare python env:
```sh
conda create --name ai-handson-brownbag-backend
conda activate ai-handson-brownbag-backend
pip install -r requirements.txt
```

## API credentials setup

This application uses OpenAI's GPT from an Azure Cloud deployment,
and OpenAI DALL-E 2 and Embeddings from OpenAI's API.
You'll need to configure the credentials for both.

To do so, create a `.env` file based on `.env.sample`.
## Running

```sh
uvicorn main:app --reload
```
