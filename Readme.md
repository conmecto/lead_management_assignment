# Udaan Server

## Overview

This project is a FastAPI-based server for managing leads and their contacts. This includes creating leads/contacts with call planning, checking leads with required calls for today, managing interactions with leads(contacts) including order details, lead ordering patterns and leads stats with good/bad performing leads

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/conmecto/lead_management_assignment.git
    cd udaan/server
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**

    Create a `.env` file in the root directory and add the following environment variables:

    ```env
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=username
    DB_PASSWORD=password
    DB_NAME=name
    SERVER_HOST=0.0.0.0
    SERVER_PORT=8000
    AUTH_SECRET_KEY=your_secret_key
    AUTH_ALGORITHM=HS256
    ```

### Running the Server

To start the server, run the following command:

```sh
# uvicorn main:app --reload
python3 main.py 


### Running unti test

```sh
pytest tests.{file_name} 