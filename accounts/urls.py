from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerTechnician/', views.registerTechnician, name='registerTechnician'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name="myAccount"),
    path('custDashboard/', views.custDashboard, name="custDashboard"),
    path('technicianDashboard/', views.technicianDashboard, name="technicianDashboard"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
