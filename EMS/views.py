from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import EventData, Comment, Image, ScheduleImage, SeatingImage
from django.http import JsonResponse
from .forms import RegistrationForm
from .forms import EventDataForm
from .forms import CommentForm, ImageForm, ScheduleImageForm, SeatingImageForm
from datetime import date
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
import os
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import base64
from django.utils import timezone
import requests


# Encoding
def encode_base64(data):
    # Convert data to bytes if it's a string
    data_bytes = data.encode('utf-8')
    encoded = base64.b64encode(data_bytes)
    return encoded.decode('utf-8')  # Convert back to string for readability

# Decoding
def decode_base64(encoded_data):
    # Convert encoded data to bytes
    encoded_bytes = encoded_data.encode('utf-8')
    decoded = base64.b64decode(encoded_bytes)
    return decoded.decode('utf-8')



def send_bulk_email(subject, html_content, recipient_list):
    send_mail(
        subject,
        " ",
        settings.EMAIL_HOST_USER,  # From email
        recipient_list,
        fail_silently=False,
        html_message=html_content,
    )

def download_file(request, filename):

    file_path = (os.path.join(settings.MEDIA_ROOT, filename.replace("$$@$$","/")))
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("File does not exist")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Create the user
            return redirect('login')  # Redirect to login page or another page
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def about(request):
    return render(request, 'events/about.html', {'active_page': 'about'})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def get_location(ip_address):
    response = requests.get(f"https://ipinfo.io/{ip_address}/json?token=28cf12a285f7b3")
    if response.status_code == 200:
        return response.json()  # Returns location data as JSON
    return None


def event_list(request):

    ip_address = get_client_ip(request)
    location_data = get_location(ip_address)
    
    # Assuming we want to pass city and region
    # city = location_data.get('city') if location_data else 'Unknown'
    region = location_data.get('region') if location_data else 'Unknown'

    # print(region)

    # events = Event.objects.filter(user=request.user)
    events = EventData.objects.filter(category="public", place_info__icontains = str(region)).order_by('-pk')[:4]
    events_detail = EventData.objects.filter(category="public", place_info__icontains = str(region))[:4]
    return render(request, 'events/home.html', {'events': events, 'events_detail':events_detail,'active_page': 'home'})


def event_show(request):
    events = EventData.objects.filter(category="public").order_by('-pk')

    paginator = Paginator(events, 3)  # Show 10 items per page

    page_number = request.GET.get('page')  # Get the page number from query parameters
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/event_show.html', {'events': page_obj, 'active_page': 'show'})


@login_required(login_url="login")
def dashboard_view(request):
    userData = User.objects.get(username = request.user)
    events = EventData.objects.filter(user=userData.id).order_by('-pk')
    paginator = Paginator(events, 3)  # Show 10 items per page

    page_number = request.GET.get('page')  # Get the page number from query parameters
    page_obj = paginator.get_page(page_number)

    comments = Comment.objects.filter(user=request.user).order_by('-pk')
    cpaginator = Paginator(comments, 10)  # Show 10 items per page

    cpage_number = request.GET.get('cpage')  # Get the page number from query parameters
    cpage_obj = cpaginator.get_page(cpage_number)

    return render(request, 'events/event_dashboard.html', {'events': page_obj, 'comments':cpage_obj})


