from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea, URLInput, TextInput, NumberInput, URLField, CharField

from .models import User, Listing, Bid, Comment


class AddListingForm(ModelForm):
    image_url = URLField(required=False, 
                         widget=URLInput(attrs={"class": "form-control", 
                                                "placeholder": "Image",},))
    category = CharField(required=False, 
                         widget=TextInput(attrs={"class": "form-control", 
                                         "placeholder": "Category",}))

    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category",]

        widgets = {
            "title": TextInput(attrs={"class": "form-control", 
                                      "placeholder": "Title",}),
            "description": Textarea(attrs={"class": "form-control", 
                                           "placeholder": "Description",}),
            "starting_bid": NumberInput(attrs={"class": "form-control", 
                                               "placeholder": "Starting Bid",}),
        }

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
    

def add(request):
    if request.method != "POST":
        return render(request, "auctions/add.html", {
            "form": AddListingForm
        })

    form = AddListingForm(request.POST)

    if form.is_valid():

        listing = form.save()

        return HttpResponseRedirect(reverse("index"))

        
    return render(request, "auctions/add.html", {
            "form": form
        })

    

