from django import forms
from .models import Students

class studentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = "__all__"
        labels = {
            'grade': 'Room allotted',
        }