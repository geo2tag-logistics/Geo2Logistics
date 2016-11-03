from django import forms
from logistics.models import Fleet, Driver

ROLE_CHOICES = (
    ("1", "OWNER"),
    ("2", "DRIVER")
)

# class SignUpForm(forms.Form):
#     login = forms.CharField(label='Your login', max_length=50)
#     password = forms.CharField(label='Your password', max_length=50)
#     role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
#     first_name = forms.CharField(label='Your first_name', max_length=50)
#     last_name = forms.CharField(label='Your last_name', max_length=50)
#     email = forms.CharField(label='Your email', max_length=50)


class SignUpForm(forms.Form):
    login = forms.CharField(label='Your login', max_length=50)
    email = forms.EmailField(label='Your email', max_length=50)
    password = forms.CharField(label='Your password', max_length=50,
                               widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    first_name = forms.CharField(label='Your first_name', max_length=50)
    last_name = forms.CharField(label='Your last_name', max_length=50)


class LoginForm(forms.Form):
    login = forms.CharField(label='Your login', max_length=50)
    password = forms.CharField(label='Your password', max_length=50)


class FleetAddForm(forms.ModelForm):
    class Meta:
        model = Fleet
        fields = [
            'name',
            'description'
        ]


class FleetInviteDismissForm(forms.Form):
    # drivers_id = forms.ModelMultipleChoiceField(queryset=Driver.objects.all())
    driver_id = forms.CharField(label='Driver id', max_length=50)
