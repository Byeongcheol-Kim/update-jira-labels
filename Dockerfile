FROM python:3.10.11-slim AS python
ENV PYTHONUNBUFFERED=true
ADD . /app
WORKDIR /app

FROM python as poetry
ENV POETRY_VERSION=1.4.1
RUN pip install "poetry==$POETRY_VERSION"
COPY . ./
RUN poetry config virtualenvs.create true && poetry config virtualenvs.in-project true && poetry install --no-interaction --no-ansi --no-root

FROM python as runtime
COPY --from=poetry /app /app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "/app/main.py"]