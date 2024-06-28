FROM python:3.11.9-slim-bullseye

RUN pip install poetry

WORKDIR /app

COPY ["pyproject.toml", "poetry.lock", "./"]

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY ["main.py", "turtles.py", "./"]

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]