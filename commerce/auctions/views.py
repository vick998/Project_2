from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import AuctionListing, AuctionBid, ListingComment, ListingWatchlist

# cute bug, using the same form in a different instance confuses the is_valid clause

class WatchlistForm(forms.Form):
    stvw = forms.BooleanField(initial=False)

class CloseForm(forms.Form):
    stvcf = forms.BooleanField(initial=False)

class BidForm(forms.Form):
    stvb = forms.IntegerField(label="newbid")

class ListingForm(forms.Form):
    stvname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    stvdesc = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    stvcat = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Category'}))
    stvurl = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Image URL'}))
    stvbid = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Starting Bid'}))

class CommentForm(forms.Form):
    stvcomm = forms.CharField()

class DeletionForm(forms.Form):
    stvdel = forms.BooleanField(initial=True)
    stvdelid = forms.IntegerField()

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


def listingsubexist(user_name_s, listingname_s, listingdesc_s, listingcategory_s, listingurl_s, initbid_s, liquid_s):
    listingentries = list(AuctionListing.objects.all())
    listingdata = [user_name_s, listingname_s, listingdesc_s, listingcategory_s, listingurl_s, int(initbid_s), liquid_s]
    k0 = 0
    for lentry in listingentries:
        listingdata0 = [lentry.user_name, lentry.listingname, lentry.listingdesc, lentry.listingcategory, lentry.listingurl, int(lentry.initbid), lentry.liquid]
        k = 0
        for i in range(0,len(listingdata0)):
            if listingdata[i] == listingdata0[i]:
                k = k + 1
        if k == 7:
            k0 = k0 + 1
    if k0 != 0:
        return True
    else:
        return False


def listentry(request):
    lform = ListingForm(request.POST)
    if request.method == "POST":
        if lform.is_valid():
            user_name_s = request.user
            listingname_s = lform.cleaned_data["stvname"]
            listingdesc_s = lform.cleaned_data["stvdesc"]
            listingcategory_s = lform.cleaned_data["stvcat"]
            listingurl_s = lform.cleaned_data["stvurl"]
            initbid_s = lform.cleaned_data["stvbid"]
            liquid_s = True
            if listingsubexist(user_name_s, listingname_s, listingdesc_s, listingcategory_s, listingurl_s, initbid_s, liquid_s) == True:
                return render(request, "auctions/listingentry.html", {
                    "lform": ListingForm(),
                    "message": "Listing already exists."
                    })
            else:
                listing = AuctionListing(user_name=user_name_s, listingname=listingname_s, listingdesc=listingdesc_s,  listingcategory=listingcategory_s, listingurl=listingurl_s, initbid=initbid_s, liquid=liquid_s)
                listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/listingentry.html", {
            "lform": ListingForm()
            })