@login_required(login_url="login")
def event_create(request):
    image_forms = ImageForm()
    schedule_image_forms = ScheduleImageForm()
    sitting_image_forms = SeatingImageForm()
    if request.method == 'POST':
        form = EventDataForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.created_user = request.user
            event.updated_user = request.user
            event.image = request.FILES.getlist('image')[0]
            event.save()
            
            for image_file in request.FILES.getlist('image'):
                Image.objects.create(event=event, image=image_file)

            for image_file in request.FILES.getlist('sitting_plan'):
                SeatingImage.objects.create(event=event, image=image_file)

            for image_file in request.FILES.getlist('schedule_plan'):
                ScheduleImage.objects.create(event=event, image=image_file)

            subject = "Invitaion of "+event.name
            message = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <style>
        .venue-tickets {
            margin: 0px 15px;
        }

        .venue-tickets .venue-item {
            margin-bottom: 23px;
        }

        .venue-item .thumb img {
            width: 100%;
            overflow: hidden;
        }

        .venue-item .down-content {
            background-color: #07421b;
            position: relative;
            display: inline-block;
            z-index: 1;
            width: 100%;
        }

        .venue-item .down-content .left-content {
            width: 31%;
            float: left;
            background-color: rgba(124, 131, 139, 0.3);
            height: 100%;
            display: inline-block;
            position: absolute;
            z-index: 111;
        }

        .venue-item .down-content .left-content .main-white-button {
            -webkit-transform: rotate(-90deg);
            -moz-transform: rotate(-90deg);
            -o-transform: rotate(-90deg);
            -ms-transform: rotate(-90deg);
            transform: rotate(-90deg);
            position: absolute;
            top: 50%;
            margin-top: -22.5px;
        }

        .venue-item .down-content .right-content {
            /* width: 64%; */
            margin-left: 5%;
        }

        .venue-item .down-content .right-content h4 {
            font-size: 22px;
            color: #fff;
            font-weight: 700;
            margin-top: 30px;
        }

        .venue-item .down-content .right-content p {
            color: #fff;
            margin-top: 20px;
            font-weight: 300;
            padding-right: 30px;
            margin-bottom: 20px;
        }

        .venue-item .down-content .right-content ul li {
            display: inline-block;
            color: #fff;
            font-size: 16px;
            margin-right: 20px;
            ;
        }

        .venue-item .down-content .right-content ul li i {
            margin-right: 5px;
        }

        .venue-item .down-content .right-content .price {
            background-color: rgba(124, 131, 139, 0.3);
            display: inline-block;
            padding: 20px;
            margin-top: 25px;
            margin-bottom: 30px;
        }

        .venue-item .down-content .right-content .price span {
            color: #fff;
            font-size: 14px;
            line-height: 25px;
        }

        .venue-item .down-content .right-content .price span em {
            font-weight: 700;
            font-size: 20px;
            font-style: normal;
        }

        .main-white-button a {
            display: inline-block;
            font-size: 14px;
            padding: 12px 18px;
            background-color: #fff;
            color: #2a2a2a;
            text-align: center;
            font-weight: 500;
            text-transform: capitalize;
            transition: all .3s;
            border-radius: 5px;
            text-decoration: none;
        }

        .main-white-button a:hover {
            opacity: 0.9;
        }

        .main-dark-button a {
            display: inline-block;
            font-size: 14px;
            padding: 12px 18px;
            background-color: #40d621;
            color: #fff;
            text-align: center;
            font-weight: 500;
            text-transform: capitalize;
            transition: all .3s;
        }

        .main-dark-button a:hover {
            opacity: 0.9;
        }

.text-button a {
  font-size: 14px;
  color: #088633;
  transition: all .3s;
}

.text-button i {
  font-size: 12px;
  margin-left: 5px;
  transition: all .5s;
}

.text-button a:hover {
  color: #40d621;
}

.text-button a:hover i {
  margin-left: 8px;
}


    </style>
</head>

<body>

    <!-- *** Venues & Tickets ***-->
    <div class="venue-tickets">
        <div class="container-fluid">
            <div class="row" style="width: 90%;margin: auto;justify-content: center;">
                <div class="col-lg-12">
                    <div class="section-heading">
                    </div>
                </div>
                <div class="col-lg-3">
                    <div class="venue-item" style="border-radius: 9px; overflow: hidden;">
                        <div class="thumb">
                            <img src="https://huppsi.pythonanywhere.com"""+event.image.url+""""
                                alt="">
                        </div>
                        <div class="down-content" style="border-radius: 0 0 9px 9px; overflow: hidden;height: 400px;">
                            <div class="right-content">
                                <h4>"""+event.name[:20]+"""...</h4>
                                <p>"""+event.description[:80]+"""</p>
                                <p>"""+str(event.start_date) +" - "+ str(event.start_time)+"""...</p>
                                <p>"""+ str(event.place_info)+"""...</p>
                                <p> This is the Secret Code for access this private event from our website search box "https://huppsi.pythonanywhere.com" <br>Secret Code : """+ encode_base64(f"{event.user}$$@$${event.id}")+"""</p>
                                <div class="main-white-button" style="margin: 20px 0;position: absolute;bottom: 0;">
                                    <a href="https://huppsi.pythonanywhere.com/event/"""+str(event.id)+"""">Event Details</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>


            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
        crossorigin="anonymous"></script>

</body>

</html>
            """

            html_content = message
            send_bulk_email(subject ,html_content, event.geast_list.split(","))
            return redirect('event_list')

    else:
        form = EventDataForm()
        
    return render(request, 'events/event_form.html', {'form': form,'image_form': image_forms,'sitting_image_forms': sitting_image_forms,'schedule_image_forms': schedule_image_forms, 'active_page': 'create'})

