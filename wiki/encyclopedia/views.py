import markdown2

from django.forms import Form, CharField
from django.shortcuts import render
from django.http import HttpResponse

from . import util
    

class SearchForm(Form):
    query = CharField(label="q")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def search(request):
    if request.method == "POST":
        
        form = SearchForm(request.POST)

        if form.isvalid():
            return HttpResponse("YAY")

def wiki(request, title):
    entry = util.get_entry(title)

    # If entry returns none then it doesn't exist
    if not entry:
        return HttpResponse("<h1>Error 404: Entry not found</h1>")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry)
    })
