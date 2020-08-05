from django.forms import ModelForm
from django import forms
from .models import CouncilMember, Vote


class CMDropdown(forms.Form):

    cmembers = forms.ModelChoiceField(
        queryset=CouncilMember.objects.all().order_by("name"),
        label="Council Member"
    )
