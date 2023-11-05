from .models import Listing


def gbp(i):
    return f"£{i:.2f}"


def get_top_bid(listing):
    if list(listing.bids.all()):
        top_bid = max(listing.bids.all(), key=lambda bid: bid.value)
        price = top_bid.value

    else:
        top_bid = None
        price = listing.starting_bid

    return price, top_bid


def produce_listing(user, listing):
    price, top_bid = get_top_bid(listing)
    return {
            "listing": listing,
            "price": gbp(price),
            "top_bid": top_bid,
            "watchlisted": (user in listing.watchers.all()),
        }


def get_categories(user):
    # Find all categories
    listings = Listing.objects.all()
    categories = []

    for listing in listings:
        if listing.category != "" and listing.active:
            i = 0
            found = False
            while i < len(categories) and not found:
                if listing.category == categories[i]["name"]:
                    categories[i]["size"] += 1
                    categories[i]["listings"].append(produce_listing(user, listing))
                    found = True

                i += 1

            if not found:
                categories.append({"name": listing.category,
                                   "size": 1,
                                   "listings": [produce_listing(user, listing)]})

    return categories
