# Contributing

## How to run Dockerfile locally.

```
docker run -dp 5000:5000 -w /app -v "%cd%:/app" flask_smorest_api sh -c flask run --host 0.0.0.0

```