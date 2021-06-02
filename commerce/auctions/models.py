from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	id = models.BigAutoField(primary_key=True)

class AuctionListing(models.Model):
	id = models.BigAutoField(primary_key=True)
	user_name = models.ForeignKey(User, on_delete = models.CASCADE)
	listingname = models.CharField(max_length = 50)
	listingdesc = models.CharField(max_length = 200)
	initbid = models.IntegerField()

	def __str__(self):
		return f"{self.user_name} is selling {self.listingname} for {self.initbid}" 

class AuctionBid(models.Model):
	id = models.BigAutoField(primary_key=True)
	username_bid = models.ForeignKey(User, on_delete = models.CASCADE, blank = True)
	listingname_bid = models.CharField(max_length = 50, default = "Epoxy")
	followbid = models.IntegerField()

	def __str__(self):
		return f"A bid of {self.followbid} has been entered for {self.listingname_bid} by {self.username_bid}"

class ListingComment(models.Model):
	id = models.BigAutoField(primary_key=True)
	username_comm = models.ForeignKey(User, on_delete = models.CASCADE)
	listingname_comm = models.CharField(max_length = 50)
	listing_comm = models.CharField(max_length = 100)

	def __str__(self):
		return f"{self.username_comm} has commented '{self.listing_comm}' on listing {self.listingname_comm}"