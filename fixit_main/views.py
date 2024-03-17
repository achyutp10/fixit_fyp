from django.shortcuts import render
from django.http import HttpResponse
from rating.models import Rating


def home(request):
  all_ratings = Rating.objects.all()[:2]
    
  context = {
        'all_ratings': all_ratings,
    }
  return render(request, 'home.html', context)

def services(request):
  all_ratings = Rating.objects.all()[:2]
    
  context = {
        'all_ratings': all_ratings,
    }
  return render(request, 'services.html', context)
