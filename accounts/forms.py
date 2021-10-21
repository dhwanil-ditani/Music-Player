from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import EmailField
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
        field_classes = {'email': EmailField}