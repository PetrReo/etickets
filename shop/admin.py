from django.contrib import admin

# Register your models here.
from .models import Event, Ticket, Review

admin.site.register(Ticket)
admin.site.register(Event)
admin.site.register(Review)