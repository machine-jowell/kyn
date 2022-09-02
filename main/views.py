from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import os
from .models import UserProfile, UserEvent
from .filters import EventFilter
from .forms import ExtendedUserCreationForm, UserProfileForm, UserAuthenticationForm, UserEditProfile, UserProfileEditProfile, UserChangePassword, EventCreationForm, EventEditForm


# Create your views here.
def homepage(request):
    context={}
    events = []
    neighbourhoodEvents = []
    if request.user.is_authenticated:
        for event in UserEvent.objects.all():
            events.append(event)
            if event.neighbourhood == request.user.userprofile.neighbourhood:
                neighbourhoodEvents.append(event)
        context["events"] = events
        context["neighbourhoodEvents"] = neighbourhoodEvents

    return render(request, "main/home.html", context)

def aboutus(request):
    return render(request, "main/aboutus.html")

def faq(request):
    return render(request, "main/faq.html")

def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            messages.success("You have been registered successfully")

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, "main/register.html", context)

def login_user(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back "+str(user.username)+"!")
                return redirect('home')
            else:
                messages.error(request, ("There was an error logging you in. Please try again."))
                return redirect('home')
    else:
        form = UserAuthenticationForm()
    
    context= {'form': form}
    return render(request, "main/login.html", context)

# logging out an already signed in user
def logout_user(request):
    logout(request)
    return redirect("home")


@login_required
def view_profile(request):
    return render(request, "main/profile/profile.html")

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditProfile(request.POST, instance=request.user)
        profile_form = UserProfileEditProfile(request.POST, request.FILES, instance=request.user.userprofile)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect('editProfile')
        else:
            messages.error(request, "Something went wrong!")
    else:
        form = UserEditProfile(instance=request.user)
        profile_form = UserProfileEditProfile(instance=request.user.userprofile)
    context= {'form': form, 'profile_form': profile_form}
    return render(request, "main/profile/edit_profile.html", context)

def change_password(request):
    if request.method == 'POST':
        form = UserChangePassword(request.POST, instance=request.user)
        if form.is_valid():
            password = form.cleaned_data["password"]
            request.user.password = make_password(password)
            request.user.save()
            messages.success(request, "Your password was successfully updated!")
            return redirect('changePassword')
        else:
            messages.error(request, "Something went wrong!")
    else:
        form = UserChangePassword()
    return render(request, 'main/profile/password_change.html', {'form': form})


@login_required
def view_profile_events(request):
    context = {}
    created_events = UserEvent.objects.filter(created_by__exact=request.user.id)
    signedUp_events = UserEvent.objects.filter(attendees__exact=request.user.id)
    context["created_events"] = created_events
    context["signedUp_events"] = signedUp_events


    return render(request, "main/profile/manage_profile_events.html", context)

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.neighbourhood = request.user.userprofile.neighbourhood
            obj.save()
            messages.success(request, "You have successfully created a new event!")
            return redirect('createEvent')
        else:
            messages.error(request, "Something went wrong!")
    else:
        form = EventCreationForm()
    
    context = {'form': form}
    return render(request, "main/event/create_event.html", context)

def view_event(request, id):
    event = UserEvent.objects.get(id=id)
    return render(request, "main/event/eventpage.html", {'event': event})


def edit_event(request, id):
    event = UserEvent.objects.get(id=id)
    if request.method == 'POST':
        form = EventEditForm(request.POST, request.FILES, instance=event)

        if form.is_valid():
            form.save()
            messages.success(request, "Your event was successfully updated!")
            return redirect('profileEvents')
        else:
            messages.error(request, "Something went wrong!")
    else:
        form = EventEditForm(instance=event)
    context= {'form': form}
    return render(request, "main/event/edit_event.html", context)

def remove_event(request, id):
    if request.method == 'POST':
        event = UserEvent.objects.get(id=id)
        event.event_image.delete(save=True)
        os.rmdir("./media/kyn/event_images/"+str(event.name))
        event.delete()
        messages.success(request, event.name + "has been successfully removed!")
    return redirect('profileEvents')

def participate_event(request, id):
    event = UserEvent.objects.get(id=id)
    if request.method == 'POST':
        event.attendees.add(request.user)
        messages.success(request, "You have successfully signed up to " + event.name)
    return redirect('/view_event/'+str(event.id))


def remove_participation_event(request, id):
    if request.method == 'POST':
        event = UserEvent.objects.get(id=id)
        event.attendees.remove(request.user)
        messages.success(request, "You have been successfully removed from " + event.name)
    return redirect('profileEvents')


def event_list_view(request):
    context = {}
    events = UserEvent.objects.all()
    context["events"] = events

    events_filter = EventFilter(request.GET, queryset=events)
    context["events_filter"] = events_filter

    has_filter = any(field in request.GET for field in set(events_filter.get_fields()))
    context["has_filter"] = has_filter
    paginator = Paginator(events_filter.qs, 9)
    page_number = request.GET.get('page')

    try:
        response = paginator.page(page_number)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    
    context["response"] = response

    return render(request, "main/event/view_events.html", context)
