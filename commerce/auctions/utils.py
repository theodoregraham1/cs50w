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