FROM python:3.10-slim as build

WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10-slim

RUN groupadd -g 999 ytgpt && useradd -r -u 999 -g ytgpt ytgpt

RUN mkdir /usr/app && chown ytgpt:ytgpt /usr/app
WORKDIR /usr/app

COPY --chown=ytgpt:ytgpt --from=build /usr/app/venv ./venv
COPY --chown=ytgpt:ytgpt . .
USER 999

ENV PATH="/usr/app/venv/bin:$PATH"
EXPOSE 8000


ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "app.main:app"]
