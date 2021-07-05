from django.contrib import admin
from .models import AuctionListing, AuctionBid, ListingComment, ListingWatchlist
# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(AuctionBid)
admin.site.register(ListingComment)
admin.site.register(ListingWatchlist)


