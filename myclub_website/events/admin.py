from django.contrib import admin
from .models import Event, Venue, MyClubUser
#Group is part of the auth system, so we need to import it:
from django.contrib.auth.models import Group

#admin.site.register(Event)
#admin.site.register(Venue)
admin.site.register(MyClubUser)

#TO REMOVE GROUPS:
admin.site.unregister(Group)

#Admin panel customization:
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address','phone')
    ordering = ('name',) #need a comma b/c it's a tuple if I want descending, att a -
    #search bar:
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields=(('name','venue'), 'event_date', 'description', 'manager', 'attendees', 'approved')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)

