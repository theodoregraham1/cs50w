from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.URLField(null=True)
    category = models.CharField(max_length=64, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")


class Bid(models.Model):
    pass
class Comment(models.Model):
    pass 