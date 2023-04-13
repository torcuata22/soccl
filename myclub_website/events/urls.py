from . import views
from django.urls import path
from .views import home, events

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events', views.events, name='list-events'),
    path('add_venue', views.add_venue, name='add_venue'),
    path('list_venues', views.list_venues, name='list_venues'),

]


#<>/<> are called path converters, you can use: int, str, path(whole urls), slug, UUID (universally unique identifier)
#we can pass <> to the function as variables