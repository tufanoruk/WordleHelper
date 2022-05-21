# syntax = docker/dockerfile:1.3
# tag = toruk/wordlehelper:$version

FROM python:3.9-slim
RUN mkdir /app
COPY ./wordlehelp.py /app
COPY ./wordle-tr.txt /app
WORKDIR /app
ENTRYPOINT ["python", "wordlehelp.py", "wordle-tr.txt"]
