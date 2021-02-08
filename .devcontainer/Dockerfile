# Mostly inspired from:
# https://github.com/wemake-services/wemake-django-template/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/docker/django/Dockerfile
# https://github.com/python-poetry/poetry/discussions/1879
# https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker

# `python-base` sets up all our shared environment variables
FROM python:3.9.1-slim-buster AS python-base

# python:
# https://docs.python.org/3/using/cmdline.html#environment-variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    # https://pip.pypa.io/en/stable/user_guide/#environment-variables
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    # paths:
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    git




# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl \
    # deps for building python deps
    build-essential \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL "https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py" | python

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY pyproject.toml poetry.lock ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev



# `development` image is used during development / testing
FROM python-base as development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Setting up proper permissions:
#   - Create non-root user
#   - Make poetry runnable by non-root user
RUN adduser --disabled-password --shell /bin/bash --gecos "" --uid 1002 vscodebot \
    && chown vscodebot:vscodebot -R $POETRY_HOME

# quicker install as runtime deps are already installed
RUN poetry install

# will become mountpoint of our code
WORKDIR /workspace

# Running as non-root user:
USER vscodebot
