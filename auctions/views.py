from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse

from .models import User,Product,Comment,Bid


def index(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user=request.user
            product=Product()
            product.title = request.POST["title"]
            product.desc = request.POST["desc"]
            product.price = request.POST["price"]
            product.base_price = request.POST["price"]
            product.photo = request.POST["photo"]
            product.user = user
            product.save()    
        else:
            return render(request, "auctions/login.html")   
    return render(request, "auctions/index.html",{
        "product" : Product.objects.all()
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


def product(request,title):
    product=Product.objects.filter(title=title).first()
    if request.method == "POST":
        if request.user.is_authenticated:
            price=request.POST["bid"]
            user=request.user
            bid=Bid(price=price,product=product,user=user)
            bid.save()
            product=Product.objects.get(title=title)
            product.price=price
            product.save()
        else:
            return render(request, "auctions/login.html")
    bids=product.product_bid.all()
    comments=product.product_comm.all()
    return render(request, "auctions/product.html", {
        "product" : product,
        "bids" : bids,
        "comments" : comments
    })


def items(request):
    if request.user.is_authenticated:
        user=request.user
        products=user.product.all()
        return render(request, "auctions/items.html", {
        "product" : products,
        })
    else:
        return render(request, "auctions/login.html")

def bids(request):
    if request.user.is_authenticated:
        user=request.user
        bids=user.user_bid.all()
        return render(request, "auctions/bids.html", {
        "bids" : bids,
        })
    else:
        return render(request, "auctions/login.html")

def create(request):
    return render(request, "auctions/create.html")