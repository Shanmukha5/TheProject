from django import forms
from .models import workerdetails

class WorkerDetailsForm(forms.ModelForm):
	
	class Meta:
		model = workerdetails
		fields = ['profilelink', 'name', 'rating', 'skill']

