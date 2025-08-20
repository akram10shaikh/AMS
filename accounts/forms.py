# forms.py
from accounts.models import Staff, Organization
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class OrganizationRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Organization
        fields = ['name', 'phone_number', 'address','role']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            role=self.cleaned_data['role'],
        )
        organization = super().save(commit=False)
        organization.user = user
        if commit:
            organization.save()
        return organization

class OrganizationLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")



class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'phone_number', 'address']

User = get_user_model()  # This replaces the direct import of User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password','role']

from django import forms
from .models import Staff, Organization

class StaffForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Organization"
    )

    role = forms.ChoiceField(
        choices=Staff.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Role"
    )

    class Meta:
        model = Staff
        fields = ['name', 'email', 'organization', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'age', 'mobile_number', 'email', 'address',
                  'player_management', 'injury_tracking', 'add_form',
                  'add_result', 'view_result', 'create_camps_tournaments',
                  'view_camps_tournaments', 'create_program', 'assign_program',
                  'view_programs', 'organization', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'player_management': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'injury_tracking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'add_form': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'add_result': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'view_result': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'create_camps_tournaments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'view_camps_tournaments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'create_program': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assign_program': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'view_programs': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(StaffRegistrationForm, self).__init__(*args, **kwargs)
        # Dynamically filter organizations if needed (e.g., based on logged-in user's org)
        # self.fields['organization'].queryset = Organization.objects.filter(user=self.user)


# NEw

class StaffRegistrationFormOrg(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'age', 'mobile_number', 'email', 'address',
                  'player_management', 'injury_tracking', 'add_form',
                  'add_result', 'view_result', 'create_camps_tournaments',
                  'view_camps_tournaments', 'create_program', 'assign_program',
                  'view_programs', 'staff_role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'player_management': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'injury_tracking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'add_form': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'add_result': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'view_result': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'create_camps_tournaments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'view_camps_tournaments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'create_program': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assign_program': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'view_programs': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'staff_role': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(StaffRegistrationFormOrg, self).__init__(*args, **kwargs)
        # Dynamically filter organizations if needed (e.g., based on logged-in user's org)
        # self.fields['organization'].queryset = Organization.objects.filter(user=self.user)


ROLE_CHOICES = [
        ('OrganizationAdmin', 'Organization Admin'),
        ('Staff', 'Staff'),
    ]
class UserFormOrg(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=False  # required only if user_role == 'Staff'
    )
    class Meta:
        model = User
        fields = ['username', 'password','role']