from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError





class Event(models.Model):
    CATEGORY_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True)
    image = models.ImageField(upload_to='event_images/', null=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField( null=True)

    def __str__(self):
        return self.name
    
def validate_pdf(value):
    if not value.name.endswith('.jpg','.png','.webp'):
        raise ValidationError("Only PDF files are allowed.")
    
class EventData(models.Model):
    CATEGORY_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]

    ART_CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('nightlife', 'Nightlife'),
        ('performingVisualArts', 'Performing & Visual Arts'),
        ('holidays', 'Holidays'),
        ('dating', 'Dating'),
        ('hobbies', 'Hobbies'),
        ('business', 'Business'),
        ('foodDrink', 'Food & Drink'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, blank=True)
    art_category = models.CharField(max_length=20, choices=ART_CATEGORY_CHOICES, blank=True, default='other')
    image = models.ImageField(upload_to='event_images/',blank=True)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=500,blank=True)
    instructions = models.TextField(blank=True)
    geast_list = models.TextField(blank=True)
    # venue = models.CharField(max_length=255, null=True)
    place_info = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()   

    created_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_user')
    updated_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='updated_user')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)
    sitting_plan = models.ImageField(upload_to='sitting_plan_files/', blank=True)
    schedule_plan = models.ImageField(upload_to='schedule_plan_files/', blank=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    event = models.ForeignKey(EventData, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_images/')

    def __str__(self):
        return f"Image for {self.event.name}"
    
class SeatingImage(models.Model):
    event = models.ForeignKey(EventData, on_delete=models.CASCADE, related_name='sitting_plans')
    image = models.ImageField(upload_to='sitting_plan_files/')

    def __str__(self):
        return f"SeatingImage for {self.event.name}"
    
class ScheduleImage(models.Model):
    event = models.ForeignKey(EventData, on_delete=models.CASCADE, related_name='schedule_plans')
    image = models.ImageField(upload_to='sitting_plan_files/')

    def __str__(self):
        return f"ScheduleImage for {self.event.name}"

def validate_video_file(value):
    if not value.name.endswith(('.mp4', '.mov', '.avi')):
        raise ValidationError('Unsupported file format. Please upload a video file with one of the following extensions: .mp4, .mov, .avi, .mkv.') 

class Comment(models.Model):
    event = models.ForeignKey(EventData, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    video = models.FileField(upload_to='comment_videos/', validators=[validate_video_file], null=True, blank=True)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    status_choice = (
        ('approve', 'Approve'),
        ('deny', 'Deny'),
    )
    status = models.CharField(choices=status_choice, max_length=10,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    heart_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Comment on {self.user.username}'s {self.event.name}"

