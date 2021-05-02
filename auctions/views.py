from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    active_listing = list(Listing.objects.filter(status=True))
    return render(request, "auctions/index.html",{
        "active_listing": active_listing
    })

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

@login_required(login_url='../login')
def new_listing(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        title = request.POST["title"]
        description = request.POST["description"]
        start_bid = float(request.POST["start_bid"])
        category = request.POST["category"]
        image = request.POST["image_url"]
        seller = User.objects.get(pk=user_id)
        try:
            listing = Listing(title=title, description=description,start_bid=start_bid, image=image, category=category, seller=seller)
            listing.save()
        except:
            return render(request, "auctions/new_listing.html",{
                "message": "Please fill all required field correctly"
            })
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/new_listing.html")
    
def listing_page(request, listing_id):
    message= ""
    listing = Listing.objects.get(pk=listing_id)
    current_bid = listing.bids.last()
    if request.method == "POST": #someone placed a bid, a comment, or wants to close the auction
        action = request.POST['action']
        user_id = request.POST['user_id']
        user = User.objects.get(pk=user_id)
        if action == 'bid': 
            value = float(request.POST['bid_value'])
            if ((current_bid and value <= current_bid.value) or value < listing.start_bid): #checks if bid is valid
                message = "Bid not valid. Value should be greater than current bid (if any) or equal/greater than starting bid."
            else: 
                try:
                    new_bid = Bid(value = value, bidder=user,product=listing)
                    new_bid.save()
                    return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
                except:
                    message="Could not post your bid."
        elif action == 'comment':
            content = request.POST['content']
            try:
                comment = Comment(content=content, page=listing, author=user)
                comment.save()
                return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
            except:
                message="Your comment could not be posted."
        elif action == 'close':
            listing.status = False #status False closes the auction
            try:
                listing.save() 
                return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))
            except:
                message="Could not close the auction."
        else:
            return HttpResponseRedirect(reverse("index"))    
    comments = listing.comments.all()
    return render(request, "auctions/listing_page.html",{
        "listing":listing,
        "comments": comments,
        "current_bid": current_bid,
        "message": message
    })