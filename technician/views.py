from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from accounts.views import check_role_technician
from technician.models import Technician
from booking.models import Booking
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_technician)
def tprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    technician = get_object_or_404(Technician, user=request.user)

    if request.method == "POST":
       profile_form = UserProfileForm(request.POST, instance=profile)
       if profile_form.is_valid():
          profile_form.save()
          messages.success(request, 'Location Settings updated!')
          return redirect('tprofile')
       else:
          print(profile_form.errors)

    else:
      profile_form = UserProfileForm(instance=profile)
    # Fetching all technician data here to display it in services
      technician = Technician.objects.get(user=request.user)
    
    context = {
        'technician': technician,
        'profile_form': profile_form,
    } 

    return render(request, 'technician/tprofile.html', context)  
  
# def technicianBookingList(request):
#   bookings = Booking.objects.get(user=request.user)
#   context = {
#     'bookings': bookings,
#   }
#   return render(request, 'technician/technicianBookingList.html', context)  

def technicianBookingList(request):
    # Get the current logged-in technician
    technician = Technician.objects.get(user=request.user)
    
    # Query bookings associated with the technician
    bookings = Booking.objects.filter(technician=technician)
    
    # Pagination
    paginator = Paginator(bookings, 2)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'bookings': bookings,
        'page_obj': page_obj,
    }
    return render(request, 'technician/technicianBookingList.html', context)