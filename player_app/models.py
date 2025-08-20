from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import Organization,Staff
from django.conf import settings
from django.contrib.auth import get_user_model


# Group model
class Player_Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


User = get_user_model()  # Use the CustomUser model if defined


# Player model
class Player(models.Model):
    Age_category_choices = [
        ('boys_under-15', 'Boys under 15'),
        ('boys_under-19', 'Boys under 19'),
        ('men_under-23', 'Men Under 23'),
        ('men_senior', 'Men Senior'),
    ]
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's user model (CustomUser)
    # Player Information
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True, default='images/default_profile.jpg')
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True) 
    primary_contact_number = models.CharField(max_length=15, blank=True, null=True)
    secondary_contact_number = models.CharField(max_length=15, blank=True, null=True)
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    STATES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Chandigarh', 'Chandigarh'),
        ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Delhi', 'Delhi'),
        ('Puducherry', 'Puducherry'),
        ('Ladakh', 'Ladakh'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('others', 'others')
    ]

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None


    state = models.CharField(max_length=40, choices=STATES, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)

    # Sports Related Information
    batting_style = models.CharField(max_length=100, blank=True, null=True)
    bowling_style = models.CharField(max_length=100, blank=True, null=True)
    handedness_choices = [('R', 'Right'), ('L', 'Left')]
    handedness = models.CharField(max_length=1, choices=handedness_choices, blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    sports_role = models.CharField(max_length=100, blank=True, null=True)
    id_card_number = models.CharField(max_length=50, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    age_category = models.CharField(max_length=50, choices=Age_category_choices, blank=True, null=True)
    team = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)

    # Files/Documents Section
    medical_certificates = models.FileField(upload_to='certificates/', blank=True, null=True)
    aadhar_card_upload = models.FileField(upload_to='documents/aadhar/', blank=True, null=True)
    pan_card_upload = models.FileField(upload_to='documents/pan/', blank=True, null=True)
    marksheets_upload = models.FileField(upload_to='documents/marksheets/', blank=True, null=True)

    # Parents/Guardian Information
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    relation_choices = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Guardian', 'Guardian'),
        ('Other', 'Other')
    ]
    relation = models.CharField(max_length=20, choices=relation_choices, blank=True, null=True)
    guardian_mobile_number = models.CharField(max_length=15, blank=True, null=True)

    # Wellness Report
    disease = models.CharField(max_length=100, blank=True, null=True)
    allergies = models.CharField(max_length=100, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)

    players_in_groups = models.ManyToManyField(Player_Group, blank=True)
    user_role = models.CharField(max_length=20, default='Player')
    password = models.CharField(max_length=100, default=False)

    def __str__(self):
        return self.name


class CampTournament(models.Model):
    CAMP_TYPES = [('camp', 'Camp'), ('tournament', 'Tournament')]

    name = models.CharField(max_length=255)
    camp_type = models.CharField(max_length=50, choices=CAMP_TYPES, default='camp')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=255, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='camps_created')
    participants = models.ManyToManyField(Player, related_name="camps")
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class CampActivity(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('player_added', 'Player Added'),
        ('player_removed', 'Player Removed'),
        ('deleted', 'Deleted'),
        ('recovered', 'Recovered'),
    ]

    camp = models.ForeignKey(CampTournament, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.camp.name} - {self.action} by {self.performed_by.username}"


class Program(models.Model):
    PROGRAM_TYPES = [
        ('rehab', 'Rehabilitation'),
        ('training', 'Training'),
    ]

    program_id = models.AutoField(primary_key=True)  # Unique ID for each program
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES)
    template = models.BooleanField(default=False)  # Indicates if this is a reusable template
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.program_id} - {self.name} ({self.program_type})"


class AssignedProgram(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='assignments')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='programs')
    injury_id = models.CharField(max_length=100, blank=True, null=True)  # Only for rehab programs
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.program.name} assigned to {self.player.name}"


class WorkoutData(models.Model):
    assigned_program = models.ForeignKey(AssignedProgram, on_delete=models.CASCADE, related_name='workout_data')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    workout_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Workout for {self.assigned_program.program.name} by {self.player.name}"

