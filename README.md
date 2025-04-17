# Flask Application

A simple Flask application with health check and greeting endpoints.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file:
```bash
cp .env.example .env
```

4. Update the .env file with your environment variables.

## Running the Application

1. Development mode:
```bash
python src/app.py
```

2. Production mode:
```bash
gunicorn src.app:app
```

## Running Tests

```bash
pytest
```

## API Endpoints

- `GET /`: Returns a greeting message
- `GET /health`: Health check endpoint 