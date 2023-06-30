FROM python:slim-buster

WORKDIR /src
COPY . /src

RUN pip install -r requirements.txt --timeout=50

CMD [ "gunicorn", "blog.wsgi", "-b", "0.0.0.0:8000" ]
