import markdown2

from django.forms import Form, CharField, widgets
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import util


class SearchForm(Form):
    q = CharField()

class NewEntryForm(Form):
    title = CharField(widget=widgets.TextInput(
        attrs={'placeholder': 'Title',
               'style': 'width: 80%'}
        ),
        label="")
    content = CharField(widget=widgets.Textarea(
        attrs={'rows': '3',
               'placeholder': 'Content',}
        ),
        label="")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def add(request):

    if request.method == "GET":
        return render(request, "encyclopedia/add.html", {
            "form": NewEntryForm
        })
    
    form = NewEntryForm(request.POST)

    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        if title in util.list_entries():
            return(HttpResponse("<h1>Error 500: Entry name already exists</h1>"))
        
        util.save_entry(title, content)

        return HttpResponseRedirect(reverse("wiki", args=[title]))

def search(request):

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
    entry = util.get_entry(title)

    # If entry returns none then it doesn't exist
    if not entry:
        return HttpResponse("<h1>Error 404: Entry not found</h1>")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry),
    })
