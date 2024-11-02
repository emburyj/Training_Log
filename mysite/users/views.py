from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You are now able to log in!")
            return redirect('login')

        else:
            pass

        else:
            form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})
