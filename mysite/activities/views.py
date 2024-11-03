from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from activities.models import Activity
from users.models import *
import math
# from activities.forms import *

@login_required
def about_view(request):
    context = {}
    return render(request, 'about.html', context)

@login_required
def training_log_view(request):
    context = {}
    recent_activities_query = Activity.objects.order_by('date')[:10]
    recent_activities = [x for x in recent_activities_query]
    context["activities"] = recent_activities
    return render(request, 'training_log.html', context)

@login_required
def create_activity_view(request):
    context = {}
    return render(request, 'create_activity.html', context)

@login_required
def edit_activity_view(request):
    context = {}
    return render(request, 'edit_activity.html', context)
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

