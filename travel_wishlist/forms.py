from django import forms
from django.forms import FileInput, DateInput
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')


# 
class DateInput(forms.DateInput):
    input_type = 'date'  #  this is date input class, where you will choose the date 


class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')  # 3 field, if you want more add in here
        widgets = {  #
            'date_visited': DateInput()
        }