from django.shortcuts import render, redirect
#To create calendar:
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponseRedirect #makes form redirect back to itself
#to generate text files on the fly:
from django.http import HttpResponse
#to generate csv files
import csv
#imports needed to generate pdf files:
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



# Create your views here.
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name='Marilyn'
    month = month.capitalize()
    #convert month fom name to number:
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    #create calendar:
    cal = HTMLCalendar().formatmonth(year, month_number)
    #get current year:
    now=datetime.now()
    current_year = now.year 
    #get current time:
    time = now.strftime('%I:%M %p')   
    return render(request, 'events/home.html', {'name':name, 
                                                'year':year, 
                                                'month':month,
                                                'month_number':month_number,
                                                'cal':cal,
                                                'current_year': current_year,
                                                'time':time,})



def events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html', {'event_list':event_list})


def add_venue(request):
    submitted=False
    if request.method == "POST":
        form=VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form=VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted})


def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')
    return render(request, 'events/venues.html', {'venue_list':venue_list})

def show_venue(request, venue_id):
    venue=Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html', {'venue':venue})

def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)  #returned search results
        return render(request, 'events/search_venues.html', {'searched':searched, 'venues':venues})
    else:
        return render(request, 'events/search_venues.html', {})
    
def update_venue(request, venue_id):
    venue=Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')

    return render(request, 'events/update_venue.html', {'venue':venue, 'form':form})

def add_event(request):
    submitted=False
    if request.method == "POST":
        form=EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form=EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})
    

def update_event(request, event_id):
    event=Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request, 'events/update_event.html', {'event':event, 'form':form})


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venues')


#GENERATE TEXT FILE:
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    #Designate the model:
    venues = Venue.objects.all()
    lines=[]
    #Loop through and uotput:
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.phone}\n{venue.email}\n\n\n\n')
    response.writelines(lines)
    return response
    

#GENERATE CSV FILE:
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    #create csv writer:
    writer=csv.writer(response)
    #Designate the model:
    venues = Venue.objects.all()
   #Add column headings to csv file:
    writer.writerow(['Venue Name','Address','Zip Code','Phone','Web Address','Email'])
    #Loop through and append to spreadsheet:
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.web, venue.email])
    return response

#GENERATE PDF FILE:
#need to pip install reportlab (also installs pillow)
def venue_pdf(request):
    #Create Bytestram buffer:
    buf = io.BytesIO()
    #Create Canvas:
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #Create text object:
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    #To Add lines of text:
    # lines=[
    #     "this is line 1",
    #     "this is line 2",
    #     "this is line 3",
    # ]
    # for line in lines:
    #     textob.textLine(line)
    venues = Venue.objects.all()
    lines=[]
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email)
        lines.append('')
        
    for line in lines:
         textob.textLine(line)
    #finish:
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venues.pdf')
        


