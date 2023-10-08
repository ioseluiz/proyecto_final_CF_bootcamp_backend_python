from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import EmailInput, TextInput, PasswordInput, CharField

class CustomUserCreationForm(UserCreationForm):
    password1 = CharField(
        label="Password",
        widget=PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'Password'}),
    )
    password2 = CharField(
        label="Confirm password",
        widget=PasswordInput(attrs={'class':'form-control', 'type':'password','placeholder':'Confirmar Password'}),
    )
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "username",
        ]
        #exclude = ['password1','password1',]
        widgets = {
            'email': EmailInput(attrs={
                'class': "form-control",
                'placeholder':"Correo Electronico",
            }),
            'username': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Nombre de Usuario",
                'required': "required",
            }),
            
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username"
        )