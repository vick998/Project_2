from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	id = models.BigAutoField(primary_key= True, unique= True)

class AuctionListing(models.Model):
	id = models.BigAutoField(primary_key= True, unique= True)
	user_name = models.ForeignKey(User, on_delete = models.CASCADE, default = "victor")
	listingname = models.CharField(max_length = 50)
	listingdesc = models.CharField(max_length = 200, blank = True)
	listingurl = models.CharField(max_length = 100, blank = True)
	listingcategory = models.CharField(max_length = 20, blank = True)
	liquid = models.BooleanField(default = True)
	initbid = models.IntegerField()

	def __str__(self):
		return f"{self.user_name} is selling {self.listingname} for {self.initbid}" 

class AuctionBid(models.Model):
	id = models.BigAutoField(primary_key= True, unique= True)
	username_bid = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, default = "victor")
	listingname_bid = models.CharField(max_length = 50, blank = True)
	listingnameid_bid =  models.IntegerField(default = 0)
	followbid = models.IntegerField()

	def __str__(self):
		return f"A bid of {self.followbid} has been entered for {self.listingname_bid} by {self.username_bid}"

class ListingComment(models.Model):
	id = models.BigAutoField(primary_key= True, unique= True)
	username_comm = models.ForeignKey(User, on_delete = models.CASCADE, default = "victor")
	listingname_comm = models.CharField(max_length = 50, blank = True)
	listingnameid_comm =  models.IntegerField(default = 0)
	listing_comm = models.CharField(max_length = 100)

	def __str__(self):
		return f"{self.username_comm} has commented '{self.listing_comm}' on listing {self.listingname_comm}"

class ListingWatchlist(models.Model):
	id = models.BigAutoField(primary_key= True, unique= True)
	username_watchlist = models.ForeignKey(User, on_delete = models.CASCADE, default = "victor")
	listingname_watchlist = models.CharField(max_length = 50, blank = True)
	listingnameid_watchlist =  models.IntegerField(default = 0, unique= True)

	def __str__(self):
		return f"{self.username_watchlist}'s wishlist contains the entries '{self.listingname_watchlist}'"