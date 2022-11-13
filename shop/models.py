from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name')
    performer = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to="events", blank=True)

    description = models.TextField(blank=True)


    #featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Events"


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    #type = models.CharField(choices=TYPE_CHOICES, max_length=200, default=TYPE_CONCERTS)

    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name')
    city = models.CharField(max_length=200, null=True)  # lze dodělat jako model
    location = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="tickets", blank=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    ticket_seat_nr = models.IntegerField(default=0)
    #ticket_reserved_nr = models.IntegerField(default=0)
    ticket_stand_nr = models.IntegerField(default=20)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=10, validators=[MaxValueValidator(10), MinValueValidator(1)])
    review = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.review

