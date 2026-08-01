from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

class Blog(models.Model):
    author = models.TextField(
        max_length=100,
        blank=True,
        null=True,
        default="unknown user",
        editable=False
    )
    title = models.CharField(
        max_length=100,
        unique=False,
    )
    desc = models.TextField(max_length=200, blank=False)
    blog_content = models.TextField(blank=True, null=True)
    thumbnail = models.URLField(max_length=400)
    read_more = models.URLField(max_length=400, blank=True)
    category = models.CharField(max_length=10, blank=True)
    id = models.AutoField(primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    approve_status = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title


class AccessRequest(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='access_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']

    def __str__(self):
        return f"{self.user.username} -> {self.post.title} ({'✅' if self.is_approved else '⏳'})"