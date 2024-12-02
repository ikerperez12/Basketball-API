from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder

#módulo de formularios para una aplicación web en Django

#forms, AuthenticationForm y UserCreationForm  módulos  Django formularios y autenticación de usuarios.
#FormHelper, Submit, Layout y ButtonHolder son módulos de la librería crispy_forms, que se utiliza para dar un aspecto agradable y moderno a los formularios de Django.


#Formulario de registro de usuarios
class SignupForm(forms.Form, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-registerForm'
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_action = 'signup_view'
        self.helper.add_input(Submit('registrar', 'Registrar'))


#Formulario de inicio de sesióN

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )




class Conference(forms.Form):
    name=forms.CharField(label="Conference Name" ,max_length=100)