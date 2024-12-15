from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from activities.models import Activity
from users.models import Units
from decimal import Decimal
import math
from activities.forms import new_activity_form
from activities import microservice_interface as msi

@login_required
def about_view(request):
    context = {}
    return render(request, 'about.html', context)

@login_required
def training_log_view(response):
    current_user = response.user
    is_metric = Units.objects.get(user=current_user).metric # boolean value for unit
    if response.method == "POST":
        if 'Imperial' in response.POST.keys() and is_metric:
            # change unit to imperial
            unit = Units.objects.get(user=current_user)
            unit.metric = False
            unit.save()
        if 'Metric' in response.POST.keys() and not is_metric:
            # change unit to metric
            unit = Units.objects.get(user=current_user)
            unit.metric = True
            unit.save()
        return redirect("training_log")

    context = {}
    recent_activities_query = Activity.objects.filter(athlete=current_user).order_by('-date', '-time')[:10]
    recent_activities = [x for x in recent_activities_query]

    if is_metric:
        data_to_convert = []
        for activity in recent_activities:
            current_act = {}
            current_act['distance'] = float(activity.distance)
            current_act['elevation'] = activity.elevation
            data_to_convert.append(current_act)
        converted_data = msi.convert(data_to_convert)
        for i in range(len(recent_activities)):
            print(converted_data[i])
            recent_activities[i].distance = Decimal(converted_data[i]['distance']).quantize(Decimal('.01'))
            recent_activities[i].elevation = converted_data[i]['elevation']

    recent_activities_dict = {}
    for activity in recent_activities:
        recent_activities_dict[activity] = {
                                     'distance_string': msi.get_distance_string(activity.distance, is_metric),
                                     'pace_string': get_pace(activity, is_metric),
                                     'duration_string': msi.get_duration_string(activity.duration)
                                     }

    all_activity_query = Activity.objects.filter(athlete=current_user).order_by('date')
    all_activities = [x for x in all_activity_query]
    all_stats = msi.retrieve_stats("ALL", all_activities, is_metric)
    ytd_stats = msi.retrieve_stats("YEAR", all_activities, is_metric)
    avg_stats = msi.average_stats("MONTH", all_activities, is_metric)
    snapshot = msi.snapshot_stats(all_activities, is_metric)
    context["activities"] = recent_activities_dict
    context["ytd_stats"] = ytd_stats
    context["all_stats"] = all_stats
    context["avg_stats"] = avg_stats
    context["snapshot"] = snapshot
    return render(response, 'training_log.html', context)

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
def get_pace(activity, is_metric):
    ''' This method calculates and returns a string containing the average
        pace for an activity.
        :param activity: Object of type Activity
        :return: String representing average pace example: "6:23"
        '''
    unit = 'mi'
    if is_metric:
        unit = 'km'
    raw_pace = activity.duration / float(activity.distance) # sec/mi
    pace = raw_pace/60 # min/mi
    pace_minutes = math.floor(pace)
    pace_seconds = math.floor((pace - pace_minutes)*60)

    if pace_seconds < 10:
        return f"{pace_minutes}:0{pace_seconds}/{unit}"
    return f"{pace_minutes}:{pace_seconds}/{unit}"


