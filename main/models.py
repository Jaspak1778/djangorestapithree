# main/models.py

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    content = models.TextField()  # Postin sisältö
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}..."

class Comment(models.Model):
    comment_content = models.TextField()  # Kommentin sisältö
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.commenter.username} - {self.comment_content[:20]}..."

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.liker.username} liked {self.post.content[:20]}..."
