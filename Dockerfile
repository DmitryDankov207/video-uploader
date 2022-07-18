FROM python:3.10-slim-bullseye

# Copy only requirements to cache them in Docker layer.
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Install dependencies.
RUN pip install --upgrade pip
RUN pip install poetry==1.1.13
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy project.
COPY ./src /app
