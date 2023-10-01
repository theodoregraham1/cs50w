from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    watchlist = models.ManyToManyField('Listing', related_name="watchers")

class Listing(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.URLField(null=True)
    category = models.CharField(max_length=64, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")


class Bid(models.Model):
    id = models.AutoField(primary_key=True)

    value = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
 