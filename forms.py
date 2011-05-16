from django.contrib import forms
from sher.models import Service
import sher.settings as settings


class AddServiceForm(forms.Form):
    service = forms.ChoiceField(choices=settings.SUPPORTED_SERVICES)

