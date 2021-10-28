from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import EmailField
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {'email': EmailField}