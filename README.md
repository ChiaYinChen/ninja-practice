# Django Ninja Practice

A simple project to explore Django Ninja.

## Development

### Setup

1. Use Poetry to install the required dependencies defined in `pyproject.toml`.
2. Copy `.env.example` to `src/.env` and update the environment variables as needed.

### Run

Start the server:

```
$ cd src && uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --reload
```

Once running, you can access the interactive API documentation at [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs).
