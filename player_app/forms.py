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
        fields = ['player', 'affected_body_part', 'severity', 'injury_date', 'status', 'notes']
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
            'role','district','batting_style', 'bowling_style', 'handedness', 'age_category', 
            'guardian_name', 'relation', 'guardian_mobile_number',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class OrganizationPlayerFormUpdate(forms.ModelForm):
    BOWLING_CHOICES = [
        ('None','None'),
        ('Spinner','Spinner'),
        ('Spin Bowling All-rounder','Spin Bowling All-rounder'),
        ('Right-arm fast', 'Spin Bowling All-rounder'),
        ('Right-arm fast-medium', 'Right-arm fast-medium'),
        ('Right-arm medium', 'Right-arm medium'),
        ('Right-arm off-spin', 'Right-arm off-spin'),
        ('Right-arm leg-spin (leg break)', 'Right-arm leg-spin (leg break)'),
        ('Fast Bowler','Fast Bowler'),
        ('Fast Bowler All-rounder','Fast Bowler All-rounder'),
        ('Left-arm fast','Left-arm fast'),
        ('Left-arm fast-medium','Left-arm fast-medium'),
        ('Left-arm medium','Left-arm medium'),
        ('Left-arm orthodox spin','Left-arm orthodox spin'),
        ('Left-arm unorthodox spin (chinaman)','Left-arm unorthodox spin (chinaman)'),
        ('Other (Specify)','Other (Specify)'),
    ]
    BATTING_CHOICES =  [
        ('None','None'),
        ('Right Arm Batter','Right Arm Batter'),
        ('Left Arm Batter','Left Arm Batter'),
    ]

    new_password = forms.CharField(
        label="Set New Password", required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    bowling_style = forms.ChoiceField(choices=BOWLING_CHOICES, required=False)
    batting_style = forms.ChoiceField(choices=BATTING_CHOICES, required=False)
    class Meta:
        model = Player
        fields = [
            'name', 'image', 'email', 'date_of_birth',
            'primary_contact_number', 'secondary_contact_number', 'gender','state',
            'role', 'batting_style', 'bowling_style','player_status','handedness', 'age_category',
            'guardian_name', 'relation', 'guardian_mobile_number','skill_status','traning_status',
        ]
        widgets = {'date_of_birth': forms.DateInput(attrs={'type': 'date'})}

# Injury Form
SIDE_CHOICES = [
    ('left', 'Left'),
    ('right', 'Right'),
    ('bilateral', 'Bilateral'),
]
class InjuryForm(forms.ModelForm):
    injury_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Injury Date'})
    )
    expected_date_of_return = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Expected Date of Return'})
    )
    
    from player_app.models import Player  # import Player model

    player_status = forms.ChoiceField(
        choices=Player._meta.get_field('player_status').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    side = forms.ChoiceField(
        choices=SIDE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Side of body injured'}),
        required=True,
        label='Side of body injured'
    )
    class Meta:
        model = Injury
        fields = [
            'player', 'reported_by', 'name', 'injury_date','diagnosis_date',
            'venue', 'team', 'type_of_activity','side','diagnosis_remarks','action_taken','traning_participation',
            'nature_of_injury', 'expected_date_of_return',
            'notes', 'affected_body_part', 'severity_rating', 'player_status','unknown_injury_date','camp_tournament',
        ]
        widgets = {
            'player': forms.Select(attrs={'class': 'form-control'}),
            'reported_by': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Reported by'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team'}),
            'type_of_activity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type of activity at time of injury'}),
            'camp_tournament': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Camp/Tournament'}),
            'nature_of_injury': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nature of injury'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows':2}),
            'affected_body_part': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Body region injured'}),
            # 'player_status': forms.Select(attrs={'class': 'form-control'}),
            'action_taken': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Action Taken', 'rows': 2}),
            'traning_participation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Training Participation'}),
            'severity_rating': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Severity Rating','min': 1,'max': 10,}),
            'diagnosis_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Diagnosis Date'}),
        }

    def __init__(self, *args, **kwargs):
        players_qs = kwargs.pop('players_qs', None)
        physios_qs = kwargs.pop('physios_qs', None)
        camps_qs = kwargs.pop('camps_qs', None)
        super().__init__(*args, **kwargs)
        if players_qs is not None:
            self.fields['player'].queryset = players_qs
        if physios_qs is not None:
            self.fields['reported_by'].queryset = physios_qs
        if camps_qs is not None:
            self.fields['camp_tournament'].queryset = camps_qs  # NEW: Filter camps
    def clean_severity_rating(self):
        value = self.cleaned_data.get('severity_rating')
        if value is None:
            raise forms.ValidationError("Severity rating is required.")
        if not (1 <= value <= 10):
            raise forms.ValidationError("Severity rating must be between 1 and 10.")
        return value

