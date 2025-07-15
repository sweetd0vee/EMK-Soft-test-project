FROM python:3.9

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /python/
RUN mkdir /python/database
RUN mkdir /python/routes
RUN mkdir /python/schemas
RUN mkdir /python/utils

COPY database /python/database
COPY routes /python/routes
COPY schemas /python/schemas
COPY utils /python/utils
COPY main.py /python/main.py
COPY base_logger.py /python/base_logger.py

WORKDIR /python/

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host",  "0.0.0.0", "--port",  "8000", "main:app"]
