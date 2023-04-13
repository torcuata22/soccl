from django import forms
from django.forms import ModelForm
from .models import Venue

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