from django import forms
from .models import CV

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['full_name', 'profession', 'profile_summary', 'experience_details', 'education_details', 'skills_list', 'template']

class UploadCVForm(forms.Form):
    cv_file = forms.FileField()

class AssistantCVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['full_name', 'profession', 'profile_summary', 'skills_list']
        # Assistant only asks for few fields to generate a simple CV first
