from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')  # ForeignKey relationship
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50, blank=True)
    user_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    # additional_info = models.TextField(blank=True)
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True)
    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    contact_details = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Profile of {self.name} ({self.user.username})"

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
        ('Entertainment', 'Entertainment'),
        ('Festivals_and_Fairs', 'Festivals and Fairs'),
        ('Sporting', 'Sporting'),
        ('Cultural', 'Cultural '),
        ('business', 'Business and Corporate'),
        ('Community', 'Community'),
        ('Educational', 'Educational '),
        ('Health_and_Wellness', 'Health and Wellness'),
        ('Political', 'Political'),
        ('other', 'Other'),
    ]
    SAVING_MODE_CHOICES = [
        ('draft', 'Draft'),
        ('publish', 'Publish'),

    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, blank=True, default='public')
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
    sitting_plan_name = models.CharField(max_length=500,blank=True)
    sitting_plan = models.ImageField(upload_to='sitting_plan_files/', blank=True, default='Seating Plan')
    schedule_plan_name = models.CharField(max_length=500,blank=True)
    schedule_plan = models.ImageField(upload_to='schedule_plan_files/', blank=True, default='Schedule Plan')
    hashTags = models.CharField(max_length=100, blank=True)
    saving_mode = models.CharField(max_length=20, choices=SAVING_MODE_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        # Set default name if not provided
        if not self.sitting_plan_name:
            self.sitting_plan_name = "Seating Plan"
        if not self.schedule_plan_name:
            self.schedule_plan_name = "Schedule Plan"
        super().save(*args, **kwargs)

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


class SponsorWithImage(models.Model):
    event = models.ForeignKey(EventData, on_delete=models.CASCADE, related_name='sponsorsWithImage')
    logo = models.ImageField(upload_to='sponsorsWithImage/logos/')

    def __str__(self):
        return f"Sponsor for {self.event}"

class SponsorWithName(models.Model):
    event = models.ForeignKey(EventData, on_delete=models.CASCADE, related_name='sponsorsWithName')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Sponsor for {self.event.name}"
    
class SponsorWithLink(models.Model):
    event = models.ForeignKey(EventData, on_delete=models.CASCADE, related_name='sponsorsWithLink')
    logo = models.ImageField(upload_to='sponsorsWithLink/logos/')
    link = models.URLField()

    def __str__(self):
        return f"Sponsor for {self.event.link}"


class EventDetail(models.Model):
    event = models.ForeignKey(EventData, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Event details for {self.event.name}"


class Guest(models.Model):

    CONFIRM_CHOICES = [
        ('confirm', 'Confirm'),
        ('not_confirm', 'Not Confirm'),

    ]

    event = models.ForeignKey(EventData, on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    confirm = models.CharField( max_length=100 , choices=CONFIRM_CHOICES, blank=True, default='confirm')

    def __str__(self):
        return f"{self.name} - {self.email}"