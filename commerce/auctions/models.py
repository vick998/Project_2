from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	user_id = models.BigAutoField(primary_key=True)

class AuctionListing(models.Model):
	listing_id = models.BigAutoField(primary_key=True)
	user_name = models.ForeignKey(User, on_delete = models.CASCADE, default = "victor")
	listingname = models.CharField(max_length = 50)
	listingdesc = models.CharField(max_length = 200)
	listingurl = models.CharField(max_length = 100)
	listingcategory = models.CharField(max_length = 20)
	initbid = models.IntegerField()

	def __str__(self):
		return f"{self.user_name} is selling {self.listingname} for {self.initbid}" 

class AuctionBid(models.Model):
	bid_id = models.BigAutoField(primary_key=True)
	username_bid = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, default = "victor")
	listingname_bid = models.CharField(max_length = 50, blank = True)
	followbid = models.IntegerField()

	def __str__(self):
		return f"A bid of {self.followbid} has been entered for {self.listingname_bid} by {self.username_bid}"

class ListingComment(models.Model):
	comm_id = models.BigAutoField(primary_key=True)
	username_comm = models.ForeignKey(User, on_delete = models.CASCADE, default = "victor")
	listingname_comm = models.CharField(max_length = 50, blank = True)
	listing_comm = models.CharField(max_length = 100)

	def __str__(self):
		return f"{self.username_comm} has commented '{self.listing_comm}' on listing {self.listingname_comm}"

class ListingWatchlist(models.Model):
	watchlist_id = models.BigAutoField(primary_key=True)
	username_watchlist = models.ForeignKey(User, on_delete = models.CASCADE, default = "victor")
	listingname_watchlist = models.CharField(max_length = 50, blank = True)

	def __str__(self):
		return f"{self.username_watchlist}'s wishlist contains the entries '{self.listingname_watchlist}'"