# @login_required(login_url="login")
# def event_update(request, pk):
#     event = get_object_or_404(EventData, pk=pk, user=request.user)
#     if request.method == 'POST':
#         form = EventDataForm(request.POST, request.FILES, instance=event)
#         if form.is_valid():
#             form.save()
#             return redirect('event_list')
#     else:
#         form = EventDataForm(instance=event)
#     return render(request, 'events/event_form.html', {'form': form,'active_page': 'create'})


@login_required(login_url="login")
def event_update(request, pk):
    event = get_object_or_404(EventData, pk=pk, user=request.user)
    image_forms = ImageForm()
    schedule_image_forms = ScheduleImageForm()
    sitting_image_forms = SeatingImageForm()

    existing_images = event.images.all()  # Assuming `images` is a related name for Image model
    existing_schedule_plans = event.sitting_plans.all()
    existing_sitting_plans = event.schedule_plans.all()

    
    if request.method == 'POST':
        form = EventDataForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            updated_event = form.save(commit=False)
            updated_event.updated_user = request.user
            updated_event.save()

            # Update images if new ones are uploaded
            if 'image' in request.FILES:
                existing_images.delete()
                for image_file in request.FILES.getlist('image'):
                    Image.objects.create(event=updated_event, image=image_file)

            if 'sitting_plan' in request.FILES:
                existing_sitting_plans.delete()
                for image_file in request.FILES.getlist('sitting_plan'):
                    SeatingImage.objects.create(event=updated_event, image=image_file)

            if 'schedule_plan' in request.FILES:
                existing_schedule_plans.delete()
                for image_file in request.FILES.getlist('schedule_plan'):
                    ScheduleImage.objects.create(event=updated_event, image=image_file)

            subject = "Invitaion of "+event.name
            message = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <style>
        .venue-tickets {
            margin: 0px 15px;
        }

        .venue-tickets .venue-item {
            margin-bottom: 23px;
        }

        .venue-item .thumb img {
            width: 100%;
            overflow: hidden;
        }

        .venue-item .down-content {
            background-color: #07421b;
            position: relative;
            display: inline-block;
            z-index: 1;
            width: 100%;
        }

        .venue-item .down-content .left-content {
            width: 31%;
            float: left;
            background-color: rgba(124, 131, 139, 0.3);
            height: 100%;
            display: inline-block;
            position: absolute;
            z-index: 111;
        }

        .venue-item .down-content .left-content .main-white-button {
            -webkit-transform: rotate(-90deg);
            -moz-transform: rotate(-90deg);
            -o-transform: rotate(-90deg);
            -ms-transform: rotate(-90deg);
            transform: rotate(-90deg);
            position: absolute;
            top: 50%;
            margin-top: -22.5px;
        }

        .venue-item .down-content .right-content {
            /* width: 64%; */
            margin-left: 5%;
        }

        .venue-item .down-content .right-content h4 {
            font-size: 22px;
            color: #fff;
            font-weight: 700;
            margin-top: 30px;
        }

        .venue-item .down-content .right-content p {
            color: #fff;
            margin-top: 20px;
            font-weight: 300;
            padding-right: 30px;
            margin-bottom: 20px;
        }

        .venue-item .down-content .right-content ul li {
            display: inline-block;
            color: #fff;
            font-size: 16px;
            margin-right: 20px;
            ;
        }

        .venue-item .down-content .right-content ul li i {
            margin-right: 5px;
        }

        .venue-item .down-content .right-content .price {
            background-color: rgba(124, 131, 139, 0.3);
            display: inline-block;
            padding: 20px;
            margin-top: 25px;
            margin-bottom: 30px;
        }

        .venue-item .down-content .right-content .price span {
            color: #fff;
            font-size: 14px;
            line-height: 25px;
        }

        .venue-item .down-content .right-content .price span em {
            font-weight: 700;
            font-size: 20px;
            font-style: normal;
        }

        .main-white-button a {
            display: inline-block;
            font-size: 14px;
            padding: 12px 18px;
            background-color: #fff;
            color: #2a2a2a;
            text-align: center;
            font-weight: 500;
            text-transform: capitalize;
            transition: all .3s;
            border-radius: 5px;
            text-decoration: none;
        }

        .main-white-button a:hover {
            opacity: 0.9;
        }

        .main-dark-button a {
            display: inline-block;
            font-size: 14px;
            padding: 12px 18px;
            background-color: #40d621;
            color: #fff;
            text-align: center;
            font-weight: 500;
            text-transform: capitalize;
            transition: all .3s;
        }

        .main-dark-button a:hover {
            opacity: 0.9;
        }

