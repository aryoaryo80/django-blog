FROM python:slim-buster

WORKDIR /src
COPY . /src

RUN pip install -r requirements.txt

EXPOSE 8000
CMD [ "gunicorn", "blog.wsgi", "-b", "0.0.0.0:8000" ]
