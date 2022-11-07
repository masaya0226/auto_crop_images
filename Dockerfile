FROM python:3.9-slim

RUN apt update -y \
    && apt-get install -y curl zbar-tools libgl1-mesa-dev
RUN apt install -y libopencv-dev

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.1.5 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/src" \
    U2NET_HOME="u2net"

ENV PATH=$POETRY_HOME/bin:$PATH

# poetryインストール
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/$POETRY_VERSION/get-poetry.py | python
WORKDIR $PYSETUP_PATH

RUN mkdir volumes
COPY poetry.lock pyproject.toml ./

RUN poetry install