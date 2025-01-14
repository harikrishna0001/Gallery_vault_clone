from django.db import models
from django.contrib.auth.models import User

class Gallery(models.Model):
    feedimage = models.ImageField(upload_to='gallery_images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} by {self.user.username}"
