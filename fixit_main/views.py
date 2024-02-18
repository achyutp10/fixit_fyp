from django.shortcuts import render
from django.http import HttpResponse

from technician.models import Technician

def home(request):
  return render(request, 'home.html')
def services(request):
  return render(request, 'services.html')
def bookTechnician(request):
  # technicians = Technician.objects.filter(is_approved=True)
  technicians = Technician.objects.filter()
  context = {
      'technicians': technicians
    }
  return render(request, 'bookTechnician.html', context)