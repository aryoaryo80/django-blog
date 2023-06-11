from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=500)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now=True)
    votes = GenericRelation('Vote', related_query_name='posts')

    def __str__(self):
        return f'{self.title[:20]}'

    def get_absolute_url(self):
        return reverse('posts:detail', args=(self.slug,))

    def get_user_profile_url(self):
        return reverse('posts:profile', args=(self.user.id,))

    def comment_count(self):
        count = self.comments.count()
        if count > 0:
            return f'{count} Comments'
        return '0 comments'

    def likes_count(self):
        count = self.votes.count()
        if count > 0:
            return f'{count} likes'
        return f'0 likes'

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    is_sub = models.BooleanField(default=False)
    sub = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='nested', blank=True, null=True)
    votes = GenericRelation('Vote', related_query_name='comments')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user}'

    def likes_count(self):
        count = self.votes.count()
        if count > 0:
            return f'{count}'
        return 0


class Vote(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='votes')
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f'{self.user} liked {self.content_object}'
