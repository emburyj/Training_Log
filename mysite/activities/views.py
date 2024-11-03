from django.shortcuts import render

def about_view(request):
    context = {}
    return render(request, 'about.html', context)

def training_log_view(request):
    context = {}
    return render(request, 'training_log.html', context)

def create_activity_view(request):
    context = {}
    return render(request, 'create_activity.html', context)

def edit_activity_view(request):
    context = {}
    return render(request, 'edit_activity.html', context)
