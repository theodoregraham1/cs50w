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
        fields = ["title", "description", "starting_bid", "image_url", "category", "user"]

        widgets = {
            "title": TextInput(attrs={"class": "form-control", 
                                      "placeholder": "Title",}),
            "description": Textarea(attrs={"class": "form-control", 
                                           "placeholder": "Description",}),
            "starting_bid": NumberInput(attrs={"class": "form-control", 
                                               "placeholder": "Starting Bid",}),
        }


class AddBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["value", "listing", "user",]

        widgets = {
            "value": TextInput(attrs={"class": "form-control",
                                      "placeholder": "Bid"}),
        }