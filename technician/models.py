from django.db import models
from accounts.models import User, UserProfile

# Create your models here.
from django.utils.deconstruct import deconstructible

@deconstructible
class TechnicianImagePath:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # Generate the path and filename
        return f'technician/{self.sub_path}/{instance.user.username}/{filename}'
class Technician(models.Model):
  CHOICES = (
           ("PLUMBER", "Plumber"),
           ("ELECTRICIAN", "Electrician"),
           ("PANITER", "Painter"),
           ("CARPENTER", "Carpenter"),
           ("PEST", "Pest"),
            )
  user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
  user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
  technician_license = models.ImageField(upload_to=TechnicianImagePath('license'), blank=True, null=True)
  technician_description = models.TextField(blank=True, null=True)
  service_type = models.CharField(max_length=25, choices=CHOICES, default='PLUMBER')
  service_description = models.TextField(blank=True, null=True)
  service_charge = models.IntegerField()
  service_image = models.ImageField(upload_to=TechnicianImagePath('serviceImages'), blank=True, null=True)
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.username