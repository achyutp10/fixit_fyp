from django.urls import path, include
from .import views


urlpatterns = [
    path('profile/',views.tprofile, name='tprofile'),
    path('technicianBookingList/',views.technicianBookingList, name='technicianBookingList'),


]
