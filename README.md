# Mempool API
This repository builds a [FastAPI](https://fastapi.tiangolo.com/) based API used as a gateway to Bitcoin network metrics and other data as needed for the mempool dashboard and other applications. 

## Setting Up
Clone the Repository:
```bash
git clone https://github.com/lone-starr/mempool_api.git
```
```bash
cd mempool_api
```

## Create a fresh Python virtual environment
```bash
python3 -m venv ./venv
```

## Select Python interpretor (Visual Studio Code)
Open VS Code from the mempool_api directory:
```bash
code .
```
In VS Code press < Ctrl >< Shift >< p >, type Python and choose 'Python: Select Interpretor', choose the newly created venv for mempool_dashboard


## Install Dependencies
Open a new Terminal in VS Code and use the following command to install the required dependencies. Your Python venv should be indicated in your terminal shell.
```bash
pip install -r requirements.txt
```

## Environment Variables
Create a .env file with the necessary credentials and API keys for your MongoDB instance. You can create a free cluster to host your collection at https://cloud.mongodb.com/ or create a MongoDB instance on Railway.

## Run locally
Run service locally:
```bash
uvicorn main:app
```
