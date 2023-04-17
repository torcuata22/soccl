from django import forms
from django.forms import ModelForm
from .models import Venue, Event

#create venue form:
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name','address','zip_code','phone','email')
        labels={
            'name':'',
            'address':'',
            'zip_code':'',
            'phone':'',
            'email':'',
        }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue name'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Zip Code'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'email'}),
        }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name','event_date','venue','manager','attendees','description',)
        labels={
            'name':'',
            'event_date':'YYYY-MM-DD HH:MM:SS',
            'venue':'Venue',
            'manager':'Manager',
            'attendees':'Attendees',
            'description':'',
        }
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event name'}),
            'event_date':forms.TextInput(attrs={'class':'form-control','placeholder':'Date'}),
            'venue':forms.Select(attrs={'class':'form-select','placeholder':'Venue'}),
            'manager':forms.Select(attrs={'class':'form-select','placeholder':'Manager'}),
            'attendees':forms.SelectMultiple(attrs={'class':'form-select','placeholder':'Attendees'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}),
        }