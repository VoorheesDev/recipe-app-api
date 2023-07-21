FROM python:3.10-alpine3.18

ENV PYTHONBUFFERED 1

COPY ./requirements /tmp/requirements
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    if [ "$DEV" = true ]; then \
      /venv/bin/pip install -r /tmp/requirements/dev.txt ; \
    else  \
      /venv/bin/pip install -r /tmp/requirements/prod.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/venv/bin:$PATH"

USER django-user