BODY_PART_CHOICES = [
    ('head', 'Head'),
    ('neck', 'Neck'),
    ('chest', 'Chest'),
    ('back', 'Back'),
    ('abdomen', 'Abdomen'),
    ('shin-left', 'Shin Left'),
    ('shin-right', 'Shin Right'),
    ('left-arm', 'Left Arm'),
    ('right-arm', 'Right Arm'),
    ('left-hand', 'Left Hand'),
    ('right-hand', 'Right Hand'),
    ('left-leg', 'Left Leg'),
    ('right-leg', 'Right Leg'),
    ('left-foot', 'Left Foot'),
    ('right-foot', 'Right Foot'),
    ('obliques-left', 'Obliques Left'),
    ('obliques-right', 'Obliques Right'),
    ('rotator-cuff-left', 'Rotator Cuff Left'),
    ('rotator-cuff-right', 'Rotator Cuff Right'),
    ('finger-left', 'Finger Left'),
    ('finger-right', 'Finger Right'),
    ('lower-back', 'Lower Back'),
    ('knee-left', 'Knee Left'),
    ('knee-right', 'Knee Right'),
    ('hamstring-left', 'Hamstring Left'),
    ('hamstring-right', 'Hamstring Right'),
    ('shin-left', 'Shin Left'),
    ('shin-right', 'Shin Right'),
    ('ankle-left', 'Ankle Left'),
    ('ankle-right', 'Ankle Right'),
    ('other', 'Other'),
]   
class InjuryFormUpdate(forms.ModelForm):
    injury_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Injury Date'})
    )
    expected_date_of_return = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Expected Date of Return'})
    )

    affected_body_part = forms.MultipleChoiceField(
        required=False,
        choices=BODY_PART_CHOICES,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '12',
            'id': 'part-select'
        }),
        label='Affected Body Parts',
    )
    side = forms.ChoiceField(
        choices=SIDE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Side of body injured'}),
        required=True,
        label='Side of body injured'
    )
    class Meta:
        model = Injury
        fields = [
            'player', 'reported_by', 'name', 'injury_date','diagnosis_date',
            'venue', 'team', 'type_of_activity', 'unknown_injury_date',
            'cause_of_injury', 'nature_of_injury', 'expected_date_of_return',
            'notes', 'affected_body_part', 'severity_rating', 'side','diagnosis_remarks','action_taken','traning_participation', 'camp_tournament',
        ]
        widgets = {
            'player': forms.Select(attrs={'class': 'form-control'}),
            'reported_by': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Reported by'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'team': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team'}),
            'type_of_activity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type of activity at time of injury'}),
            'cause_of_injury': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cause of injury'}),
            'nature_of_injury': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nature of injury'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows': 2}),
            'diagnosis_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Diagnosis Date'}),
            'side': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Side of body injured'}),
            'action_taken': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Action Taken', 'rows': 2}),
            'traning_participation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Training Participation'}),
            'severity_rating': forms.NumberInput(attrs={'class': 'form-control','placeholder': 'Severity Rating','min': 1,'max': 10,}),
            'camp_tournament': forms.Select(attrs={'class': 'form-control','placeholder': 'Select Camp/Tournament'}),

            }

    def __init__(self, *args, **kwargs):
        players_qs = kwargs.pop('players_qs', None)
        physios_qs = kwargs.pop('physios_qs', None)
        camps_qs = kwargs.pop('camps_qs', None)  
        super().__init__(*args, **kwargs)
        if players_qs is not None:
            self.fields['player'].queryset = players_qs
        if physios_qs is not None:
            self.fields['reported_by'].queryset = physios_qs
        
        if camps_qs is not None:
            self.fields['camp_tournament'].queryset = camps_qs  # NEW: Filter camps


        # Initialize multiple select field with list if instance value exists
        if self.instance and self.instance.affected_body_part:
            self.initial['affected_body_part'] = self.instance.affected_body_part.split(',')
    
    def clean_severity_rating(self):
        value = self.cleaned_data.get('severity_rating')
        if value is None:
            raise forms.ValidationError("Severity rating is required.")
        if not (1 <= value <= 10):
            raise forms.ValidationError("Severity rating must be between 1 and 10.")
        return value

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Join list from form multiple select to comma-separated string for storage
        instance.affected_body_part = ','.join(self.cleaned_data.get('affected_body_part', []))
        if commit:
            instance.save()
        return instance

from player_app.models import Player
class PlayerAvailabilityForm(forms.ModelForm):
    player_status = forms.ChoiceField(
        choices=Player._meta.get_field('player_status').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Injury
        fields = ['status']  # Remove 'player_status' here since handled manually

        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial value of player_status from related player
        if self.instance and self.instance.pk:
            self.fields['player_status'].initial = self.instance.player.player_status

    def save(self, commit=True):
        # Save injury status normally
        injury = super().save(commit=commit)
        # Save player_status to the related player
        player_status = self.cleaned_data.get('player_status')
        if player_status and injury.player.player_status != player_status:
            injury.player.player_status = player_status
            injury.player.save()
        return injury

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
        fields = ['player', 'test', 'date', 'phase', 'best','notes','reported_by']
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
            if 'reported_by' in self.fields:
                # Get the org admin user
                try:
                    org_admin_user = organization.user
                except Organization.DoesNotExist:
                    org_admin_user = None

                # Get all staff user ids for this organization
                staff_users = User.objects.filter(staff__organization=organization)

                # Combine org admin + staff users queryset
                users_qs = User.objects.none()
                if org_admin_user:
                    users_qs = User.objects.filter(id=org_admin_user.id) | staff_users
                else:
                    users_qs = staff_users

                self.fields['reported_by'].queryset = users_qs.distinct()

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


