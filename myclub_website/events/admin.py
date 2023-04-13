from django.contrib import admin
from .models import Event, Venue, MyClubUser

#admin.site.register(Event)
#admin.site.register(Venue)
admin.site.register(MyClubUser)

#Admin panel customization:
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address','phone')
    ordering = ('name',) #need a comma b/c it's a tuple if I want descending, att a -
    #search bar:
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields=(('name','venue'), 'event_date', 'description', 'manager', 'attendees')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)

