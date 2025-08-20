from django import forms
from player_app.models import *  # Import your custom User model


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'name', 'image', 'email', 'primary_contact_number', 'secondary_contact_number',
            'date_of_birth', 'pincode', 'address', 'nationality', 'gender', 'state', 'district',
            'role', 'batting_style', 'bowling_style', 'handedness', 'aadhar_number', 'sports_role',
            'id_card_number', 'weight', 'height', 'age_category', 'team', 'position',
            'aadhar_card_upload', 'pan_card_upload', 'marksheets_upload', 'guardian_name', 'relation',
            'guardian_mobile_number', 'disease', 'allergies', 'additional_information', 'players_in_groups','organization','password'

        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'primary_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'batting_style': forms.TextInput(attrs={'class': 'form-control'}),
            'bowling_style': forms.TextInput(attrs={'class': 'form-control'}),
            'handedness': forms.Select(attrs={'class': 'form-control'}),
            'aadhar_number': forms.TextInput(attrs={'class': 'form-control'}),
            'sports_role': forms.TextInput(attrs={'class': 'form-control'}),
            'id_card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'age_category': forms.Select(attrs={'class': 'form-control'}),
            'team': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'aadhar_card_upload': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'pan_card_upload': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'marksheets_upload': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'relation': forms.Select(attrs={'class': 'form-control'}),
            'guardian_mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'disease': forms.TextInput(attrs={'class': 'form-control'}),
            'allergies': forms.TextInput(attrs={'class': 'form-control'}),
            'additional_information': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            'players_in_groups': forms.CheckboxSelectMultiple(),

            'password': forms.PasswordInput(),


            'organization': forms.Select(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['image'].required = True
        self.fields['email'].required = True
        self.fields['primary_contact_number'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['pincode'].required = True
        self.fields['address'].required = False
        self.fields['nationality'].required = False
        self.fields['gender'].required = False
        self.fields['state'].required = False
        self.fields['district'].required = False
        self.fields['role'].required = False
        self.fields['batting_style'].required = False
        self.fields['bowling_style'].required = False
        self.fields['handedness'].required = False
        self.fields['aadhar_number'].required = True
        self.fields['sports_role'].required = False
        self.fields['id_card_number'].required = False
        self.fields['weight'].required = False
        self.fields['height'].required = False
        self.fields['age_category'].required = False
        self.fields['team'].required = False
        self.fields['position'].required = False
        self.fields['aadhar_card_upload'].required = True
        self.fields['pan_card_upload'].required = False
        self.fields['marksheets_upload'].required = False
        self.fields['guardian_name'].required = False
        self.fields['relation'].required = False
        self.fields['guardian_mobile_number'].required = False
        self.fields['disease'].required = False
        self.fields['allergies'].required = False
        self.fields['additional_information'].required = False
        self.fields['password'].required = False


    def clean_primary_contact_number(self):
        data = self.cleaned_data.get('primary_contact_number')
        if data and not data.isdigit():
            raise forms.ValidationError("Primary contact number must contain only digits.")
        return data

    def clean_secondary_contact_number(self):
        data = self.cleaned_data.get('secondary_contact_number')
        if data and not data.isdigit():
            raise forms.ValidationError("Secondary contact number must contain only digits.")
        return data

    def clean_aadhar_number(self):
        data = self.cleaned_data.get('aadhar_number')
        if data and (not data.isdigit() or len(data) != 12):
            raise forms.ValidationError("Aadhar number must be 12 digits.")
        return data

    def clean_pincode(self):
        data = self.cleaned_data.get('pincode')
        if data and (not data.isdigit() or len(data) != 6):
            raise forms.ValidationError("Pincode must be 6 digits, Pincode must be numbers")
        return data

    def clean_state(self):
        data = self.cleaned_data.get('state')
        valid_states = [state[0] for state in Player.STATES]
        if data not in valid_states:
            raise forms.ValidationError("Invalid state selected.")
        return data

    def clean_district(self):
        data = self.cleaned_data.get('district')
        if data and (not data.isalpha() or len(data) < 3):
            raise forms.ValidationError("District must contain only letters and be at least 3 characters long.")
        return data


class GroupForm(forms.ModelForm):
    class Meta:
        model = Player_Group
        fields = ['name']

class UploadFileForm(forms.Form):
    file = forms.FileField()

class InjuryForm(forms.ModelForm):
    class Meta:
        model = Injury
        fields = ['player', 'injury_type', 'affected_body_part', 'severity', 'injury_date', 'status', 'notes']
        widgets = {
            'injury_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MultipleMedicalDocumentsForm(forms.Form):
    documents = forms.FileField(required=True)


class TreatmentRecommendationForm(forms.ModelForm):
    class Meta:
        model = TreatmentRecommendation
        fields = ['player', 'treatment', 'recommendation_notes', 'recovery_time_weeks']  # Include 'treatment' and 'recovery_time_weeks'

    player = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        required=True,
        label="Player",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    treatment = forms.CharField(
        max_length=255,
        required=True,
        label="Treatment",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    recommendation_notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True,
        label="Recommendation Notes"
    )
    
    recovery_time_weeks = forms.IntegerField(
        required=True,
        label="Recovery Time (Weeks)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

# Ak Forms

class OrganizationPlayerForm(forms.ModelForm):
   
    class Meta:
        model = Player
        fields = [
            'name', 'image', 'email', 'date_of_birth',
            'primary_contact_number', 'secondary_contact_number', 'gender','state',
            'role', 'batting_style', 'bowling_style', 'handedness', 'age_category', 
            'guardian_name', 'relation', 'guardian_mobile_number',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class OrganizationPlayerFormUpdate(forms.ModelForm):
    new_password = forms.CharField(
        label="Set New Password", required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    class Meta:
        model = Player
        fields = [
            'name', 'image', 'email', 'date_of_birth',
            'primary_contact_number', 'secondary_contact_number', 'gender','state',
            'role', 'batting_style', 'bowling_style', 'handedness', 'age_category',
            'guardian_name', 'relation', 'guardian_mobile_number',
        ]
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'})}

# Injury Form

class InjuryForm(forms.ModelForm):
    injury_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Injury Date'})
    )
    expected_date_of_return = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Expected Date of Return'})
    )

    class Meta:
        model = Injury
        fields = [
            'player', 'reported_by', 'name', 'injury_date',
            'venue', 'team', 'type_of_activity', 'injury_type',
            'cause_of_injury', 'nature_of_injury', 'expected_date_of_return',
            'notes', 'affected_body_part', 'body_segment', 'severity', 
        ]
        widgets = {
            'player': forms.Select(attrs={'class': 'form-control'}),
            'reported_by': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Reported by'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team'}),
            'type_of_activity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type of activity at time of injury'}),
            'injury_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type of injury'}),
            'cause_of_injury': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cause of injury'}),
            'nature_of_injury': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nature of injury'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows':2}),
            'affected_body_part': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Body region injured'}),
            'body_segment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Body segment'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        players_qs = kwargs.pop('players_qs', None)
        physios_qs = kwargs.pop('physios_qs', None)
        super().__init__(*args, **kwargs)
        if players_qs is not None:
            self.fields['player'].queryset = players_qs
        if physios_qs is not None:
            self.fields['reported_by'].queryset = physios_qs

