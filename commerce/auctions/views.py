from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import AuctionListing, AuctionBid, ListingComment, ListingWatchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings" : list(AuctionListing.objects.all())
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user) 
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listentry(request):
    if request.method == "POST":
        listingname = request.POST["listingname"]
        listingdesc = request.POST["listingdesc"]
        listingcategory = request.POST["listingcategory"]
        listingurl = request.POST["listingurl"]
        initbid = request.POST["initbid"]
        try:
            listing = AuctionListing.objects.create(user, listingname, listingdesc, listingurl, listingcategory, initbid)
            listing.save()
        except IntegrityError:
            return render(request, "auctions/listingentry.html", {
                "message": "Listing already exists."
            })
        # return HttpResponseRedirect(reverse("listingpage", args=(listing.id,)))
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/listingentry.html")

def listingpage(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    # if request.user.is_authenticated:
        # if request.method == "POST":
            # if AuctionListing.user_name == request.user.username:
                # username_bid = request.user.username
                # listingname_bid = listing.listingname
                # followbid = request.POST["newbid"]
                # try:
                #     auctionbid = AuctionBid.objects.create(username_bid, listingname_bid, followbid)
                #     auctionbid.save()
                #     return HttpResponseRedirect(reverse("index"))
                # except IntegrityError:
                #     return render(request, "auctions/listingpage.html", {
                #         "listing": listing,
                #         "message": "Bid already entered."
                #     })
            # else:
            #     return render(request, "auctions/listingpage.html", {
            #         "listing": listing,
            #         "message": "Auction closed by owner"
            #     })
        # else:
            # if AuctionListing.user_name == request.user.username:
    return render(request, "auctions/listingpage.html", {
            "listing": listing,
            "user_match" : True
        })
            # else:
            #     return render(request, "auctions/listingpage.html", {
            #         "listing": listing,
            #         "user_match" : False
            #         })
    # else:
    #     return HttpResponseRedirect(reverse("index"))    

def watchlist(request):
    listings = list(AuctionListing.objects.all())
    listingspec = []
    for listing in listings:
        if user.username == listing.user_name:
            listingspec.append(listing)
    if len(listingspec) == 0:
        return render(request, "auctions/watchlist.html",{
            "message":"No listings entered"
            })
    else:
        return render(request, "auctions/watchlist.html",{
            "listings":listingspec
            })

def category(request):
    return render(request, "auctions/category.html", {
        "listings" : list(AuctionListing.objects.all())
        })

