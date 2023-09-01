from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea, URLInput, TextInput, NumberInput, Select

from .models import User, Listing, Bid, Comment


class AddListingForm(ModelForm):


    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category", "user_id"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "starting_bid": NumberInput(attrs={"class": "form-control"}),
            "image_url": URLInput(attrs={"class": "form-control"}),
            "category": TextInput(attrs={"class": "form-control"}),
            "user_id": Select(attrs={"class": "form-control"}),
        }

def index(request):
    return render(request, "auctions/index.html")


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
    