class InjuryFormUpdate(forms.ModelForm):
    injury_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Injury Date'})
    )
    expected_date_of_return = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Expected Date of Return'})
    )

    class Meta:
        model = Injury
        fields = [
            'player', 'reported_by', 'name', 'injury_date',
            'venue', 'team', 'type_of_activity', 'injury_type',
            'cause_of_injury', 'nature_of_injury', 'expected_date_of_return',
            'notes', 'affected_body_part', 'body_segment', 'severity','status',
        ]
        widgets = {
            'player': forms.Select(attrs={'class': 'form-control'}),
            'reported_by': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Reported by'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team'}),
            'type_of_activity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type of activity at time of injury'}),
            'injury_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type of injury'}),
            'cause_of_injury': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cause of injury'}),
            'nature_of_injury': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nature of injury'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows':2}),
            'affected_body_part': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Body region injured'}),
            'body_segment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Body segment'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        players_qs = kwargs.pop('players_qs', None)
        physios_qs = kwargs.pop('physios_qs', None)
        super().__init__(*args, **kwargs)
        if players_qs is not None:
            self.fields['player'].queryset = players_qs
        if physios_qs is not None:
            self.fields['reported_by'].queryset = physios_qs


from django import forms
from .models import MedicalDocument, Injury

class MedicalDocumentForm(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ["date", "title", "notes", "document", "view_option", "injury"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }
    def __init__(self, *args, player=None, **kwargs):
        super().__init__(*args, **kwargs)
        if player is not None:
            self.fields['injury'].queryset = Injury.objects.filter(player=player)
        self.fields['injury'].required = False
        self.fields['injury'].widget.attrs['style'] = 'min-width:172px;'
        self.fields['view_option'].widget.attrs['onchange'] = "showHideInjuryField()"

class MedicalDocumentFormN(forms.ModelForm):
    class Meta:
        model = MedicalDocument
        fields = ["date", "title", "notes", "document", "view_option"]

        widgets = {
                "date": forms.DateInput(attrs={"type": "date"}),
                "notes": forms.Textarea(attrs={"rows": 2}),
            }
    def __init__(self, *args, **kwargs):
        injury = kwargs.pop('injury', None)
        super().__init__(*args, **kwargs)
        self.fields["view_option"].choices = [("injury_only", "Only Injury"), ("injury_profile", "Injury and Profile")]
        
        


class TestAndResultForm(forms.ModelForm):
    class Meta:
        model = TestAndResult
        fields = ['player', 'test', 'date', 'phase', 'trial']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Pop user or organization passed in view kwargs
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)

        if organization:
            # Example: if there is a 'player' field
            if 'player' in self.fields:
                self.fields['player'].queryset = Player.objects.filter(organization=organization)

class TestSummaryFilterForm(forms.Form):
    player = forms.ModelChoiceField(
        queryset=Player.objects.all(),
        required=False,
        empty_label="All Players"
    )
    test = forms.ChoiceField(
        choices=[('', 'All Tests')] + TestAndResult.TEST_CHOICES,
        required=False
    )
