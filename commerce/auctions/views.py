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
    listingentries = list(AuctionListing.objects.all())
    if request.method == "POST":
        listingdata = []
        listingdata.append(request.user)
        listingdata.append(request.POST["listingname"])
        listingdata.append(request.POST["listingdesc"])
        listingdata.append(request.POST["listingcategory"])
        listingdata.append(request.POST["listingurl"])
        listingdata.append(request.POST["initbid"])
        try:
            listing = AuctionListing(user_name=listingdata[0], listingname=listingdata[1], listingdesc=listingdata[2],  listingcategory=listingdata[3], listingurl=listingdata[4], initbid=listingdata[5])
            k0 = 0
            for lentry in listingentries:
                listingdata0 = [lentry.user_name, lentry.listingname, lentry.listingdesc, lentry.listingcategory, lentry.listingurl, lentry.initbid]
                k = 0
                for i in range(6):
                    if listingdata[i]==listingdata0[i]:
                        k += 1
                if k == 6:
                    k0 += 1
                else: 
                    k0 += 0
            if k0 != 0:
                return render(request, "auctions/listingentry.html", {
                    "message": "Listing already exists."
                    })
            else:
                listing.save()
                # redo for liquidity
        except IntegrityError:
            return render(request, "auctions/listingentry.html", {
                # "message": "Listing already exists."
            })
        return HttpResponseRedirect(reverse("listingpage", args=(listing.id,)))
        # return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/listingentry.html")

def listingpage(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    auctionbidall = list(AuctionBid.objects.all())
    if request.user.is_authenticated:
        if request.method == "POST":
            if listing.user_name != request.user:
                username_bid_v = request.user
                listingname_bid_v = listing.listingname
                followbid_v = request.POST["newbid"]
                try:
                    auctionbid = AuctionBid.objects.create(username_bid=username_bid_v, listingname_bid=listingname_bid_v, followbid=followbid_v)
                    auctionbid.save()
                    if int(auctionbid.followbid) > int(listing.initbid) :
                        listing.initbid = auctionbid.followbid
                        listing.save()
                except IntegrityError:
                    return HttpResponseRedirect(reverse("index"))
                return render(request, "auctions/listingpage.html", {
                    "listing": listing,
                    "auctionbidall" : list(AuctionBid.objects.all()),
                    "message": "Your bid is " + auctionbid.followbid
                })
            else:
                listing.liquid = False
                listing.save()
                return render(request, "auctions/listingpage.html", {
                    "listing": listing,
                    "auctionbidall" : list(AuctionBid.objects.all()),
                    "closed" : True,
                    "message": "Auction closed by owner"
                })
        else:
            if listing.user_name == request.user:
                return render(request, "auctions/listingpage.html", {
                    "listing": listing,
                    "auctionbidall" : list(AuctionBid.objects.all()),
                    "user_match" : True
                    })
            else:
                return render(request, "auctions/listingpage.html", {
                    "listing": listing,
                    "auctionbidall" : list(AuctionBid.objects.all()),
                    "user_match" : False
                    })
    else:
        return HttpResponseRedirect(reverse("index"))    

def watchlist(request, listing_id):
    if request.method == "POST":
        listing = AuctionListing.objects.get(id = listing_id)
        watchlist0 = ListingWatchlist(username_watchlist= request.user ,listingname_watchlist= listing.listingname,listingnameid_watchlist= listing.id)
        watchlist0.save()
    else:
        watchlist = list(ListingWatchlist.objects.all())
        wuser = []
        for w in watchlist:
            if request.user == w.username_watchlist:
                wuser.append(w)
        if len(wuser) == 0:
            return render(request, "auctions/watchlist.html",{
                "message":"No listings entered"
                })
        else:
            return render(request, "auctions/watchlist.html",{
                "listings": wuser
                })

def category(request):
    return render(request, "auctions/category.html", {
        "listings" : list(AuctionListing.objects.all())
        })