class Injury(models.Model):
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='injuries')
    reported_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, related_name='reported_injuries')
    name = models.CharField(max_length=100,null=True)
    injury_date = models.DateField()
    venue = models.CharField(max_length=100, blank=True)
    team = models.CharField(max_length=100, blank=True)
    type_of_activity = models.CharField(max_length=100, blank=True)
    injury_type = models.CharField(max_length=255,null=True)
    cause_of_injury = models.CharField(max_length=100,null=True)
    nature_of_injury = models.CharField(max_length=100,null=True)
    expected_date_of_return = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    affected_body_part = models.CharField(max_length=255,null=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES,null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open') 
    updated_at = models.DateTimeField(auto_now=True,null=True)
    body_segment = models.CharField(max_length=100, blank=True,null=True)

    def __str__(self):
        return f"{self.player.name} - {self.injury_type} ({self.severity})"
    
class MedicalDocument(models.Model):
    VIEW_CHOICES = [
        ("profile", "Only Profile"),
        ("injury_profile", "Injury and Profile"),
        ("injury_only", "Only Injury"),
    ]
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='medical_documents')
    injury = models.ForeignKey(Injury, null=True, blank=True, related_name="documents", on_delete=models.CASCADE)
    document = models.FileField(upload_to='medical_documents/')
    title = models.CharField(max_length=120,null=True)
    date = models.DateField(null=True, blank=True)  # Date of the document
    notes = models.TextField(blank=True)
    view_option = models.CharField(max_length=20, choices=VIEW_CHOICES,null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Stores the upload timestamp
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='uploaded_documents')

    def __str__(self):
        return f"{self.player.name} - {self.document.name} ({self.uploaded_at})"
    class Meta:
        ordering = ["-date", "-uploaded_at"]


class MedicalActivityLog(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='activity_logs')
    document = models.ForeignKey('MedicalDocument', on_delete=models.CASCADE, related_name='activity_logs')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='medical_activity_logs'
    )
    activity_type = models.CharField(max_length=100, default='UPLOAD') 
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Log: {self.activity_type} for {self.player} by {self.user} at {self.timestamp}"
    class Meta:
        ordering = ['-timestamp']


class InjuryActivityLog(models.Model):
    injury = models.ForeignKey('Injury', on_delete=models.CASCADE, related_name='activity_logs')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100,null=True)  # e.g., 'created', 'updated', 'added note'
    details = models.TextField(blank=True,null=True)     # More info about the action
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.injury} - {self.action} at {self.created_at}"
    
class PlayerActivityLog(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='activity_log')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100, null=True)  # e.g., 'created', 'updated', 'contact info changed'
    details = models.TextField(blank=True, null=True)     # More info about the action
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.player} - {self.action} at {self.created_at}"


class TreatmentRecommendation(models.Model):
    injury = models.ForeignKey(Injury, on_delete=models.CASCADE)
    physio = models.ForeignKey(Staff, on_delete=models.CASCADE, limit_choices_to={'role': 'physio'})  # ✅ Link to Staff instead of separate model
    treatment = models.CharField(max_length=255, null=True, blank=True)
    recommendation_notes = models.TextField()
    recovery_time_weeks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation by {self.physio.name} for {self.injury.player.name}"


class TestAndResult(models.Model):
    TEST_CHOICES = [
         ('10m', '10m'),
        ('20m', '20m'),
        ('40m', '40m'),
        ('YoYo', 'YoYo'),
        ('SBJ', 'SBJ'),
        ('S/L Glute Bridges', 'S/L Glute Bridges (Sec)'),
        ('SL Lunge Calf Raises', 'SL Lunge Calf Raises'),
        ('MB Rotational Throws', 'MB Rotational Throws'),
        ('Copenhagen', 'Copenhagen (Sec)'),
        ('S/L Hop', 'S/L Hop'),
        ('Run A 3', 'Run A 3'),
        ('Run A 3x6', 'Run A 3×6'),
        ('1 Mile', '1 Mile'),
        ('Push-ups', 'Push-ups'),
        ('2 KM', '2 KM'),
        ('CMJ Scores', 'CMJ Scores'),
    ]
    test = models.CharField(max_length=32, choices=TEST_CHOICES)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField()
    phase = models.CharField(max_length=128)
    trial = models.FloatField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.player} - {self.test} ({self.date}) Trial: {self.trial}"
  