.text-button a {
  font-size: 14px;
  color: #088633;
  transition: all .3s;
}

.text-button i {
  font-size: 12px;
  margin-left: 5px;
  transition: all .5s;
}

.text-button a:hover {
  color: #40d621;
}

.text-button a:hover i {
  margin-left: 8px;
}


    </style>
</head>

<body>

    <!-- *** Venues & Tickets ***-->
    <div class="venue-tickets">
        <div class="container-fluid">
            <div class="row" style="width: 90%;margin: auto;justify-content: center;">
                <div class="col-lg-12">
                    <div class="section-heading">
                    </div>
                </div>
                <div class="col-lg-3">
                    <div class="venue-item" style="border-radius: 9px; overflow: hidden;">
                        <div class="thumb">
                            <img src="https://huppsi.pythonanywhere.com"""+event.image.url+""""
                                alt="">
                        </div>
                        <div class="down-content" style="border-radius: 0 0 9px 9px; overflow: hidden;height: 400px;">
                            <div class="right-content">
                                <h4>"""+event.name[:20]+"""...</h4>
                                <p>"""+event.description[:80]+"""</p>
                                <p>"""+str(event.start_date) +" - "+ str(event.start_time)+"""...</p>
                                <p>"""+ str(event.place_info)+"""...</p>
                                <p> This is the Secret Code for access this private event from our website search box "https://huppsi.pythonanywhere.com" <br>Secret Code : """+ encode_base64(f"{event.user}$$@$${event.id}")+"""</p>
                                <div class="main-white-button" style="margin: 20px 0;position: absolute;bottom: 0;">
                                    <a href="https://huppsi.pythonanywhere.com/event/"""+str(event.id)+"""">Event Details</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>


            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
        crossorigin="anonymous"></script>

</body>

</html>
            """

            html_content = message
            send_bulk_email(subject ,html_content, event.geast_list.split(","))

            return redirect('event_list')
    else:
        form = EventDataForm(instance=event)

    return render(request, 'events/event_form.html', {
        'form': form,
        'image_forms': image_forms,
        'schedule_image_forms': schedule_image_forms,
        'sitting_image_forms': sitting_image_forms,
        'existing_images': existing_images,
        'existing_sitting_plans': existing_sitting_plans,
        'existing_schedule_plans': existing_schedule_plans,
        'active_page': 'create',
    })


@login_required(login_url="login")
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    text = comment.text
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            comment.text = text
            comment.status = 'approve'
            comment.save()
            return redirect('dashboard')

    return render(request, 'events/event_dashboard.html')

