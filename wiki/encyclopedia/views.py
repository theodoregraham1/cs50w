import markdown2

from django.forms import Form, CharField
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from . import util
 

class SearchForm(Form):
    q = CharField()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


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
    

def wiki(request, title):
    entry = util.get_entry(title)

    # If entry returns none then it doesn't exist
    if not entry:
        return HttpResponse("<h1>Error 404: Entry not found</h1>")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry),
        "form": SearchForm()
    })
