from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt
from users.models import Units

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You are now able to log in!")
            username = form.cleaned_data.get('username')
            new_user = User.objects.get(username=username)
            user_units = Units(user=new_user, metric=False)
            user_units.save()
            return redirect('login')

        else:
            pass

    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})
