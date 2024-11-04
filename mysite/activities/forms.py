from django import forms
from datetime import datetime
from django.core.validators import MinValueValidator
class MyDateInput(forms.widgets.DateInput):
    input_type = 'date'

class new_activity_form(forms.Form):
    sport_choices = ((1, 'Run'),)

    distance = forms.DecimalField(label="Distance (miles)", max_digits=7, decimal_places=2)
    duration_hours = forms.IntegerField(label="Duration (hours)", validators=[MinValueValidator(0)])
    duration_minutes = forms.IntegerField(label="Duration (Minutes)", validators=[MinValueValidator(0)])
    duration_seconds = forms.IntegerField(label="Duration (Seconds)", validators=[MinValueValidator(0)])
    elevation = forms.IntegerField(label="Elevation (feet)", validators=[MinValueValidator(0)])
    date = forms.DateField(widget=MyDateInput(), label="Date", initial=datetime.now, required=True)
    time = forms.TimeField(label="Time", initial=datetime.now, required=True)
    location = forms.CharField(label="Location", max_length=128)
    title = forms.CharField(label="Title", max_length=128, required=True)
    description = forms.CharField(label="Description", max_length=128)
    sport = forms.ChoiceField(choices=sport_choices, label="Sport")
