from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from activities.models import Activity
from users.models import *
import math
from activities.forms import new_activity_form

@login_required
def about_view(request):
    context = {}
    return render(request, 'about.html', context)

@login_required
def training_log_view(request):
    context = {}
    recent_activities_query = Activity.objects.order_by('date')[:10]
    recent_activities = [x for x in recent_activities_query]
    recent_activities_dict = {}
    for activity in recent_activities:
        recent_activities_dict[activity] = {
                                     'pace_string': get_pace(activity),
                                     'duration_string': get_duration_string(activity)
                                     }
    context["activities"] = recent_activities_dict
    return render(request, 'training_log.html', context)

@login_required
def create_activity_view(response):
    current_user = response.user
    if response.method == "POST":
        new_activity = new_activity_form(response.POST)
        if new_activity.is_valid():
            # hours = new_activity.cleaned_data["duration_hours"]
            # minutes = new_activity.cleaned_data["duration_minutes"]
            # seconds = new_activity.cleaned_data["duration_seconds"]
            # activity_duration = 3600*int(hours) + 60*int(minutes) + int(seconds)
            # duration = activity_duration
            duration = new_activity.cleaned_data["duration"]
            distance = new_activity.cleaned_data["distance"]
            elevation = new_activity.cleaned_data["elevation"]
            date = new_activity.cleaned_data["date"]
            time = new_activity.cleaned_data["time"]
            location = new_activity.cleaned_data["location"]
            title = new_activity.cleaned_data["title"]
            description = new_activity.cleaned_data["description"]
            # sport = new_activity.cleaned_data["sport"]
            save_activity = Activity(athlete=current_user, location=location, date=date, time=time, title=title, description=description, duration=duration, distance=distance, elevation=elevation)
            save_activity.save()
            messages.success(response, "Your activity has been created!")
            return redirect("training_log")
        else:
            return redirect("create_activity")
    context = {'activity_form': new_activity_form}
    return render(response, 'create_activity.html', context)

@login_required
def edit_activity_view(request, aid):
    edit_activity = Activity.objects.get(aid=aid)
    if request.method == "POST":
        if 'activityDelete' in request.POST.keys():
            edit_activity.delete()
            messages.success(request, "Your activity has been deleted!")
            return redirect('training_log')

        form = new_activity_form(request.POST, instance=edit_activity)
        if form.is_valid():
            # raw_hours = (edit_activity.duration/3600)
            # hours = math.floor(raw_hours)
            # raw_minutes = 60*(raw_hours - hours)
            # minutes = math.floor(raw_minutes)
            # seconds = math.floor(60*(raw_minutes - minutes))
            edit_activity.save()
            messages.success(request, "Your activity has been changed!")
            return redirect('training_log')
    else:
        form = new_activity_form(instance=edit_activity)
        return render(request, 'edit_activity.html', {'form': form})
'''
Helper functions
'''
def get_pace(activity):
    ''' This method calculates and returns a string containing the average
        pace for an activity.
        :param activity: Object of type Activity
        :return: String representing average pace example: "6:23"
        '''
    raw_pace = activity.duration / activity.distance # sec/mi
    pace = raw_pace/60 # min/mi
    pace_minutes = math.floor(pace)
    pace_seconds = math.floor((pace - pace_minutes)*60)
    if pace_seconds < 10:
        return f"{pace_minutes}:0{pace_seconds}"
    return f"{pace_minutes}:{pace_seconds}"

def get_duration_string(activity):
    ''' This method calculates and returns a string containing the hours and
        minutes for an activity duration.
        :param activity: Object of type Activity
        :return: String representing the activity duration example: "1hr 32min"
        '''
    duration_hours = math.floor(activity.duration / 3600)
    duration_minutes = math.floor(60*((activity.duration/3600) - duration_hours))
    if duration_hours > 0:
        return f"{duration_hours}h {duration_minutes}m"
    return f"{duration_minutes}m"

