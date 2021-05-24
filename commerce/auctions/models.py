from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
	user_name = models.ForeignKey(User, on_delete = models.CASCADE)
	listingname = models.CharField(max_length = 50)
	initbid = models.IntegerField()

	def __str__(self):
		return f"{self.user_name} is selling {self.listingname} for {self.initbid}" 

class AuctionBid(models.Model):
	user_name = models.ManyToManyField(User, blank=True)
	listing_name = models.ForeignKey(AuctionListing, on_delete = models.CASCADE)
	followbid = models.IntegerField()

	def __str__(self):
		return f"A bid of {self.followbid} has been entered for {self.listing_name} by {self.user_name}"

class ListingComment(models.Model):
	user_name = models.ForeignKey(User, on_delete = models.CASCADE)
	listing_name = models.ForeignKey(AuctionListing, on_delete = models.CASCADE)
	listing_comm = models.CharField(max_length = 100)
