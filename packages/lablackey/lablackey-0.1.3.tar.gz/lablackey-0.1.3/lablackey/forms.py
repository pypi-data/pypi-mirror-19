from django.contrib.auth import get_user_model
from django import forms

class UserEmailForm(forms.ModelForm):
  class Meta:
    fields = ('email',)
    model = get_user_model()
