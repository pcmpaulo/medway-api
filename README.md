### Project Medway

## Description

A Django rest project with base functions to save answers for exams of a student and return a formated resume of his answers.

## Prerequisites

Ensure you have the following dependencies installed:

- Make
- Python
- Pip
- Pyenv
- Docker
- Docker Compose
- Debian based OS

## Tech Stack

**Server:** Python, Django, Django Rest

**Database:** Postgres

**Infrastructure:** Docker

## Run application locally

1. **Create a .env file based on .env.example:**
    ```bash
      cp .env.example .env
    ```
2. **Configure environment:**
    ```bash
       make create-virtualenv # create virtual env

       make activate-virtualenv # Activate virtual env
    ```
3. **Install all dependencies:**
    ```bash
       make install-dependencies
    ```
4. **Start database with docker and run migrations:**
    ```bash
       make start-database # Start docker database
   
       make apply-migrations # Apply all django migrations
    ```
5. **Run api locally:**
    ```bash
       make run-dev
    ```
6. **Create a user/student:**
    ```bash
       python app/manage.py createsuperuser
    ```

## Run application on docker

1. **start docker build:**
    ```bash
      make run-prod
    ```
2. **Access the container bash:**
    ```bash
       make access-docker-bash
    ```
3. **Create a user/student:**
    ```bash
       python manage.py createsuperuser
    ```

# Environment Variables

The ```.env``` file should include:

```bash
    DEBUG=True
    POSTGRES_PORT=5432
    POSTGRES_USER=teste
    POSTGRES_PASSWORD=teste
    POSTGRES_DB=teste
    POSTGRES_HOST=localhost
    DJANGO_SECRET_KEY='secret key'
```

# Running Tests

Run tests with coverage using the cobe below: (need to follow the steps 1 to 4 on ```Run application locally``` first)
```bash
   make test   
```