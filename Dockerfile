FROM python:3.8

RUN apt-get update -y
# установка pipenv
RUN apt-get -y install pipenv

WORKDIR /app
# копирование всех важных файлов в рабочую директорию
COPY . /app
EXPOSE 5000
# запуск pipenv
RUN set -ex && pipenv install --deploy --system

ENTRYPOINT ["pipenv", "run", "python m", "configure_and_run.py", "&"]