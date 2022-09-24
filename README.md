# ASTARIX

Web API built for help post guides and tutorials about games

## Requirements

- [Python-3.+](https://python.org)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Setup

1. Clone the repository

```bash
git clone
```

2. Create a virtual environment

```bash
python3 -m venv venv
```

3. Activate the virtual environment

```bash
source venv/bin/activate
```

4. Install the dependencies

```bash
pip install -r requirements.txt
```

## Running

```bash
python manage.py runserver
```

```bash
python manage.py createsuperuser # Create a superuser
python manage.py makemigrations # Create migrations
python manage.py migrate # Apply migrations
```

# Contributing
