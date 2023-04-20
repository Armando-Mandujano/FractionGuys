from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profesor, Grupo
from .models import Estudiante

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

class ProfesorCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(required=True)
    grupo = forms.ModelChoiceField(queryset=Grupo.objects.all())

    class Meta:
        model = Profesor
        fields = ("email", "nombre", "grupo", "password1", "password2")

    def clean_username(self):
        # Replace 'username' with 'nombre' as the field to be used for authentication
        username = self.cleaned_data.get('nombre')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya existe")
        return username

    def save(self, commit=True):
        user = super(ProfesorCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["nombre"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['numero_de_lista', 'grupo']