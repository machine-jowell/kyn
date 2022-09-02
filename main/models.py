from django.db import models
from django.contrib.auth.models import User
from PIL import Image



def get_profile_image_filepath(self, filename):
    return f'kyn/profile_images/{self.pk}/{filename}'

def get_default_profile_image():
    return "kyn/default_user_pic.png"

def get_event_image_filepath(self, filename):
    return f'kyn/event_images/{self.name}/{filename}'

def get_default_event_image():
    return "kyn/default_event_pic.png"

# Create your models here.
class UserProfile(models.Model):
    NEIGHBOURHOOD_CHOICES = [
        ('Choa Chu Kang', 'Choa Chu Kang'),
        ('Bukit Gombak', 'Bukit Gombak'),
        ('Bukit Batok', 'Bukit Batok'),
        ('Jurong East', 'Jurong East'),
        ('Clementi', 'Clementi'),
        ('Dover', 'Dover'),
        ('Buona Vista', 'Buona Vista'),
        ('Commonwealth', 'Commonwealth'),
        ('Queenstown', 'Queenstown'),
        ('Redhill', 'Redhill'),
        ('Tiong Bahru', 'Tiong Bahru'),
        ('Outram Park', 'Outram Park'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    contactNo = models.IntegerField()
    address = models.CharField(max_length=200)
    neighbourhood = models.CharField(max_length=100, choices=NEIGHBOURHOOD_CHOICES)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)


    def __str__(self):
        return self.user.username
    
    def save(self):
        super().save()
        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)

class UserEvent(models.Model):

    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('COMMUNITY', 'Community'),
        ('SPORTS', 'Sports & Exercise'),
        ('FESTIVAL', 'Festival'),
        ('OTHER', 'Other')
    ]

    NEIGHBOURHOOD_CHOICES = [
        ('Choa Chu Kang', 'Choa Chu Kang'),
        ('Bukit Gombak', 'Bukit Gombak'),
        ('Bukit Batok', 'Bukit Batok'),
        ('Jurong East', 'Jurong East'),
        ('Clementi', 'Clementi'),
        ('Dover', 'Dover'),
        ('Buona Vista', 'Buona Vista'),
        ('Commonwealth', 'Commonwealth'),
        ('Queenstown', 'Queenstown'),
        ('Redhill', 'Redhill'),
        ('Tiong Bahru', 'Tiong Bahru'),
        ('Outram Park', 'Outram Park'),
    ]

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    neighbourhood = models.CharField(max_length=100, choices=NEIGHBOURHOOD_CHOICES)
    event_image = models.ImageField(max_length=255, upload_to=get_event_image_filepath, null=True, blank=True, default=get_default_event_image)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    attendees = models.ManyToManyField(User, blank=True, related_name='attendees')