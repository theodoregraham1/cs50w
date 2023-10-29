from django.contrib.auth import authenticate, login, logout, decorators
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .forms import AddListingForm, AddBidForm
from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings,
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
            messages.error(request, "Invalid username and/or password.")
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")


@decorators.login_required
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
            messages.error(request, "Passwords must match.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "auctions/register.html")
        
        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@decorators.login_required
def add(request):
    if request.method != "POST":
        return render(request, "auctions/add.html", {
            "form": AddListingForm
        })

    form = AddListingForm(request.POST)

    if form.is_valid():

        form.save()

        messages.success(request, 'Listing created successfully')
        return HttpResponseRedirect(reverse("index"))

    messages.error(request, "New listing invalid.")
    return render(request, "auctions/add.html", {
            "form": form
        })


def listing_view(request, id):
    listing = Listing.objects.get(id=id)

    if not request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
            "listing": listing
        })
    
    if request.method != "POST":
        return render(request, "auctions/listing.html", {
            "watchlisted": (listing in request.user.watchlist.all()),
            "listing": listing,
            "form": AddBidForm,
        })
    
    # Add bid


@decorators.login_required
def add_to_watchlist(request, id):
    listing = Listing.objects.get(id=id)

    if (listing not in request.user.watchlist.all()):
        request.user.watchlist.add(listing)
        messages.success(request, "Listing added to watchlist")
    else:
        request.user.watchlist.remove(listing)
        messages.info(request, "Listing removed from watchlist")

    return HttpResponseRedirect(reverse("listing", args=[id]))


@decorators.login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })