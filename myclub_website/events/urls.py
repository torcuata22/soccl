from . import views
from django.urls import path
from .views import home, events

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events', views.events, name='list-events'),

]


#<>/<> are called path converters, you can use: int, str, path(whole urls), slug, UUID (universally unique identifier)
#we can pass <> to the function as variables