from django.shortcuts import render, redirect
#To create calendar:
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User #import User model to create query
from .forms import VenueForm, EventFormAdmin, UserEventForm
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

#For pagination:
from django.core.paginator import Paginator

#Messages:
from django.contrib import messages



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
    #Query Events Model for dates:
    event_list = Event.objects.filter(
    event_date__year=year,
    event_date__month=month_number
)

    #get current time:
    time = now.strftime('%I:%M %p')   
    return render(request, 'events/home.html', {'name':name, 
                                                'year':year, 
                                                'month':month,
                                                'month_number':month_number,
                                                'cal':cal,
                                                'current_year': current_year,
                                                'time':time,
                                                'event_list':event_list,})



def events(request):
    event_list = Event.objects.all().order_by('-event_date')
    return render(request, 'events/event_list.html', {'event_list':event_list})


def add_venue(request):
    submitted=False
    if request.method == "POST":
        form=VenueForm(request.POST, request.FILES) 
        if form.is_valid():
            venue=form.save(commit=False) #don't save yet because we want to attach the id to the request
            venue.owner = request.user.id #user.id is the loggedin user
            venue.save() #save the venue object
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form=VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted})


def list_venues(request):
    venue_list = Venue.objects.all().order_by('name') #to randomize: '?'
    #set up pagination:
    p = Paginator(Venue.objects.all(),2
                  )
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" *venues.paginator.num_pages #create list with as many utems as pages (this is an iterable, unlike "i" which is an integer)
    return render(request, 'events/venues.html', {'venue_list':venue_list, 'venues':venues, 'nums':nums,})


def show_venue(request, venue_id):
    venue=Venue.objects.get(pk=venue_id)
    #query Venue to access name of the venue owner's username
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {'venue':venue, 'venue_owner':venue_owner})

def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)  #returned search results
        return render(request, 'events/search_venues.html', {'searched':searched, 'venues':venues})
    else:
        return render(request, 'events/search_venues.html', {})
    
def update_venue(request, venue_id):
    venue=Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue) #fills out the form with original data for us to edit
    if form.is_valid():
        form.save()
        return redirect('list_venues')

    return render(request, 'events/update_venue.html', {'venue':venue, 'form':form})

def add_event(request):
    submitted=False
    if request.method == "POST":
        if request.user.is_superuser:
            form=EventFormAdmin(request.POST) #goes to form for super user
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form=UserEventForm(request.POST) #goes to form for regular users
            if form.is_valid():
                #to associate user id with the event:
                event = form.save(commit=False)
                event.manager = request.user
                event.save()                
                return HttpResponseRedirect('/add_event?submitted=True')
            
    #This one goes to the form to be filled (empty)    
    else:
        if request.user.is_superuser:
            form=EventFormAdmin
        else:
            form=UserEventForm    
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})
    

def update_event(request, event_id):
    event=Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = UserEventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request, 'events/update_event.html', {'event':event, 'form':form})


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    #Check if the person who is logged in is the event manager, so they are authorized to delete
    if request.user == event.manager:
        event.delete()
        messages. success(request, "Event has been deleted")
        return redirect('list-events')
    else:
        messages. success(request, "You are not authorized to delete this event")
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
        


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me) #filter(model field = value)
        return render(request, 
                      'events/my_events.html', 
                      {'me':me, 'events':events})
    else:
        messages.success(request, "You aren't authorized to see this pate")
        return redirect('home')

def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains=searched)  #returned search results
        return render(request, 'events/search_events.html', {'searched':searched, 'events':events})
    else:
        return render(request, 'events/search_events.html', {}) 

#Admin approval page    
def admin_approval(request):
    #get venues:
    venue_list = Venue.objects.all()
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()


    event_list = Event.objects.all().order_by('-event_date') #list all events in specific order
    if request.user.is_superuser:
        if request.method == 'POST':
            #create list of checked box ids:
            id_list = request.POST.getlist('boxes')
           
           #uncheck all boxes (clean slate)
            event_list.update(approved=False)
            #tell database to update the ids to approve them:
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request,('Event approval has been updated') )        
            return redirect('list-events')
            
        else:
            return render(request, 'events/admin_approval.html', {'event_list':event_list, 
                                                                  'event_count':event_count,
                                                                  'venue_count':venue_count,
                                                                  'user_count':user_count, 
                                                                  'venue_list':venue_list,})

    else:
        messages.success(request,('You shall not pass!') )
        return redirect('home')
    
    return render(request, 'events/admin_approval.html')

#Show an event:
def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, "events/show_event.html", {'event':event,})



#Show events in a venue:
def venue_events(request, venue_id):
    #Grab venue:
    venue = Venue.objects.get(id = venue_id)
    #Grab events in that venue:
    events = venue.event_set.all()
    if events:
        return render(request, "events/venue_events.html", {'events':events,})
    else: 
        messages.success(request, ('that venue has no events at this time'))
        return redirect('admin_approval')


#CONTINUE HERE: https://www.youtube.com/watch?v=hyzM1lpc6Rs&list=PLCC34OHNcOtqW9BJmgQPPzUpJ8hl49AGy&index=45