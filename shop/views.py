from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.forms import ReviewForm, SignupForm, SigninForm
from shop.models import Ticket, Event
from shop.serializer import TicketSerializer


def home(request):
    # if request.META['HTTP_HOST'] != "ecommerce.hem.xyz.np":
    #     return redirect("http://ecommerce.hem.xyz.np")
    tickets = Ticket.objects.filter(active=True)
    events = Event.objects.filter(active=True)
    context = {"tickets": tickets, "events": events}
    return render(request, "shop/home.html", context)


def search(request):
    q = request.GET["q"]
    tickets = Ticket.objects.filter(active=True, name__icontains=q)
    events = Event.objects.filter(active=True)
    context = {"tickets": tickets,
               "events": events,
               "title": q + " - search"}
    return render(request, "shop/list.html", context)


def events(request, slug):
    cat = Event.objects.get(slug=slug)
    tickets = Ticket.objects.filter(active=True, event=cat)
    events = Event.objects.filter(active=True)
    context = {"tickets":tickets, "events":events, "title":cat.name + " - Events"}
    return render(request, "shop/list.html", context)


def detail(request, slug):
    ticket = Ticket.objects.get(active=True, slug=slug)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, "Review saved")
        else:
            messages.error(request, "Invalid form")
    else:
        form = ReviewForm()


    events = Event.objects.filter(active=True)
    context = {"ticket" : ticket,
               "events":events,
               "form": form}
    return render(request, "shop/detail.html", context)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, "User saved")
            return redirect("shop:signin")
        else:
            messages.error(request, "Error in form")
    else:
        form = SignupForm()
    context = {"form": form}
    return render(request, "shop/signup.html", context)


def signin(request):
    if request.method=="POST":
        form = SigninForm(request.POST)
        # username = req.POST["username"]
        # password = req.POST["password"]
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username,  password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("shop:home")
        else:
            messages.error(request, "Invalid Username or Password")
    else:
        form = SigninForm()
    context = {"form": form}
    return render(request, "shop/signin.html", context)


def signout(request):
    logout(request)
    return redirect("shop:signin")


def cart(request, slug):
    """
        data = {"items" : ["slug1", "slug2"],
                "price" : 12342,
                "count" : 5
                }
        request.session["data"] = data
        """
    ticket = Ticket.objects.get(slug=slug)
    inital = {"items":[],"price":0.0,"count":0}
    session = request.session.get("data", inital)
    if slug in session["items"]:
        messages.error(request, "Already added to cart")
    else:
        session["items"].append(slug)
        session["price"] += float(ticket.price)
        session["count"] += 1
        request.session["data"] = session
        messages.success(request, "Added successfully")
    return redirect("shop:detail", slug)


def mycart(request):
    sess = request.session.get("data", {"items":[]})
    tickets = Ticket.objects.filter(active=True, slug__in=sess["items"])
    events = Event.objects.filter(active=True)
    context = {"tickets": tickets,
               "events": events,
               "title": "My Cart"}
    return render(request, "shop/list.html", context)


def checkout(request):
    request.session.pop('data', None)
    return redirect("/")

@api_view(['GET'])
def api_tickets(request):
    query = request.GET.get("q", "")
    tickets = Ticket.objects.filter(Q(name__contains=query) | Q(description__contains=query))
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

