from csv import reader, DictReader
from datetime import datetime
from posts.models import User, Post
from django.utils.text import slugify


def ok():

    with open('WinnersInterviewBlogPosts.csv') as csvfile:
        data = DictReader(csvfile)
        user = User.objects.get(username='root')
        for i in data:
            pub_date = i['publication_date']
            pub_date = datetime.strptime(pub_date, '%Y-%m-%d %H:%M:%S')
            print(i.keys())
            Post.objects.create(
                user=user,
                title=i['title'],
                content=i['content'],
                slug=slugify(i['title'][:100]),
                created=pub_date,
            )