@login_required(login_url="login")
def event_delete(request, pk):
    event = get_object_or_404(EventData, pk=pk, user=request.user)
    userData = User.objects.get(username = request.user)
    events = EventData.objects.filter(user=userData.id)
    if request.method == 'POST':
        event.delete()
        userData = User.objects.get(username = request.user)
        events = EventData.objects.filter(user=userData.id)
        return render(request, 'events/event_dashboard.html', {'events': events,'message':'Delete Successfully', 'status':'success'})
    return render(request, 'events/event_dashboard.html', {'events': events,'status':'success','message': 'Invalid request.'})

@login_required(login_url="login")
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    userData = User.objects.get(username = request.user)
    events = EventData.objects.filter(user=userData.id)
    if request.method == 'POST':
        comment.delete()
        return redirect('dashboard')
    return render(request, 'events/event_dashboard.html', {'events': events,'status':'success','message': 'Invalid request.'})



def event_detail(request, event_id):

    event = get_object_or_404(EventData, id=event_id)
    images = event.images.all()
    sitting_plans = event.sitting_plans.all()
    schedule_plans = event.schedule_plans.all()
    userData = User.objects.get(username = event.user)
    event_related = EventData.objects.filter(user=userData.id)[:3]
    comments = event.comments.filter(status = 'approve')

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.user = event.user  # Assuming the user is logged in
            comment.save()
            messages.success(request, 'Successfully Sent!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = CommentForm()


    if event.category == 'public':
        return render(request, 'events/event_detail.html', {'event': event,'images': images,'sitting_plans': sitting_plans,'schedule_plans': schedule_plans, 'event_related':event_related, 'comments': comments, 'form': form,'active_page': 'home', 'showComment':''})
    else:
        return render(request, 'events/event_detail.html', {'event': event, 'images': images,'sitting_plans': sitting_plans,'schedule_plans': schedule_plans,'event_related':event_related, 'comments': comments, 'form': form,'active_page': 'home', 'showComment':'True'})




def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.like_count += 1
    comment.save()
    return JsonResponse({'like_count': comment.like_count})

def heart_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.heart_count += 1
    comment.save()
    return JsonResponse({'heart_count': comment.heart_count})

def calendar_view(request):
    # events = EventData.objects.all()
    today = timezone.now().date()  # Get today's date
    events = EventData.objects.filter(start_date__gte=today) 
    return render(request, 'events/event_calendar.html', {'events': events,'active_page': 'calendar'})


# def search_event(request):
#     if request.method == 'POST':
#        data = request.POST['search']
#        userData = User.objects.get(username = data)
#        events = EventData.objects.filter(user=userData.id)
#     #    print(events[1].user)
#        context = {
#            'events': events,
#            'active_page': 'show'
#        }
#        return render(request, 'events/event_show.html', context)
#     return render(request, 'events/event_show.html')

def search_event(request):
    if request.method == 'POST':
       data = request.POST['search']
       userData = User.objects.get(username = data)
       events = EventData.objects.filter(user=userData.id).order_by('-pk')
       paginator = Paginator(events, 3)  # Show 10 items per page
       page_number = request.GET.get('page')
       page_obj = paginator.get_page(page_number)

       context = {
           'events': page_obj,
           'active_page': 'show'
       }
       return render(request, 'events/event_show.html', context)
    return render(request, 'events/event_show.html')



    # events = EventData.objects.filter(category="public").order_by('-pk')

    # paginator = Paginator(events, 3)  # Show 10 items per page

    # page_number = request.GET.get('page')  # Get the page number from query parameters
    # page_obj = paginator.get_page(page_number)
    # return render(request, 'events/event_show.html', {'events': page_obj, 'active_page': 'show'})


def search_private_event(request):
    if request.method == 'POST':
       data = request.POST['search']
       data = decode_base64(data).split("$$@$$")
       events = EventData.objects.filter(id = data[1])
       context = {
           'events': events,
           'active_page': 'show'
       }
       return render(request, 'events/event_show.html', context)
    return render(request, 'events/event_show.html')



def search_place(request):
    location = request.GET.get('location', '')
    events = EventData.objects.all()
    
    if location:
        events = events.filter(place_info__icontains=location)

    event_data = [
        {
            'name': event.name[0:10],
            'location': event.place_info,
            'date': event.start_date,
            'id': event.id
        }
        for event in events
    ]
    return JsonResponse(event_data, safe=False)