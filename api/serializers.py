from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Vote

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'confirm_password', 'age',
                  'full_name', 'biography', 'phone_number', 'email')
        extra_kwargs = {
            'id': {'read_only': True},
            'age': {'required': False},
            'full_name': {'required': False},
            'biography': {'required': False},
            'phone_number': {'required': False},
            'email': {'required': False},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                'password and confirm_password must be match')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'], password=validated_data['password'])
        user.age = validated_data['age']
        user.full_name = validated_data['full_name']
        user.biography = validated_data['biography']
        user.email = validated_data['email']
        user.phone_number = validated_data['phone_number']
        user.save()
        del validated_data['password']
        return user


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        exclude = ('is_admin', 'is_active', 'is_superuser',
                   'last_login', 'groups', 'user_permissions', 'password')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def get_posts(self, obj):
        return PostSerializer(obj.posts.all(), many=True).data


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def create(self, data, user):
        post = Post.objects.create(user=user, **data)
        return post

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj, is_sub=False)
        return CommentSerializer(comments, many=True).data

    def get_likes(self, obj):
        likes = obj.votes.count()
        return likes


class CommentSerializer(serializers.ModelSerializer):
    sub_comments = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_sub_comments(self, obj):
        comments = Comment.objects.filter(sub=obj)
        return SubCommentSerializer(comments, many=True).data

    def get_likes(self, obj):
        likes = obj.votes.count()
        return likes


class SubCommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_likes(self, obj):
        likes = obj.votes.count()
        return likes
