FROM python:3.12 AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.5.1
ENV APP_DIR=/opt/fantasy_league

RUN mkdir -p ${APP_DIR}/src/

# Install dependencies
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock ${APP_DIR}
COPY pyproject.toml ${APP_DIR}
COPY src/ ${APP_DIR}/src/

# Set work directory
WORKDIR ${APP_DIR}/src

FROM base as dev
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi