FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
ENV POETRY_VERSION=1.1.13

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock app/
COPY pyproject.toml app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root


# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/cmd/main.py"]