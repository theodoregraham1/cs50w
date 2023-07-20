import markdown2

from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    entry = util.get_entry(title)

    # Entry returns none
    if not entry:
        return HttpResponse("<h1>Error 404: Entry not found</h1>")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry)
    })
