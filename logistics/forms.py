from django import forms
from logistics.models import Fleet, Driver


class SignUpForm(forms.Form):
    login = forms.CharField(label='Your login', max_length=50)
    password = forms.CharField(label='Your password', max_length=50)
    is_driver = forms.BooleanField(label='Driver?')
    first_name = forms.CharField(label='Your first_name', max_length=50)
    last_name = forms.CharField(label='Your last_name', max_length=50)
    email = forms.CharField(label='Your email', max_length=50)


class LoginForm(forms.Form):
    login = forms.CharField(label='Your login', max_length=50)
    password = forms.CharField(label='Your password', max_length=50)


class FleetAddForm(forms.ModelForm):
    class Meta:
        model = Fleet
        fields = [
            'name',
            'description'
            # 'owner'
        ]


class FleetInviteDismissForm(forms.Form):
    # drivers_id = forms.ModelMultipleChoiceField(queryset=Driver.objects.all())
    driver_id = forms.CharField(label='Driver id', max_length=50)