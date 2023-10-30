def gbp(i):
    return f"£{i:.2f}"


def get_top_bid(listing):
    if list(listing.bids.all()) != []: 
        top_bid = max(listing.bids.all(), key=lambda bid: bid.value)
        price = top_bid.value

    else:
        top_bid = None
        price = listing.starting_bid

    return price, top_bid


def produce_listing(user, l):
    price, top_bid = get_top_bid(l)
    return {
            "listing": l,
            "price": gbp(price),
            "top_bid": top_bid,
            "watchlisted": (user in l.watchers.all()),
        }