def listingpage(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    if request.method == "POST":
        cform = CommentForm(request.POST)
        wform = WatchlistForm(request.POST)
        bform = BidForm(request.POST)
        delform = CloseForm(request.POST)
        dbform = DeletionForm(request.POST)
        dcform = DeletionForm(request.POST)
        if bform.is_valid():
            username_bid_v = request.user
            listingname_bid_v = listing.listingname
            followbid_v = bform.cleaned_data["stvb"]
            try:
                auctionbid = AuctionBid.objects.create(username_bid=username_bid_v, listingname_bid=listingname_bid_v, listingnameid_bid=listing.id, followbid=followbid_v)
                auctionbid.save()
                if auctionbid.followbid > listing.initbid :
                    listing.initbid = auctionbid.followbid
                    listing.save()
            except IntegrityError:
                return HttpResponseRedirect(reverse("index"))
            return render(request, "auctions/listingpage.html", {
                "listing": listing,
                "bform" : BidForm(),
                "cform" : CommentForm(),
                # "stvw": True,
                "wform" : WatchlistForm(),
                "delform" : CloseForm(),
                # "stvdelid":listing.id,
                # "dcform" : DeletionForm(),
                # "dbform" : DeletionForm({"stvdelid":listing.id}),
                "auctionbidall" : list(AuctionBid.objects.all()),
                "wlisting" : wlist(request.user),
                "lcommall" : list(ListingComment.objects.all()),
                "message": "Your bid is " + str(auctionbid.followbid),
                "user_match" : False
                })

        if delform.is_valid():
            listing.liquid = False
            listing.save()
            return render(request, "auctions/listingpage.html", {
                "listing": listing,
                "bform" : BidForm(),
                "cform" : CommentForm(),
                # "stvw": True,
                # "stvdelid":listing.id,
                "wform" : WatchlistForm(),
                "delform" : CloseForm(),
                # "dcform" : DeletionForm(),
                # "dbform" : DeletionForm({"stvdelid":listing.id}),
                "auctionbidall" : list(AuctionBid.objects.all()),
                "wlisting" : wlist(request.user),
                "lcommall" : list(ListingComment.objects.all()),
                "closed" : True,
                "message": "Auction closed by owner",
                "user_match" : True
                    })

        if cform.is_valid():
            listing_comm_s = cform.cleaned_data["stvcomm"]    
            clisting = ListingComment(username_comm=request.user, listingname_comm=listing.listingname, listingnameid_comm=listing.id, listing_comm=listing_comm_s)
            clisting.save()
            return HttpResponseRedirect(reverse("index"))

        if wform.is_valid():
            wlisting = ListingWatchlist(username_watchlist=request.user, listingname_watchlist=listing.listingname, listingnameid_watchlist=listing.id)
            wlisting.save()
            return HttpResponseRedirect(reverse("watchlist"))

        # if request.user.is_superuser:
        #     if dbform.is_valid():
        #         delbid = dbform.cleaned_data["stvdel"]      
        #         AuctionBid.objects.get(id=delbid).delete()
        #     return HttpResponseRedirect(reverse("index"))

        #     if dcform.is_valid():
        #         delcomm = dcform.cleaned_data["stvdel"]    
        #         ListingComment.objects.get(id=delcomm).delete()
        #     return HttpResponseRedirect(reverse("index"))

    else:
        if listing.user_name == request.user:
            return render(request, "auctions/listingpage.html", {
                "listing": listing,
                "bform" : BidForm(),
                "cform" : CommentForm(),
                # "stvw": True,
                "wform" : WatchlistForm(),
                "delform" : CloseForm(),
                # "stvdel" : "comm.id",
                # "stvdel" : "auctionbid0.id",
                # "dcform" : DeletionForm({"stvdel" : "comm.id",}),
                # "dbform" : DeletionForm({"stvdel" : "auctionbid0.id"}),
                "auctionbidall" : list(AuctionBid.objects.all()),
                "wlisting" : wlist(request.user),
                "lcommall" : list(ListingComment.objects.all()),
                "user_match" : True
                })
        else:
            return render(request, "auctions/listingpage.html", {
                "listing": listing,
                "bform" : BidForm(),
                "cform" : CommentForm(),
                # "stvw": True,
                "wform" : WatchlistForm(),
                "delform" : CloseForm(),
                # "stvdel" : "comm.id",
                # "stvdel" : "auctionbid0.id",
                # "dcform" : DeletionForm({"stvdel" : "comm.id",}),
                # "dbform" : DeletionForm({"stvdel" : "auctionbid0.id"}),
                "auctionbidall" : list(AuctionBid.objects.all()),
                "wlisting" : wlist(request.user),
                "lcommall" : list(ListingComment.objects.all()),
                "user_match" : False
                })

def admlistingpage(request,listing_id):
    pass


def wlist(user):
    wlisting1 = []
    wlisting = list(ListingWatchlist.objects.all())
    for w in wlisting:
        if w.username_watchlist == user:
            wlisting1.append(w.listingnameid_watchlist)
    return wlisting1

def watchlist(request):
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
        wuser0 = []
        listings0 = []
        for w in wuser:
            wuser0.append(int(w.listingnameid_watchlist))
        listings = list(AuctionListing.objects.all())
        for w in wuser0:
            for l in listings:
                if w == l.id:
                    listings0.append(l)
        return render(request, "auctions/watchlist.html",{
            "listings": listings0
            })

def category(request):
    listingsall = list(AuctionListing.objects.all())
    lcategories0 = []
    lcategories = []
    for listing in listingsall:
        lcategories0.append(listing.listingcategory)
    slcategories = set(lcategories0)
    return render(request, "auctions/category.html", {
        "categories" : slcategories,
        })

def speccategory(request,l_cat):
    return render(request, "auctions/speccategory.html", {
        "listings" : list(AuctionListing.objects.filter(listingcategory = l_cat))
        })
