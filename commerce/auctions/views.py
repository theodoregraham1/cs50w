from django.contrib.auth import authenticate, login, logout, decorators
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from . import utils 
from .forms import AddListingForm, AddBidForm, AddCommentForm
from .models import User, Listing


def index(request):
    listings = []
    raw_listings = Listing.objects.all()

    for listing in raw_listings:
        listings.append(utils.produce_listing(request.user, listing))

    listings.sort(key=lambda listing: listing["listing"].id)
    listings.reverse()

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
    listing = utils.produce_listing(request.user, Listing.objects.get(id=id))
    output = {
        "bid_form": AddBidForm,
        "comment_form": AddCommentForm,
        "num_bids": len(listing["listing"].bids.all()),
        "comments": listing["listing"].comments.all(),
    }
    output.update(listing)

    return render(request, "auctions/listing.html", output)
    

@decorators.login_required
def add_bid(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    
    form = AddBidForm(request.POST)

    if form.is_valid():
        bid = form.cleaned_data

        current_price = utils.get_top_bid(bid["listing"])[0]

        if (bid["value"] > current_price
                or (bid["value"] == bid["listing"].starting_bid and current_price == bid["listing"].starting_bid)):
            form.save()

            messages.success(request, "Bid added successfully")
        else:
            messages.error(request, "Bid must be above the current bid")

        return HttpResponseRedirect(reverse("listing", args=[bid["listing"].id,]))

    else:
        messages.error(request, "Bid invalid")

    return HttpResponseRedirect(reverse("index"))


@decorators.login_required
def add_to_watchlist(request, id):
    # Add or remove item from user's watchlist
    listing = Listing.objects.get(id=id)

    if listing not in request.user.watchlist.all():
        request.user.watchlist.add(listing)
        messages.success(request, "Listing added to watchlist")
    else:
        request.user.watchlist.remove(listing)
        messages.info(request, "Listing removed from watchlist")

    return HttpResponseRedirect(reverse("listing", args=[id]))


@decorators.login_required
def watchlist(request):
    listings = []
    raw_listings = Listing.objects.all()

    for l in raw_listings:
        new_listing = utils.produce_listing(request.user, l)

        if new_listing["watchlisted"]:
            listings.append(new_listing)

    listings.sort(key=lambda l: l["listing"].id)
    listings.reverse()

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@decorators.login_required
def close(request, id):
    listing = Listing.objects.get(id=id)

    if listing.user == request.user:
        listing.active = False
        listing.save()
        messages.warning(request, "Listing closed successfully")
    else:
        messages.error(request, "You are not the owner of this listing")
    
    return HttpResponseRedirect(reverse("listing", args=[id,]))


@decorators.login_required
def comment(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))

    form = AddCommentForm(request.POST)

    if form.is_valid():
        form.save()

        messages.success(request, "Comment added successfully")
        return HttpResponseRedirect(reverse("listing", args=[form.cleaned_data["listing"].id]))

    messages.error(request, "Comment invalid")
    try:
        return HttpResponseRedirect(reverse("listing", args=[form.cleaned_data["listing"].id]))
    except:
        return HttpResponseRedirect(reverse("index"))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": utils.get_categories(request.user),
    })


def category(request, name):
    try:
        category = next(c for c in utils.get_categories(request.user) if c["name"] == name)
    except StopIteration:
        return HttpResponseRedirect(reverse("categories"))

    print(category)
    return render(request, "auctions/category.html", {
        "category": category,
    })
