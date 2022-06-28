from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class RecipePost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="recipe_posts")
    content = models.TextField()
    featured_image = CloudinaryField("image", default="placeholder")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        sorted('-created_on')
