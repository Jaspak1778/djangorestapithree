# main/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created', 'updated']
        

class CommentSerializer(serializers.ModelSerializer):
    commenter = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'commenter', 'post', 'comment_content', 'created']  # päivitetty kentät 'user' -> 'commenter', 'content' -> 'comment_content', ja 'created_at' -> 'created'
        read_only_fields = ['commenter', 'created']  # commenter kenttä vain luettavaksi
        
class LikeSerializer(serializers.ModelSerializer):
    liker = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'liker', 'post']  # päivitetty kenttä 'user' -> 'liker'

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data.get('first_name', ''),  # Oikea tapa käyttää get()
        last_name=validated_data.get('last_name', '')     # Oikea tapa käyttää get()
    )
        user.set_password(validated_data['password'])
        user.save()
        return user
