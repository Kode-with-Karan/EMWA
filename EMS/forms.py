from django import forms
from .models import Event, EventData, Comment, Image
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'category', 'image', 'ticket_price', 'description']

class ImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Image
        fields = ['image']

class SeatingImageForm(forms.ModelForm):
    sitting_plan = forms.ImageField()

    class Meta:
        model = Image
        fields = ['sitting_plan']

class ScheduleImageForm(forms.ModelForm):
    schedule_plan = forms.ImageField()

    class Meta:
        model = Image
        fields = ['schedule_plan']

class EventDataForm(forms.ModelForm):

    class Meta:
        model = EventData
        fields = ['name', 'category', 'image', 'description', 'link', 'instructions', 'geast_list', 'place_info', 'start_date', 'end_date', 'start_time', 'end_time', 'sitting_plan', 'schedule_plan']
        # fields = ['category', 'name', 'uid', 'description', 'job_category', 'scheduled_status', 'venue', 'start_date', 'end_date', 'location', 'points', 'maximum_attende', 'status']
        widgets = {
            'geast_list': forms.TextInput(attrs={'size': '10',}),
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),  # Using time input type
            'end_time': forms.TimeInput(attrs={'type': 'time'}),    # Using time input type
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', "End date must be after start date.")

    def __init__(self, *args, **kwargs):
        super(EventDataForm, self).__init__(*args, **kwargs)
        
        self.fields['name'].label = ""
        self.fields['description'].label = ""
        self.fields['instructions'].label = ""
        self.fields['geast_list'].label = ""
        # self.fields['venue'].label = ""
        self.fields['place_info'].label = ""
        self.fields['link'].label = ""
        
        
        
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter event name.'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'About The Event You Are Hosting!'
        })
        self.fields['instructions'].widget.attrs.update({
            'placeholder': 'Instructions About The Event You Are Hosting!'
        })
        self.fields['geast_list'].widget.attrs.update({
            'placeholder': 'Geast list For The Event You Are Hosting! Separated By Comma( , )'
        })
        self.fields['place_info'].widget.attrs.update({
            'placeholder': 'Place Instructions For The Event!'
        })
        self.fields['link'].widget.attrs.update({
            'placeholder': 'Enter the ticket link'
        })
        # self.fields['venue'].widget.attrs.update({
        #     'placeholder': 'Enter name of venue.'
        # })




class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text', 'image', 'email', 'status','video']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'id': 'comment_upload_image'}),  # Add id here
            'video': forms.ClearableFileInput(attrs={'id': 'comment_upload_video'}),  # Add id here
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        
        self.fields['name'].label = ""
        self.fields['text'].label = ""
        self.fields['email'].label = ""
        
        
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter the name.'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter the email.'
        })
        self.fields['text'].widget.attrs.update({
            'placeholder': 'Comment!'
        })
