ARG APP_DIR=/app

#########
# Build Image
#########

FROM python:3.10-slim AS build
ARG APP_DIR

RUN apt-get update \
  && apt-get install -y \
       curl \
       build-essential \
       libffi-dev \
  && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.5.0
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH

WORKDIR ${APP_DIR}
COPY pyproject.toml poetry.lock ./

RUN python -m venv --copies ${APP_DIR}/venv
RUN . ${APP_DIR}/venv/bin/activate && poetry install --only main

#########
# Deployment image
#########

FROM python:3.10-slim as run
ARG APP_DIR

COPY --from=build ${APP_DIR}/venv ${APP_DIR}/venv/
ENV PATH ${APP_DIR}/venv/bin:$PATH

WORKDIR ${APP_DIR}
COPY ./ ./

CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
