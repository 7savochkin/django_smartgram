from django.contrib.auth import get_user_model
from django.db import models

from smartgram.mixins.model_mixins import PrimaryKeyMixin

User = get_user_model()


class Post(PrimaryKeyMixin):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='post_author')
    image = models.ImageField(upload_to='posts/')
    description = models.TextField(blank=True)
    likes = models.ManyToManyField(User, blank=True)
    place = models.CharField(max_length=75, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Post of {self.author.username}"

    @property
    def likes_count(self):
        if self.likes.count() == 0:
            return f"{self.likes.count()} likes"
        elif self.likes.count() == 1:
            return f"liked by {self.likes.last().username}"
        return f"liked by {self.likes.last().username} and {self.likes.count() - 1} others"
