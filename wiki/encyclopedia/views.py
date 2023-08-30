import markdown2
import random

from django.forms import Form, CharField, widgets
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import util


class EditForm(Form):
    content = CharField(
        widget=widgets.Textarea(),
        label="",
        ) 

class SearchForm(Form):
    q = CharField()

class NewEntryForm(Form):
    title = CharField(
        widget=widgets.TextInput(
            attrs={'placeholder': 'Title',
                'style': 'width: 80%'}),
        label="")

    content = CharField(
        widget=widgets.Textarea(
            attrs={'rows': '3',
                'placeholder': 'Content',}),
        label="")


def index(request):
    """ Display homepage """

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def add(request):
    """ Add new entry to wiki """

    # Render new entry page
    if request.method == "GET":
        return render(request, "encyclopedia/add.html", {
            "form": NewEntryForm
        })
    
    # Add new entry to database
    form = NewEntryForm(request.POST)

    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"].encode()

        if title in util.list_entries():
            return(HttpResponse("<h1>Error 500: Entry name already exists</h1>"))
        
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("wiki", args=[title]))

    return HttpResponse("<h1>Error 500: Form invalid</h1>")


def edit(request, title):
    """ Edit existing wiki entry """

    # Render edit page with entry data pre-loaded
    if request.method == "GET":
        entry = util.get_entry(title)

        # Ensure entry exists
        if not entry:
            return HttpResponse("<h1>Error 404: Entry not found</h1>")

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": EditForm({"content": entry}),
        })

    # Edit database record based on request
    form = EditForm(request.POST)

    if form.is_valid():
        content = form.cleaned_data["content"].encode()

        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("wiki", args=[title]))

    return HttpResponse("<h1>Error 500: Form invalid</h1>")


def random_page(request):
    """ Display random entry """

    titles = util.list_entries()

    return HttpResponseRedirect(reverse("wiki", args=[random.choice(titles)]))


def search(request):
    """ Search wiki entries """

    if request.method == "GET":
        return HttpResponseRedirect(reverse("index"))

    form = SearchForm(request.POST)

    if form.is_valid():
        query = form.cleaned_data["q"]

        entries = util.list_entries()

        # If query is a direct match, go to that page
        if query in entries:
            return HttpResponseRedirect(reverse("wiki", args=[query]))
        
        # Check all entries for the query as a substrings
        results = []
        for entry in entries:
            if query in entry:
                results.append(entry)

        return render(request, "encyclopedia/search.html", {
            "results": results
        })
    
    return HttpResponseRedirect(reverse("index"))
    

def wiki(request, title):
    """ Display wiki entry """

    entry = util.get_entry(title)

    # Ensure entry exists
    if not entry:
        return HttpResponse("<h1>Error 404: Entry not found</h1>")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry),
    })
