from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.models import User
from posts.models import Post, Vote, Comment
from .serializers import UserRegisterSerializer, UserSerializer, PostSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwner

User = get_user_model()


# User views (Register, Update, Delete, Read)
class UserRegisterView(APIView):
    """registration User"""
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            user = srz_data.create(srz_data.data)
            data = self.serializer_class(user).data
            del data['password']
            return Response(data, status.HTTP_201_CREATED)
        return Response(srz_data.errors, status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    """Update a user if user is owner
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.pop('pk'))
        self.check_object_permissions(request, user)
        srz_data = self.serializer_class(
            instance=user, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status.HTTP_202_ACCEPTED)
        return Response(srz_data.errors, status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    """ 
    Delete a user if user is owner
    """
    permission_classes = (IsAuthenticated, IsOwner)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.pop('pk'))
        self.check_object_permissions(request, user)
        user.delete()
        return Response({'message': 'your account has been deleted'}, status.HTTP_202_ACCEPTED)


class UserView(APIView):
    """ 
    Returns a User Information with all user posts
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        srz_data = self.serializer_class(request.user)
        return Response(srz_data.data, status.HTTP_200_OK)


# Post views (Read, Create, Update, Delete, Like)
class PostDetailView(APIView):
    """ 
    returns information about a post
    """
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = PostSerializer

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        srz_data = PostSerializer(post)
        return Response(srz_data.data, status.HTTP_200_OK)


class PostCreateView(APIView):
    """ 
    Create a new post 
    """
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = PostSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            post = srz_data.create(srz_data.data, request.user)
            srz_data = self.serializer_class(post)
            return Response(srz_data.data, status.HTTP_200_OK)
        return Response(srz_data.errors, status.HTTP_400_BAD_REQUEST)


class PostUpdateView(APIView):
    """ 
    Update a post data 
    """
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = PostSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post.user)
        srz_data = PostSerializer(post, request.data, partial=True)
        if srz_data.is_valid():
            post = srz_data.save()
            srz_data = PostSerializer(post)
            return Response(srz_data.data, status.HTTP_200_OK)


class PostDeleteView(APIView):
    """ 
    Delete a post
    """
    permission_classes = (IsAuthenticated, IsOwner)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post.user)
        post.delete()
        return Response({'success': f'post with id {pk} deleted'}, status.HTTP_200_OK)


class VoteView(APIView):
    """
    Create Like on a post
    """
    permission_classes = (IsAuthenticated, IsOwner)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        vote = post.votes.filter(user=request.user)
        if vote.exists():
            vote.delete()
            return Response({'message': 'Vote deleted'}, status.HTTP_200_OK)
        post.votes.create(user=request.user)
        return Response({'message': 'Vote created'}, status.HTTP_200_OK)
