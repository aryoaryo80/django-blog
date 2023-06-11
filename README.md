
<img src="https://mybocket1.s3.ir-thr-at1.arvanstorage.ir/Screenshot-from-2023-06-11-10-32-14.png" width="100%" height="33%">

# Django store

This is a blog with django and bootstrap

## Usage

Usage with docker 

```bash
## pull from docker hub and run
docker run -p 8000:8000  aryoaryo80/django-blog:1.0

## or

## build from . and run
git clone https://github.com/aryoaryo80/djnago-blog.git
cd django-blog
docker image build . -t django-blog:1.0 && docker run -p 8000:8000 django-blog:1.0

```

Then go to [localhost:8000](http://localhost:8000) to view site

## Features 🚀

- **Autentication**
- **CRUD Post**
- **Nested Comments on posts**
- **Like on post and comments**
- **Search post**