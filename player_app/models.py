from datetime import date
from .utils import age_for_current_season, get_season_cutoff
from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import Organization,Staff
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import age_for_current_season
from django.db.models import Min, Max
from django.db import transaction
from django.utils.dateparse import parse_date
# Group model
class Player_Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


User = get_user_model()  # Use the CustomUser model if defined

# Player model
class Player(models.Model):
    Age_category_choices = [
        ('boys under 16', 'Boys under 16'),
        ('boys under 19', 'Boys under 19'),
        ('men under 23', 'Men Under 23'),
        ('men senior', 'Men Senior'),
        ('girls under 15','Girls under 15'),
        ('girls under 19','Girls under 19'),
        ('women under 23','Women Under 23'),
        ('women senior','Women Senior'),

    ]
    ROLE_CHOICES = [
        ('Batter','Batter'),
        ('Bowler','Bowler'),
        ('All-rounder','All-rounder'),
        ('Wicket-keeper','Wicket-keeper'),
    ]
    PLAYERS_STATAUS = [
        ('full participation', 'Full Participation'),
        ('limited participation', 'Limited Participation'),
        ('no participation', 'No Participation'),
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
    gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    current_age = models.IntegerField(null=True,blank=True)
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
    role = models.CharField(max_length=100, choices=ROLE_CHOICES ,blank=True, null=True)

    # Sports Related Information
    batting_style = models.CharField(max_length=100, blank=True, null=True)
    bowling_style = models.CharField(max_length=100, blank=True, null=True)
    handedness_choices = [('Right', 'Right'), ('Left', 'Left')]
    handedness = models.CharField(max_length=10, choices=handedness_choices, blank=True, null=True)
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

    player_status = models.CharField(max_length=40, choices=PLAYERS_STATAUS,null=True)
    skill_status = models.CharField(max_length=500, null=True, blank=True)
    traning_status = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def save(self, *args, **kwargs):
        if isinstance(self.date_of_birth, str):
            try:
                self.date_of_birth = parse_date(self.date_of_birth)
            except:
                raise ValueError("Invalid date_of_birth format")
        
        if self.date_of_birth:
            self.current_age = age_for_current_season(self.date_of_birth)
            
            # Auto-set age_category based on age + gender
            if self.current_age and self.gender:
                category = self._get_age_category()
                if category:
                    self.age_category = category
        
        super().save(*args, **kwargs)

    def _get_age_category(self):
        """Map current_age + gender to Age_category_choices"""
        if not self.current_age or not self.gender:
            return None
        
        age = self.current_age
        if self.gender.lower() == 'male':
            if age < 16: return 'boys under 16'
            elif age <= 19: return 'boys under 19'
            elif age < 23: return 'men under 23'
            else: return 'men senior'
        else:  # female
            if age < 15: return 'girls under 15'
            elif age <= 19: return 'girls under 19'
            elif age < 23: return 'women under 23'
            else: return 'women senior'

    def __str__(self):
        return self.name


class CampTournament(models.Model):
    CAMP_TYPES = [('camp', 'Camp'), ('tournament', 'Tournament')]

    name = models.CharField(max_length=255)
    camp_type = models.CharField(max_length=50, choices=CAMP_TYPES, default='camp')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)   
    age_category = models.CharField(max_length=50, null=True, blank=True)
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
    PLAYERS_STATAUS = [
        ('full participation', 'Full Participation'),
        ('limited participation', 'Limited Participation'),
        ('no participation', 'No Participation'),
    ]
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='injuries')
    reported_by = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, related_name='reported_injuries')
    name = models.CharField(max_length=100,null=True)
    injury_date = models.DateField()
    diagnosis_date = models.DateField(null=True, blank=True)
    side = models.CharField(max_length=50, null=True, blank=True)
    diagnosis_remarks = models.TextField(blank=True, null=True)
    action_taken = models.TextField(blank=True, null=True)
    traning_participation = models.TextField(null=True,blank=True)

    venue = models.CharField(max_length=100, blank=True)
    team = models.CharField(max_length=100, blank=True)
    type_of_activity = models.CharField(max_length=100, blank=True)
    player_status = models.CharField(max_length=40, choices=PLAYERS_STATAUS,null=True)
    cause_of_injury = models.CharField(max_length=100,null=True, blank=True)
    nature_of_injury = models.CharField(max_length=100,null=True)
    expected_date_of_return = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    affected_body_part = models.CharField(max_length=255,null=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES,null=True,blank=True)
    severity_rating = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open') 
    updated_at = models.DateTimeField(auto_now=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    unknown_injury_date = models.BooleanField(default=False)
    camp_tournament = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True, blank=True, related_name='injuries')

    def __str__(self):
        return f"{self.player.name} - {self.nature_of_injury} ({self.severity})"
    
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
        ('S/L Lunge Calf Raises', 'S/L Lunge Calf Raises'),
        ('MB Rotational Throws', 'MB Rotational Throws'),
        ('Copenhagen', 'Copenhagen (Sec)'),
        ('S/L Hop', 'S/L Hop'),
        ('Run A 3', 'Run A 3'),
        ('Run A 3x6', 'Run A 3x6'),
        ('1 Mile', '1 Mile'),
        ('Push-ups', 'Push-ups'),
        ('2 KM', '2 KM'),
        ('CMJ Scores', 'CMJ Scores'),
        ('Anthropometry Test', 'Anthropometry Test'),
        ('Blood Work', 'Blood Work'),
        ('DEXA Scan Test', 'DEXA Scan Test'),
        ('MSK Injury Assessment','MSK Injury Assessment'),
    ]
    test = models.CharField(max_length=32, choices=TEST_CHOICES, null=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament,on_delete=models.CASCADE,null=True)
    best = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    distance_covered = models.FloatField(null=True, blank=True)
    predicted_vo2max = models.FloatField(null=True, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='yoyo_reports')
    indv_average = models.FloatField(null=True, blank=True)
    reported_by_designation = models.CharField(max_length=100, null=True)
    target = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # Run A 3x6 specific fields
    run_a_3x6_attempt1 = models.IntegerField(null=True, blank=True)
    run_a_3x6_attempt2 = models.IntegerField(null=True, blank=True)
    run_a_3x6_attempt3 = models.IntegerField(null=True, blank=True)
    run_a_3x6_attempt4 = models.IntegerField(null=True, blank=True)
    run_a_3x6_attempt5 = models.IntegerField(null=True, blank=True)
    run_a_3x6_attempt6 = models.IntegerField(null=True, blank=True)
    run_a_3x6_average = models.FloatField(null=True, blank=True)

    # S/L Glute Bridges specific fields
    sl_right = models.FloatField(null=True, blank=True)
    sl_left = models.FloatField(null=True, blank=True)
    sl_difference = models.FloatField(null=True, blank=True)
    slg_ratio = models.FloatField(null=True, blank=True)

    # SL Lunge Calf Raises specific fields
    sl_cr_right = models.FloatField(null=True, blank=True)
    sl_cr_left = models.FloatField(null=True, blank=True)
    sl_cr_difference = models.FloatField(null=True, blank=True)
    sl_cr_ratio = models.FloatField(null=True, blank=True)

    # MB Rotational Throws specific fields
    mb_right = models.FloatField(null=True, blank=True)
    mb_left = models.FloatField(null=True, blank=True)
    mb_difference = models.FloatField(null=True, blank=True)
    mb_ratio = models.FloatField(null=True, blank=True)

    # Copenhagen specific fields
    copenhagen_right = models.FloatField(null=True, blank=True)
    copenhagen_left = models.FloatField(null=True, blank=True)
    copenhagen_difference = models.FloatField(null=True, blank=True)
    copenhagen_ratio = models.FloatField(null=True, blank=True)
    
    # S/L Hop Test specific fields
    sl_hop_right = models.FloatField(null=True, blank=True)
    sl_hop_left = models.FloatField(null=True, blank=True)
    sl_hop_difference = models.FloatField(null=True, blank=True)
    sl_hop_ratio = models.FloatField(null=True, blank=True)

    # CMJ Scores specific fields
    cmj_body_weight = models.FloatField(null=True, blank=True)
    cmj_push_off_distance = models.FloatField(null=True, blank=True)
    cmj_box_height = models.FloatField(null=True, blank=True)
    cmj_load = models.FloatField(null=True, blank=True)
    cmj_jump_height = models.FloatField(null=True, blank=True)
    cmj_flight_time = models.FloatField(null=True, blank=True)
    cmj_contact_time = models.FloatField(null=True, blank=True)
    cmj_force = models.FloatField(null=True, blank=True)
    cmj_velocity = models.FloatField(null=True, blank=True)
    cmj_power = models.FloatField(null=True, blank=True)
    cmj_reactive_strength_index = models.FloatField(null=True, blank=True)
    cmj_stiffness = models.FloatField(null=True, blank=True)
    cmj_readiness_color = models.CharField(max_length=20,null=True, blank=True)
    cmj_jump_type = models.CharField(max_length=50,null=True, blank=True)

    # Anthropometry Test specific fields
    anthropometry_height = models.FloatField(null=True, blank=True)
    anthropometry_weight = models.FloatField(null=True, blank=True)
    anthropometry_age = models.IntegerField(null=True, blank=True)
    anthropometry_chest = models.FloatField(null=True, blank=True)
    anthropometry_mid_axillary = models.FloatField(null=True, blank=True)
    anthropometry_subscapular = models.FloatField(null=True, blank=True)
    anthropometry_triceps = models.FloatField(null=True, blank=True)
    anthropometry_abdomen = models.FloatField(null=True, blank=True)
    anthropometry_suprailiac = models.FloatField(null=True, blank=True)
    anthropometry_mid_thigh = models.FloatField(null=True, blank=True)
    anthropometry_total_skinfold = models.FloatField(null=True, blank=True)
    anthropometry_body_density = models.FloatField(null=True, blank=True)
    anthropometry_fat_percentage = models.FloatField(null=True, blank=True)
    anthropometry_error_corrected = models.CharField(max_length=100, null=True, blank=True)
    anthropometry_chest_n = models.FloatField(null=True, blank=True)
    anthropometry_chest_e = models.FloatField(null=True, blank=True)
    anthropometry_upper_arm = models.FloatField(null=True, blank=True)
    anthropometry_waist = models.FloatField(null=True, blank=True)
    anthropometry_abdomen_cm = models.FloatField(null=True, blank=True)
    anthropometry_hip = models.FloatField(null=True, blank=True)
    anthropometry_thigh = models.FloatField(null=True, blank=True)
    anthropometry_calf = models.FloatField(null=True, blank=True)

    # DEXA Scan Test specific fields
    dexa_height = models.FloatField(null=True, blank=True)
    dexa_weight = models.FloatField(null=True, blank=True)
    dexa_bmi = models.FloatField(null=True, blank=True)
    dexa_rmr = models.FloatField(null=True, blank=True)
    dexa_bmd = models.FloatField(null=True, blank=True)
    dexa_tscore = models.FloatField(null=True, blank=True)
    dexa_total_fat = models.FloatField(null=True, blank=True)
    dexa_lean = models.FloatField(null=True, blank=True)
    dexa_lean_mass = models.FloatField(null=True, blank=True)
    dexa_testosterone = models.FloatField(null=True, blank=True)

    # Blood Work specific fields
    blood_hemoglobin = models.FloatField(null=True, blank=True)
    blood_rbc = models.FloatField(null=True, blank=True)
    blood_platelets = models.FloatField(null=True, blank=True)
    blood_albumin = models.FloatField(null=True, blank=True)
    blood_globulin = models.FloatField(null=True, blank=True)
    blood_uric_acid = models.FloatField(null=True, blank=True)
    blood_creatinine = models.FloatField(null=True, blank=True)
    blood_testosterone = models.FloatField(null=True, blank=True)
    blood_iron = models.FloatField(null=True, blank=True)
    blood_vitamin_d3 = models.FloatField(null=True, blank=True)
    blood_cholesterol = models.FloatField(null=True, blank=True)
    blood_hdl = models.FloatField(null=True, blank=True)
    blood_ldl = models.FloatField(null=True, blank=True)
    blood_ldl_hdl_ratio = models.FloatField(null=True, blank=True)
    blood_vitamin_b12 = models.FloatField(null=True, blank=True)
    blood_lipoprotein = models.FloatField(null=True, blank=True)
    blood_homocysteine = models.FloatField(null=True, blank=True)
    blood_protein = models.FloatField(null=True, blank=True)
    blood_t3 = models.FloatField(null=True, blank=True)
    blood_t4 = models.FloatField(null=True, blank=True)
    blood_tsh = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Compute individual average of all 'best' values for this player and test
        if self.player_id and self.test and self.best is not None:
            qs = TestAndResult.objects.filter(
                player=self.player,
                test=self.test
            ).exclude(id=self.id)
            avg = qs.aggregate(avg_best=Avg('best'))['avg_best']
            count = qs.count()

            if avg is not None and count > 0:
                self.indv_average = (avg * count + self.best) / (count + 1)
            else:
                self.indv_average = self.best
        else:
            self.indv_average = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player} - {self.test} ({self.date}) "




class PlayerAggregate(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    test = models.CharField(max_length=32, choices=TestAndResult.TEST_CHOICES)
    individual_average = models.FloatField(null=True, blank=True)
    left_min = models.FloatField(null=True, blank=True)
    left_max = models.FloatField(null=True, blank=True)
    right_min = models.FloatField(null=True, blank=True)
    right_max = models.FloatField(null=True, blank=True)
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.player.name} - {self.test}"


class GenderAggregate(models.Model):
    gender = models.CharField(max_length=10)  # e.g., Male, Female
    test = models.CharField(max_length=32, choices=TestAndResult.TEST_CHOICES)
    average = models.FloatField(null=True, blank=True)
    left_min = models.FloatField(null=True, blank=True)
    left_max = models.FloatField(null=True, blank=True)
    right_min = models.FloatField(null=True, blank=True)
    right_max = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.gender} - {self.test}"


class CategoryAggregate(models.Model):
    category = models.CharField(max_length=64)
    test = models.CharField(max_length=32, choices=TestAndResult.TEST_CHOICES)
    average = models.FloatField(null=True, blank=True)
    left_min = models.FloatField(null=True, blank=True)
    left_max = models.FloatField(null=True, blank=True)
    right_min = models.FloatField(null=True, blank=True)
    right_max = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.test}"


class CampAggregate(models.Model):
    phase = models.CharField(max_length=64)
    test = models.CharField(max_length=32, choices=TestAndResult.TEST_CHOICES)
    average = models.FloatField(null=True, blank=True)
    left_min = models.FloatField(null=True, blank=True)
    left_max = models.FloatField(null=True, blank=True)
    right_min = models.FloatField(null=True, blank=True)
    right_max = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.phase} - {self.test}"


# Signal receiver outside the model class
@receiver(post_save, sender=TestAndResult)
def update_aggregates(sender, instance, **kwargs):
    player = instance.player
    test = instance.test

    # Update PlayerAggregate
    avg = TestAndResult.objects.filter(player=player, test=test).aggregate(avg_best=Avg('best'))['avg_best']
    PlayerAggregate.objects.update_or_create(
        player=player,
        test=test,
        defaults={'individual_average': avg}
    )

    # Update GenderAggregate
    gender = getattr(player, 'gender', None)  # Adjust if Player has gender attribute
    if gender:
        gender_avg = TestAndResult.objects.filter(player__gender=gender, test=test).aggregate(avg_best=Avg('best'))['avg_best']
        GenderAggregate.objects.update_or_create(
            gender=gender,
            test=test,
            defaults={'average': gender_avg}
        )

    # Update CategoryAggregate
    category = getattr(player, 'category', None)  # Adjust if Player has category attribute
    if category:
        cat_avg = TestAndResult.objects.filter(player__category=category, test=test).aggregate(avg_best=Avg('best'))['avg_best']
        CategoryAggregate.objects.update_or_create(
            category=category,
            test=test,
            defaults={'average': cat_avg}
        )

class Team(models.Model):
    category_choices = [
        ('boys_under-16', 'Boys under 16'),
        ('boys_under-19', 'Boys under 19'),
        ('men_under-23', 'Men Under 23'),
        ('men_senior', 'Men Senior'),
        ('girls_under-15','Girls under 15'),
        ('girls_under-19','Girls under 19'),
        ('women_under-23','Women Under 23'),
        ('women_senior','Women Senior'),

    ]
    name = models.CharField(max_length=150)
    images = models.ImageField(upload_to='team_images/', null=True, blank=True,)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teams')
    players = models.ManyToManyField('Player', blank=True, related_name='teams')
    staff = models.ManyToManyField(Staff, blank=True, related_name='teams')
    category = models.CharField(max_length=100, choices=category_choices,null=True)  # e.g., "U19 Boys", "Senior Men"
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='teams_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)  # Optional: To mark team status
    
    def __str__(self):
        return f"{self.name} ({self.organization.name})"


class NomativeData(models.Model):
    speed_level = models.IntegerField(null=True)
    shuttle_no = models.IntegerField(null=True)
    speed_kmh = models.FloatField(null=True)
    speed_ms = models.FloatField(null=True)
    level_time = models.FloatField(null=True)
    total_distance = models.FloatField(null=True)
    approximately_vo2max = models.FloatField(null=True)
    final_level = models.FloatField(null=True)
    gender_m = models.CharField(max_length=10, default="Male")
    gender_f = models.CharField(max_length=10, default="Female")
    rating_f = models.CharField(max_length=50, null=True)
    rating_m = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Level: {self.speed_level}, Shuttle: {self.shuttle_no}"
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class ReportSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_settings')
    created_at = models.DateTimeField(auto_now_add=True)

    MIN_MAX_CHOICES = [
        ("all_players", "All Players"),
        ("all_players_by_gender", "All Players by Gender"),
        ("category_based", "Category-based"),
        ("date_based", "Date-based (dynamic)"),
        ("manual_entry", "Manual Entry"),
    ]
    min_max_formula = models.CharField(max_length=30, choices=MIN_MAX_CHOICES, default="all_players")
    min_is_better = models.BooleanField(default=False)

    INDV_AVG_CHOICES = [
        ("total_result", "Total Result"),
        ("date_based", "Date Based"),
    ]
    indv_avg_option = models.CharField(max_length=20, choices=INDV_AVG_CHOICES, default="total_result")

    GRP_AVG_CHOICES = [
        ("all_players_date", "Average All Players in Date Range"),
        ("all_players_gender_date", "Average by Gender in Date Range"),
        ("all_players_stored", "Average All Players Stored"),
        ("gender_stored", "Average by Gender Stored"),
        ("category_stored", "Average by Category Stored"),
    ]
    grp_avg_option = models.CharField(max_length=30, choices=GRP_AVG_CHOICES, default="all_players_date")

    categories = models.ManyToManyField(Category, through='CategoryTarget')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Settings by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class CategoryTarget(models.Model):
    settings = models.ForeignKey(ReportSettings, on_delete=models.CASCADE, related_name='category_targets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    target_value = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('settings', 'category')

    def __str__(self):
        return f"{self.category.name}: {self.target_value}"
    


class DailySncLogCamps(models.Model):
    """
    Holds: session overview, wellbeing & logistics, niggles, recovery.
    One row per team + date.
    """
    team = models.ForeignKey(CampTournament, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='snc_logs')
    coach_name = models.CharField(max_length=100, null=True,blank=True)
    date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    # Wellbeing & logistics
    concerns = models.TextField(blank=True)
    niggles = models.BooleanField(default=False)

    # Recovery sessions (comma-separated list: "ice_bath,stretching")
    recovery_sessions = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.team} - {self.date} - {self.coach_name}"


class DailyActivityCamps(models.Model):
    """
    Holds: daily activities grid (duration + intensity per activity) for a log.
    Multiple rows per DailySncLog.
    """
    DURATION_CHOICES = [
        ('<1', '< 1 hr'),
        ('1-2', '1 - 2 hrs'),
        ('2-3', '2 - 3 hrs'),
        ('3-4', '3 - 4 hrs'),
        ('>4', '> 4 hrs'),
    ]

    INTENSITY_CHOICES = [
        ('1', '1 - Very Low'),
        ('2', '2 - Low'),
        ('3', '3 - Moderate'),
        ('4', '4 - High'),
        ('5', '5 - Very High'),
    ]

    log = models.ForeignKey(DailySncLogCamps, on_delete=models.CASCADE, related_name='activities')
    activity_name = models.CharField(max_length=80)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, blank=True)
    intensity = models.CharField(max_length=2, choices=INTENSITY_CHOICES, blank=True)

    def __str__(self):
        return f"{self.log} - {self.activity_name}"
        
    
class SLGluteBridges(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sl_glute_bridges')
    
    # Renamed main fields
    right = models.FloatField(null=True, blank=True)
    left = models.FloatField(null=True, blank=True)
    difference = models.FloatField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True)

    # Renamed min/max fields
    right_min = models.FloatField(null=True, blank=True)
    right_max = models.FloatField(null=True, blank=True)
    left_min = models.FloatField(null=True, blank=True)
    left_max = models.FloatField(null=True, blank=True)

    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)

    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    individual_average_left = models.FloatField(null=True, blank=True)
    individual_average_right = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - set gender/category from player
        - compute diff/ratio
        - save
        - update min/max + aggregates
        """

        # denormalize
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # compute diff/ratio (allow 0.0, only treat None as missing)
        if self.right is not None and self.left is not None:
            self.difference = abs(self.right - self.left)
            if self.right > 0:
                self.ratio = self.left / self.right

        # first save (so we have pk)
        super().save(*args, **kwargs)

        # now update min/max + aggregates once (no recursion)
        with transaction.atomic():
            qs_player = SLGluteBridges.objects.filter(player=self.player)

            # LEFT side: min, max, avg
            if self.left is not None:
                agg_left = qs_player.filter(left__isnull=False).aggregate(
                    min_val=Min('left'),
                    max_val=Max('left'),
                    avg_val=Avg('left'),
                )
                self.left_min = agg_left['min_val']
                self.left_max = agg_left['max_val']
                self.individual_average_left = agg_left['avg_val']

            # RIGHT side: min, max, avg
            if self.right is not None:
                agg_right = qs_player.filter(right__isnull=False).aggregate(
                    min_val=Min('right'),
                    max_val=Max('right'),
                    avg_val=Avg('right'),
                )
                self.right_min = agg_right['min_val']
                self.right_max = agg_right['max_val']
                self.individual_average_right = agg_right['avg_val']

            # persist updated min/max/avg (this save does not call extra logic)
            super().save(update_fields=[
                'left_min', 'left_max',
                'right_min', 'right_max',
                'individual_average_left', 'individual_average_right',
            ])

            # update aggregates
            test_name = 'S/L Glute Bridges'

            # PlayerAggregate
            player_agg, _ = PlayerAggregate.objects.get_or_create(
                player=self.player,
                test=test_name,
                defaults={'left_min': None, 'left_max': None, 'right_min': None, 'right_max': None},
            )
            player_agg.left_min = self.left_min
            player_agg.left_max = self.left_max
            player_agg.right_min = self.right_min
            player_agg.right_max = self.right_max
            player_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # GenderAggregate
            if self.gender:
                gender_players = Player.objects.filter(gender=self.gender)
                gender_results = SLGluteBridges.objects.filter(player__in=gender_players)

                g_left = gender_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                g_right = gender_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=test_name,
                    defaults={'left_min': None, 'left_max': None, 'right_min': None, 'right_max': None},
                )
                gender_agg.left_min = g_left['min_val']
                gender_agg.left_max = g_left['max_val']
                gender_agg.right_min = g_right['min_val']
                gender_agg.right_max = g_right['max_val']
                gender_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # CategoryAggregate
            if self.category:
                cat_players = Player.objects.filter(age_category=self.category)
                cat_results = SLGluteBridges.objects.filter(player__in=cat_players)

                c_left = cat_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                c_right = cat_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=test_name,
                    defaults={'left_min': None, 'left_max': None, 'right_min': None, 'right_max': None},
                )
                cat_agg.left_min = c_left['min_val']
                cat_agg.left_max = c_left['max_val']
                cat_agg.right_min = c_right['min_val']
                cat_agg.right_max = c_right['max_val']
                cat_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            if self.phase:
                camp_qs = SLGluteBridges.objects.filter(phase=self.phase)

                camp_left = camp_qs.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                camp_right = camp_qs.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                test_name = 'S/L Glute Bridges'

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )

                camp_agg.left_min = camp_left['min_val']
                camp_agg.left_max = camp_left['max_val']
                camp_agg.right_min = camp_right['min_val']
                camp_agg.right_max = camp_right['max_val']
                camp_agg.save(update_fields=[
                    'left_min', 'left_max', 'right_min', 'right_max'
                ])

class SLLungeCalfRaises(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,
                              related_name='sl_lunge_calf_raises')

    # Renamed main fields
    right = models.FloatField(null=True, blank=True)
    left = models.FloatField(null=True, blank=True)
    difference = models.FloatField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True)

    # Renamed min/max fields
    right_min = models.FloatField(null=True, blank=True)
    right_max = models.FloatField(null=True, blank=True)
    left_min = models.FloatField(null=True, blank=True)
    left_max = models.FloatField(null=True, blank=True)

    individual_average_left = models.FloatField(null=True, blank=True)
    individual_average_right = models.FloatField(null=True, blank=True)

    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)

    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - set gender/category from player
        - compute diff/ratio
        - save
        - update min/max + aggregates
        """

        # denormalize
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # compute diff/ratio
        if self.right is not None and self.left is not None:
            self.difference = abs(self.right - self.left)
            if self.right > 0:
                self.ratio = self.left / self.right

        # first save (so we have pk)
        super().save(*args, **kwargs)

        # now update min/max + aggregates once (no recursion)
        with transaction.atomic():
            qs_player = SLLungeCalfRaises.objects.filter(player=self.player)

            if self.left is not None:
                agg_left = qs_player.filter(left__isnull=False).aggregate(
                    min_val=Min('left'),
                    max_val=Max('left'),
                    avg_val=Avg('left'),
                )
                self.left_min = agg_left['min_val']
                self.left_max = agg_left['max_val']
                self.individual_average_left = agg_left['avg_val']

            if self.right is not None:
                agg_right = qs_player.filter(right__isnull=False).aggregate(
                    min_val=Min('right'),
                    max_val=Max('right'),
                    avg_val=Avg('right'),
                )
                self.right_min = agg_right['min_val']
                self.right_max = agg_right['max_val']
                self.individual_average_right = agg_right['avg_val']

            # persist updated min/max/avg (this save does not call extra logic)
            super().save(update_fields=[
                'left_min', 'left_max',
                'right_min', 'right_max',
                'individual_average_left', 'individual_average_right',
            ])

            # update aggregates
            test_name = 'S/L Lunge Calf Raises'

            # PlayerAggregate
            player_agg, _ = PlayerAggregate.objects.get_or_create(
                player=self.player,
                test=test_name,
                defaults={
                    'left_min': None,
                    'left_max': None,
                    'right_min': None,
                    'right_max': None,
                },
            )
            player_agg.left_min = self.left_min
            player_agg.left_max = self.left_max
            player_agg.right_min = self.right_min
            player_agg.right_max = self.right_max
            player_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # GenderAggregate
            if self.gender:
                gender_players = Player.objects.filter(gender=self.gender)
                gender_results = SLLungeCalfRaises.objects.filter(player__in=gender_players)

                g_left = gender_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                g_right = gender_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                gender_agg.left_min = g_left['min_val']
                gender_agg.left_max = g_left['max_val']
                gender_agg.right_min = g_right['min_val']
                gender_agg.right_max = g_right['max_val']
                gender_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # CategoryAggregate
            if self.category:
                cat_players = Player.objects.filter(age_category=self.category)
                cat_results = SLLungeCalfRaises.objects.filter(player__in=cat_players)

                c_left = cat_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                c_right = cat_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                cat_agg.left_min = c_left['min_val']
                cat_agg.left_max = c_left['max_val']
                cat_agg.right_min = c_right['min_val']
                cat_agg.right_max = c_right['max_val']
                cat_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])
            
            if self.phase:
                camp_qs = SLLungeCalfRaises.objects.filter(phase=self.phase)

                camp_left = camp_qs.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                camp_right = camp_qs.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                camp_agg.left_min = camp_left['min_val']
                camp_agg.left_max = camp_left['max_val']
                camp_agg.right_min = camp_right['min_val']
                camp_agg.right_max = camp_right['max_val']
                camp_agg.save(update_fields=[
                    'left_min', 'left_max', 'right_min', 'right_max'
                ])



class MBRotationalThrows(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,
                              related_name='mb_rotational_throws')

    # Renamed main fields
    right = models.FloatField(null=True, blank=True)
    left = models.FloatField(null=True, blank=True)
    difference = models.FloatField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True)

    # Renamed min/max fields
    right_min = models.FloatField(null=True, blank=True)
    right_max = models.FloatField(null=True, blank=True)
    left_min = models.FloatField(null=True, blank=True)
    left_max = models.FloatField(null=True, blank=True)

    individual_average_left = models.FloatField(null=True, blank=True)
    individual_average_right = models.FloatField(null=True, blank=True)

    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)

    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - set gender/category from player
        - compute diff/ratio
        - save
        - update min/max + aggregates
        """

        # denormalize
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # compute diff/ratio
        if self.right is not None and self.left is not None:
            self.difference = abs(self.right - self.left)
            if self.right > 0:
                self.ratio = self.left / self.right

        # first save (so we have pk)
        super().save(*args, **kwargs)

        # now update min/max + aggregates once (no recursion)
        with transaction.atomic():
            qs_player = MBRotationalThrows.objects.filter(player=self.player)

            if self.left is not None:
                agg_left = qs_player.filter(left__isnull=False).aggregate(
                    min_val=Min('left'),
                    max_val=Max('left'),
                    avg_val=Avg('left'),
                )
                self.left_min = agg_left['min_val']
                self.left_max = agg_left['max_val']
                self.individual_average_left = agg_left['avg_val']

            if self.right is not None:
                agg_right = qs_player.filter(right__isnull=False).aggregate(
                    min_val=Min('right'),
                    max_val=Max('right'),
                    avg_val=Avg('right'),
                )
                self.right_min = agg_right['min_val']
                self.right_max = agg_right['max_val']
                self.individual_average_right = agg_right['avg_val']

            # persist updated min/max/avg (this save does not call extra logic)
            super().save(update_fields=[
                'left_min', 'left_max',
                'right_min', 'right_max',
                'individual_average_left', 'individual_average_right',
            ])

            # update aggregates
            test_name = 'MB Rotational Throws'

            # PlayerAggregate
            player_agg, _ = PlayerAggregate.objects.get_or_create(
                player=self.player,
                test=test_name,
                defaults={
                    'left_min': None,
                    'left_max': None,
                    'right_min': None,
                    'right_max': None,
                },
            )
            player_agg.left_min = self.left_min
            player_agg.left_max = self.left_max
            player_agg.right_min = self.right_min
            player_agg.right_max = self.right_max
            player_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # GenderAggregate
            if self.gender:
                gender_players = Player.objects.filter(gender=self.gender)
                gender_results = MBRotationalThrows.objects.filter(player__in=gender_players)

                g_left = gender_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                g_right = gender_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                gender_agg.left_min = g_left['min_val']
                gender_agg.left_max = g_left['max_val']
                gender_agg.right_min = g_right['min_val']
                gender_agg.right_max = g_right['max_val']
                gender_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # CategoryAggregate
            if self.category:
                cat_players = Player.objects.filter(age_category=self.category)
                cat_results = MBRotationalThrows.objects.filter(player__in=cat_players)

                c_left = cat_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                c_right = cat_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                cat_agg.left_min = c_left['min_val']
                cat_agg.left_max = c_left['max_val']
                cat_agg.right_min = c_right['min_val']
                cat_agg.right_max = c_right['max_val']
                cat_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            if self.phase:
                camp_qs = MBRotationalThrows.objects.filter(phase=self.phase)

                camp_left = camp_qs.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                camp_right = camp_qs.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                camp_agg.left_min = camp_left['min_val']
                camp_agg.left_max = camp_left['max_val']
                camp_agg.right_min = camp_right['min_val']
                camp_agg.right_max = camp_right['max_val']
                camp_agg.save(update_fields=[
                    'left_min', 'left_max', 'right_min', 'right_max'
                ])

class CopenhagenTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,
                              related_name='copenhagen_tests')

    # Renamed main fields
    right = models.FloatField(null=True, blank=True)
    left = models.FloatField(null=True, blank=True)
    difference = models.FloatField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True)

    # Renamed min/max fields
    right_min = models.FloatField(null=True, blank=True)
    right_max = models.FloatField(null=True, blank=True)
    left_min = models.FloatField(null=True, blank=True)
    left_max = models.FloatField(null=True, blank=True)

    individual_average_left = models.FloatField(null=True, blank=True)
    individual_average_right = models.FloatField(null=True, blank=True)

    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)

    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - set gender/category from player
        - compute diff/ratio
        - save
        - update min/max + aggregates
        """

        # denormalize
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # compute diff/ratio
        if self.right is not None and self.left is not None:
            self.difference = abs(self.right - self.left)
            if self.right > 0:
                self.ratio = self.left / self.right

        # first save (so we have pk)
        super().save(*args, **kwargs)

        # now update min/max + aggregates once (no recursion)
        with transaction.atomic():
            qs_player = CopenhagenTest.objects.filter(player=self.player)

            if self.left is not None:
                agg_left = qs_player.filter(left__isnull=False).aggregate(
                    min_val=Min('left'),
                    max_val=Max('left'),
                    avg_val=Avg('left'),
                )
                self.left_min = agg_left['min_val']
                self.left_max = agg_left['max_val']
                self.individual_average_left = agg_left['avg_val']

            if self.right is not None:
                agg_right = qs_player.filter(right__isnull=False).aggregate(
                    min_val=Min('right'),
                    max_val=Max('right'),
                    avg_val=Avg('right'),
                )
                self.right_min = agg_right['min_val']
                self.right_max = agg_right['max_val']
                self.individual_average_right = agg_right['avg_val']

            # persist updated min/max/avg (this save does not call extra logic)
            super().save(update_fields=[
                'left_min', 'left_max',
                'right_min', 'right_max',
                'individual_average_left', 'individual_average_right',
            ])

            # update aggregates
            test_name = 'Copenhagen'

            # PlayerAggregate
            player_agg, _ = PlayerAggregate.objects.get_or_create(
                player=self.player,
                test=test_name,
                defaults={
                    'left_min': None,
                    'left_max': None,
                    'right_min': None,
                    'right_max': None,
                },
            )
            player_agg.left_min = self.left_min
            player_agg.left_max = self.left_max
            player_agg.right_min = self.right_min
            player_agg.right_max = self.right_max
            player_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # GenderAggregate
            if self.gender:
                gender_players = Player.objects.filter(gender=self.gender)
                gender_results = CopenhagenTest.objects.filter(player__in=gender_players)

                g_left = gender_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                g_right = gender_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                gender_agg.left_min = g_left['min_val']
                gender_agg.left_max = g_left['max_val']
                gender_agg.right_min = g_right['min_val']
                gender_agg.right_max = g_right['max_val']
                gender_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # CategoryAggregate
            if self.category:
                cat_players = Player.objects.filter(age_category=self.category)
                cat_results = CopenhagenTest.objects.filter(player__in=cat_players)

                c_left = cat_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                c_right = cat_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                cat_agg.left_min = c_left['min_val']
                cat_agg.left_max = c_left['max_val']
                cat_agg.right_min = c_right['min_val']
                cat_agg.right_max = c_right['max_val']
                cat_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            if self.phase:
                camp_qs = CopenhagenTest.objects.filter(phase=self.phase)

                camp_left = camp_qs.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                camp_right = camp_qs.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                camp_agg.left_min = camp_left['min_val']
                camp_agg.left_max = camp_left['max_val']
                camp_agg.right_min = camp_right['min_val']
                camp_agg.right_max = camp_right['max_val']
                camp_agg.save(update_fields=[
                    'left_min', 'left_max', 'right_min', 'right_max'
                ])

class SLHopTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,
                              related_name='sl_hop_tests')


    right = models.FloatField(null=True, blank=True)
    left = models.FloatField(null=True, blank=True)
    difference = models.FloatField(null=True, blank=True)
    ratio = models.FloatField(null=True, blank=True)


    right_min = models.FloatField(null=True, blank=True)
    right_max = models.FloatField(null=True, blank=True)
    left_min = models.FloatField(null=True, blank=True)
    left_max = models.FloatField(null=True, blank=True)

    individual_average_left = models.FloatField(null=True, blank=True)
    individual_average_right = models.FloatField(null=True, blank=True)

    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)

    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - set gender/category from player
        - compute diff/ratio
        - save
        - update min/max + aggregates
        """

        # denormalize
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # compute diff/ratio
        if self.right is not None and self.left is not None:
            self.difference = abs(self.right - self.left)
            if self.right > 0:
                self.ratio = self.left / self.right

        # first save (so we have pk)
        super().save(*args, **kwargs)

        # now update min/max + aggregates once (no recursion)
        with transaction.atomic():
            qs_player = SLHopTest.objects.filter(player=self.player)

            if self.left is not None:
                agg_left = qs_player.filter(left__isnull=False).aggregate(
                    min_val=Min('left'),
                    max_val=Max('left'),
                    avg_val=Avg('left'),
                )
                self.left_min = agg_left['min_val']
                self.left_max = agg_left['max_val']
                self.individual_average_left = agg_left['avg_val']

            if self.right is not None:
                agg_right = qs_player.filter(right__isnull=False).aggregate(
                    min_val=Min('right'),
                    max_val=Max('right'),
                    avg_val=Avg('right'),
                )
                self.right_min = agg_right['min_val']
                self.right_max = agg_right['max_val']
                self.individual_average_right = agg_right['avg_val']

            # persist updated min/max/avg (this save does not call extra logic)
            super().save(update_fields=[
                'left_min', 'left_max',
                'right_min', 'right_max',
                'individual_average_left', 'individual_average_right',
            ])

            # update aggregates
            test_name = 'S/L Hop'

            # PlayerAggregate
            player_agg, _ = PlayerAggregate.objects.get_or_create(
                player=self.player,
                test=test_name,
                defaults={
                    'left_min': None,
                    'left_max': None,
                    'right_min': None,
                    'right_max': None,
                },
            )
            player_agg.left_min = self.left_min
            player_agg.left_max = self.left_max
            player_agg.right_min = self.right_min
            player_agg.right_max = self.right_max
            player_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # GenderAggregate
            if self.gender:
                gender_players = Player.objects.filter(gender=self.gender)
                gender_results = SLHopTest.objects.filter(player__in=gender_players)

                g_left = gender_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                g_right = gender_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                gender_agg.left_min = g_left['min_val']
                gender_agg.left_max = g_left['max_val']
                gender_agg.right_min = g_right['min_val']
                gender_agg.right_max = g_right['max_val']
                gender_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            # CategoryAggregate
            if self.category:
                cat_players = Player.objects.filter(age_category=self.category)
                cat_results = SLHopTest.objects.filter(player__in=cat_players)

                c_left = cat_results.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                c_right = cat_results.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                cat_agg.left_min = c_left['min_val']
                cat_agg.left_max = c_left['max_val']
                cat_agg.right_min = c_right['min_val']
                cat_agg.right_max = c_right['max_val']
                cat_agg.save(update_fields=['left_min', 'left_max', 'right_min', 'right_max'])

            if self.phase:
                camp_qs = SLHopTest.objects.filter(phase=self.phase)

                camp_left = camp_qs.aggregate(
                    min_val=Min('left_min'),
                    max_val=Max('left_max'),
                )
                camp_right = camp_qs.aggregate(
                    min_val=Min('right_min'),
                    max_val=Max('right_max'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),
                    test=test_name,
                    defaults={
                        'left_min': None,
                        'left_max': None,
                        'right_min': None,
                        'right_max': None,
                    },
                )
                camp_agg.left_min = camp_left['min_val']
                camp_agg.left_max = camp_left['max_val']
                camp_agg.right_min = camp_right['min_val']
                camp_agg.right_max = camp_right['max_val']
                camp_agg.save(update_fields=[
                    'left_min', 'left_max', 'right_min', 'right_max'
                ])


class FortyMeterTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    best = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    distance_covered = models.FloatField(null=True, blank=True)
    predicted_vo2max = models.FloatField(null=True, blank=True)
    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='m40_reports'
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `best`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `best`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate (min/max/average)
        """
        TEST_NAME = '40m'  # must match your TestAndResult.TEST_CHOICES

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        # update per-player aggregates and global aggregates
        with transaction.atomic():
            qs_player = FortyMeterTest.objects.filter(
                player=self.player,
                best__isnull=False,
            )

            if self.best is not None:
                agg = qs_player.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = FortyMeterTest.objects.filter(
                    gender=self.gender,
                    best__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:67]

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = FortyMeterTest.objects.filter(
                    category=self.category,
                    best__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])


            if self.phase:
                camp_qs = FortyMeterTest.objects.filter(
                    phase=self.phase,
                    best__isnull=False,
                )
                camp_agg_vals = camp_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),   # or self.phase.name; keep consistent with other tests
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_agg_vals['min_val']
                camp_agg.max = camp_agg_vals['max_val']
                camp_agg.average = camp_agg_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])

class TwentyMeterTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    best = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    distance_covered = models.FloatField(null=True, blank=True)
    predicted_vo2max = models.FloatField(null=True, blank=True)
    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='test_20m'
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `best`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `best`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate (min/max/average)
        """
        TEST_NAME = '20m'  # must exist in TestAndResult.TEST_CHOICES

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        with transaction.atomic():
            qs_player = TwentyMeterTest.objects.filter(
                player=self.player,
                best__isnull=False,
            )

            if self.best is not None:
                agg = qs_player.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = TwentyMeterTest.objects.filter(
                    gender=self.gender,
                    best__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:67]

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = TwentyMeterTest.objects.filter(
                    category=self.category,
                    best__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])

            if self.phase:
                camp_qs = TwentyMeterTest.objects.filter(
                    phase=self.phase,
                    best__isnull=False,
                )
                camp_vals = camp_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),  # or self.phase.name, but keep consistent
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_vals['min_val']
                camp_agg.max = camp_vals['max_val']
                camp_agg.average = camp_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])

class TenMeterTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    best = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    distance_covered = models.FloatField(null=True, blank=True)
    predicted_vo2max = models.FloatField(null=True, blank=True)
    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='test_10m',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `best`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `best`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate (min/max/average)
        """
        TEST_NAME = '10m'  # must match TestAndResult.TEST_CHOICES

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        with transaction.atomic():
            qs_player = TenMeterTest.objects.filter(
                player=self.player,
                best__isnull=False,
            )

            if self.best is not None:
                agg = qs_player.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = TenMeterTest.objects.filter(
                    gender=self.gender,
                    best__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:67]

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = TenMeterTest.objects.filter(
                    category=self.category,
                    best__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])
   
             # CampAggregate (per phase + test on `best`)
            if self.phase:
                camp_qs = TenMeterTest.objects.filter(
                    phase=self.phase,
                    best__isnull=False,
                )
                camp_vals = camp_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),  # or self.phase.name; keep consistent with other tests
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_vals['min_val']
                camp_agg.max = camp_vals['max_val']
                camp_agg.average = camp_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])


class SBJTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    best = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    distance_covered = models.FloatField(null=True, blank=True)
    predicted_vo2max = models.FloatField(null=True, blank=True)
    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='sbj_reports',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `best`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `best`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate (min/max/average)
        """
        TEST_NAME = 'SBJ'  # must match TestAndResult.TEST_CHOICES

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        with transaction.atomic():
            qs_player = SBJTest.objects.filter(
                player=self.player,
                best__isnull=False,
            )

            if self.best is not None:
                agg = qs_player.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = SBJTest.objects.filter(
                    gender=self.gender,
                    best__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:14]

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = SBJTest.objects.filter(
                    category=self.category,
                    best__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])

            # CampAggregate (per phase + test on `best`)
            if self.phase:
                camp_qs = SBJTest.objects.filter(
                    phase=self.phase,
                    best__isnull=False,
                )
                camp_vals = camp_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),  # or self.phase.name; keep consistent with other tests
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_vals['min_val']
                camp_agg.max = camp_vals['max_val']
                camp_agg.average = camp_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])


class YoYoTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)

    # core YoYo result fields
    best = models.FloatField(null=True, blank=True)              # e.g. best level or distance
    distance_covered = models.FloatField(null=True, blank=True)  # total meters
    predicted_vo2max = models.FloatField(null=True, blank=True)  # from distance
    notes = models.TextField(blank=True, null=True)

    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='yoyo_test',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `best`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `best`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate (min/max/average)
        """
        TEST_NAME = 'YoYo'  # must match TestAndResult.TEST_CHOICES

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        with transaction.atomic():
            qs_player = YoYoTest.objects.filter(
                player=self.player,
                best__isnull=False,
            )

            if self.best is not None:
                agg = qs_player.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = YoYoTest.objects.filter(
                    gender=self.gender,
                    best__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:14]

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = YoYoTest.objects.filter(
                    category=self.category,
                    best__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])

             # CampAggregate (per phase + test on `best`)
            if self.phase:
                camp_qs = YoYoTest.objects.filter(
                    phase=self.phase,
                    best__isnull=False,
                )
                camp_vals = camp_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),  # or self.phase.name; keep consistent with other tests
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_vals['min_val']
                camp_agg.max = camp_vals['max_val']
                camp_agg.average = camp_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])


class RunA3Test(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)

    # core result fields
    best = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    distance_covered = models.FloatField(null=True, blank=True)
    predicted_vo2max = models.FloatField(null=True, blank=True)

    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='run_a3_reports',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `best`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `best`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate (min/max/average)
        """
        TEST_NAME = 'Run A 3'  # ensure this exists in TestAndResult.TEST_CHOICES

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        with transaction.atomic():
            qs_player = RunA3Test.objects.filter(
                player=self.player,
                best__isnull=False,
            )

            if self.best is not None:
                agg = qs_player.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = RunA3Test.objects.filter(
                    gender=self.gender,
                    best__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:14]

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = RunA3Test.objects.filter(
                    category=self.category,
                    best__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])

              # CampAggregate (per phase + test on `best`)
            if self.phase:
                camp_qs = RunA3Test.objects.filter(
                    phase=self.phase,
                    best__isnull=False,
                )
                camp_vals = camp_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),  # or self.phase.name; keep consistent with other tests
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_vals['min_val']
                camp_agg.max = camp_vals['max_val']
                camp_agg.average = camp_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])

class OneMileTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)

    best = models.FloatField(null=True, blank=True)              # e.g. best time
    notes = models.TextField(blank=True, null=True)
    distance_covered = models.FloatField(null=True, blank=True)  # usually 1609m
    predicted_vo2max = models.FloatField(null=True, blank=True)

    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='one_mile_reports',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `best`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `best`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate (min/max/average)
        """
        TEST_NAME = '1 Mile'  # must match TestAndResult.TEST_CHOICES

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        with transaction.atomic():
            qs_player = OneMileTest.objects.filter(
                player=self.player,
                best__isnull=False,
            )

            if self.best is not None:
                agg = qs_player.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = OneMileTest.objects.filter(
                    gender=self.gender,
                    best__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:14]

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = OneMileTest.objects.filter(
                    category=self.category,
                    best__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])
          
            # CampAggregate (per phase + test on `best`)
            if self.phase:
                camp_qs = OneMileTest.objects.filter(
                    phase=self.phase,
                    best__isnull=False,
                )
                camp_vals = camp_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),  # or self.phase.name; keep consistent
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_vals['min_val']
                camp_agg.max = camp_vals['max_val']
                camp_agg.average = camp_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])

       
class TwoKmTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)

    best = models.FloatField(null=True, blank=True)              # e.g. best time for 2 km
    notes = models.TextField(blank=True, null=True)
    distance_covered = models.FloatField(null=True, blank=True)  # usually 2000m
    predicted_vo2max = models.FloatField(null=True, blank=True)

    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='two_km_reports',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `best`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `best`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate (min/max/average)
        """
        TEST_NAME = '2 KM'  # must match TestAndResult.TEST_CHOICES

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        with transaction.atomic():
            qs_player = TwoKmTest.objects.filter(
                player=self.player,
                best__isnull=False,
            )

            if self.best is not None:
                agg = qs_player.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = TwoKmTest.objects.filter(
                    gender=self.gender,
                    best__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:14]

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = TwoKmTest.objects.filter(
                    category=self.category,
                    best__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])

            # CampAggregate (per phase + test on `best`)
            if self.phase:
                camp_qs = TwoKmTest.objects.filter(
                    phase=self.phase,
                    best__isnull=False,
                )
                camp_vals = camp_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),  # or self.phase.name; keep consistent across tests
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_vals['min_val']
                camp_agg.max = camp_vals['max_val']
                camp_agg.average = camp_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])

class PushUpsTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)

    best = models.FloatField(null=True, blank=True)  # max reps in test
    notes = models.TextField(blank=True, null=True)
    distance_covered = models.FloatField(null=True, blank=True)  # optional / unused
    predicted_vo2max = models.FloatField(null=True, blank=True)  # optional

    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='pushups_reports',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `best`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        """
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `best`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate (min/max/average)
        """
        TEST_NAME = 'Push-ups'  # must match TestAndResult.TEST_CHOICES

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        with transaction.atomic():
            qs_player = PushUpsTest.objects.filter(
                player=self.player,
                best__isnull=False,
            )

            if self.best is not None:
                agg = qs_player.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = PushUpsTest.objects.filter(
                    gender=self.gender,
                    best__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:14]

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = PushUpsTest.objects.filter(
                    category=self.category,
                    best__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )  # [web:11][web:15]

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])
         
             # CampAggregate (per phase + test on `best`)
            if self.phase:
                camp_qs = PushUpsTest.objects.filter(
                    phase=self.phase,
                    best__isnull=False,
                )
                camp_vals = camp_qs.aggregate(
                    min_val=Min('best'),
                    max_val=Max('best'),
                    avg_val=Avg('best'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),  # or phase.name; keep consistent with other tests
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_vals['min_val']
                camp_agg.max = camp_vals['max_val']
                camp_agg.average = camp_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])



class CMJTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)

    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='cmj_reports',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # CMJ metrics
    cmj_body_weight = models.FloatField(null=True, blank=True)
    cmj_push_off_distance = models.FloatField(null=True, blank=True)
    cmj_box_height = models.FloatField(null=True, blank=True)
    cmj_load = models.FloatField(null=True, blank=True)
    cmj_jump_height = models.FloatField(null=True, blank=True)          # primary metric
    cmj_flight_time = models.FloatField(null=True, blank=True)
    cmj_contact_time = models.FloatField(null=True, blank=True)
    cmj_force = models.FloatField(null=True, blank=True)
    cmj_velocity = models.FloatField(null=True, blank=True)
    cmj_power = models.FloatField(null=True, blank=True)
    cmj_reactive_strength_index = models.FloatField(null=True, blank=True)
    cmj_stiffness = models.FloatField(null=True, blank=True)
    cmj_readiness_color = models.CharField(max_length=20, null=True, blank=True)
    cmj_jump_type = models.CharField(max_length=50, null=True, blank=True)


    class Meta:
        ordering = ['-date']


class AnthropometryTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)

    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='anthropometry_reports',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # Anthropometry fields
    anthropometry_height = models.FloatField(null=True, blank=True)
    anthropometry_weight = models.FloatField(null=True, blank=True)
    anthropometry_age = models.IntegerField(null=True, blank=True)

    anthropometry_chest = models.FloatField(null=True, blank=True)
    anthropometry_mid_axillary = models.FloatField(null=True, blank=True)
    anthropometry_subscapular = models.FloatField(null=True, blank=True)
    anthropometry_triceps = models.FloatField(null=True, blank=True)
    anthropometry_abdomen = models.FloatField(null=True, blank=True)
    anthropometry_suprailiac = models.FloatField(null=True, blank=True)
    anthropometry_mid_thigh = models.FloatField(null=True, blank=True)

    anthropometry_total_skinfold = models.FloatField(null=True, blank=True)
    anthropometry_body_density = models.FloatField(null=True, blank=True)
    anthropometry_fat_percentage = models.FloatField(null=True, blank=True)
    anthropometry_error_corrected = models.CharField(
        max_length=100, null=True, blank=True
    )

    anthropometry_chest_n = models.FloatField(null=True, blank=True)
    anthropometry_chest_e = models.FloatField(null=True, blank=True)
    anthropometry_upper_arm = models.FloatField(null=True, blank=True)
    anthropometry_waist = models.FloatField(null=True, blank=True)
    anthropometry_abdomen_cm = models.FloatField(null=True, blank=True)
    anthropometry_hip = models.FloatField(null=True, blank=True)
    anthropometry_thigh = models.FloatField(null=True, blank=True)
    anthropometry_calf = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Anthropometry - {self.player} - {self.date}"


class DexaScanTest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True, null=True)

    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='dexa_reports',
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # DEXA Scan fields
    dexa_height = models.FloatField(null=True, blank=True)
    dexa_weight = models.FloatField(null=True, blank=True)
    dexa_bmi = models.FloatField(null=True, blank=True)
    dexa_rmr = models.FloatField(null=True, blank=True)
    dexa_bmd = models.FloatField(null=True, blank=True)
    dexa_tscore = models.FloatField(null=True, blank=True)
    dexa_total_fat = models.FloatField(null=True, blank=True)
    dexa_lean = models.FloatField(null=True, blank=True)
    dexa_lean_mass = models.FloatField(null=True, blank=True)
    dexa_testosterone = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"DEXA Scan - {self.player} - {self.date}"


class BloodTest(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey('CampTournament', on_delete=models.CASCADE, null=True)

    # core blood markers
    blood_hemoglobin = models.FloatField(null=True, blank=True)
    blood_rbc = models.FloatField(null=True, blank=True)
    blood_platelets = models.FloatField(null=True, blank=True)
    blood_albumin = models.FloatField(null=True, blank=True)
    blood_globulin = models.FloatField(null=True, blank=True)
    blood_uric_acid = models.FloatField(null=True, blank=True)
    blood_creatinine = models.FloatField(null=True, blank=True)
    blood_testosterone = models.FloatField(null=True, blank=True)
    blood_iron = models.FloatField(null=True, blank=True)
    blood_vitamin_d3 = models.FloatField(null=True, blank=True)
    blood_cholesterol = models.FloatField(null=True, blank=True)
    blood_hdl = models.FloatField(null=True, blank=True)
    blood_ldl = models.FloatField(null=True, blank=True)
    blood_ldl_hdl_ratio = models.FloatField(null=True, blank=True)
    blood_vitamin_b12 = models.FloatField(null=True, blank=True)
    blood_lipoprotein = models.FloatField(null=True, blank=True)
    blood_homocysteine = models.FloatField(null=True, blank=True)
    blood_protein = models.FloatField(null=True, blank=True)
    blood_t3 = models.FloatField(null=True, blank=True)
    blood_t4 = models.FloatField(null=True, blank=True)
    blood_tsh = models.FloatField(null=True, blank=True)

    notes = models.TextField(blank=True, null=True)

    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blood_tests_reported',
    )

    # denormalized fields (optional but consistent with other tests)
    gender = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    reported_by_designation = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-date']


class MSKInjuryAssessment(models.Model):
    # --- Basic info ---
    physiotherapist_name = models.CharField(max_length=255)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)

    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    # --- Choices ---

    # Example: store skills as a comma-separated string or JSON later.
    # For now, simple text; implement multi-select in forms/serializer.
    skills = models.TextField(
        null=True,
        blank=True,
        help_text="Comma-separated skills, e.g. 'RHB,RAMF,WK'",
    )

    participation_category = models.CharField(
        max_length=32,
    
        null=True,
        blank=True,
    )

    SIDE_CHOICES = [
        ('LEFT', 'Left'),
        ('RIGHT', 'Right'),
    ]
    dominant_side = models.CharField(
        max_length=5,
        null=True,
        blank=True,
    )
    lead_leg = models.CharField(
        max_length=5,
        
        null=True,
        blank=True,
    )

    FOOT_POSTURE_CHOICES = [
        ('NEUTRAL', 'Neutral'),
        ('PRONATED', 'Pronated'),
        ('SUPINATED', 'Supinated'),
    ]
    rear_foot_right = models.CharField(
        max_length=9,
        
        null=True,
        blank=True,
    )
    rear_foot_left = models.CharField(
        max_length=9,
        
        null=True,
        blank=True,
    )
    mid_foot_right = models.CharField(
        max_length=9,
        
        null=True,
        blank=True,
    )
    mid_foot_left = models.CharField(
        max_length=9,
        
        null=True,
        blank=True,
    )

    # LLD
    LLD_CHOICES = [
        ('NEUTRAL', 'Neutral'),
        ('RIGHT_LONGER', 'Right Longer'),
        ('LEFT_LONGER', 'Left Longer'),
    ]
    lld = models.CharField(
        max_length=12,
        
        null=True,
        blank=True,
    )

    # Positive/Negative
    POS_NEG_CHOICES = [
        ('NEGATIVE', 'Negative'),
        ('POSITIVE', 'Positive'),
    ]

    # --- Range / numeric tests ---

    df_lunge_right = models.FloatField(null=True, blank=True)
    df_lunge_left = models.FloatField(null=True, blank=True)

    tibial_dial_right = models.FloatField(null=True, blank=True)
    tibial_dial_left = models.FloatField(null=True, blank=True)

    hip_ir_90_supine_right = models.FloatField(null=True, blank=True)
    hip_ir_90_supine_left = models.FloatField(null=True, blank=True)

    fabers_right = models.FloatField(null=True, blank=True)
    fabers_left = models.FloatField(null=True, blank=True)

    shoulder_ir_90_right = models.FloatField(null=True, blank=True)
    shoulder_ir_90_left = models.FloatField(null=True, blank=True)

    shoulder_er_90_right = models.FloatField(null=True, blank=True)
    shoulder_er_90_left = models.FloatField(null=True, blank=True)

    pec_minor_length_right = models.FloatField(null=True, blank=True)
    pec_minor_length_left = models.FloatField(null=True, blank=True)

    thoracic_rotation_right = models.FloatField(null=True, blank=True)
    thoracic_rotation_left = models.FloatField(null=True, blank=True)

    thomas_pos1_right = models.FloatField(null=True, blank=True)
    thomas_pos1_left = models.FloatField(null=True, blank=True)

    thomas_pos2_right = models.FloatField(null=True, blank=True)
    thomas_pos2_left = models.FloatField(null=True, blank=True)

    thomas_pos3_right = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="e.g. 'ER-10, IR-5, 0'",
    )
    thomas_pos3_left = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="e.g. 'ER-10, IR-5, 0'",
    )

    thomas_pos4_right = models.FloatField(null=True, blank=True)
    thomas_pos4_left = models.FloatField(null=True, blank=True)

    # --- Clinical tests (Positive/Negative) ---

    anterior_apprehension_right = models.CharField(
        max_length=8,
        
        null=True,
        blank=True,
    )
    anterior_apprehension_left = models.CharField(
        max_length=8,
        
        null=True,
        blank=True,
    )

    relocation_right = models.CharField(
        max_length=8,
        
        null=True,
        blank=True,
    )
    relocation_left = models.CharField(
        max_length=8,
        
        null=True,
        blank=True,
    )

    gird_erg_right = models.CharField(
        max_length=8,
        
        null=True,
        blank=True,
    )
    gird_erg_left = models.CharField(
        max_length=8,
        
        null=True,
        blank=True,
    )

    hk_test_right = models.CharField(
        max_length=8,
        
        null=True,
        blank=True,
    )
    hk_test_left = models.CharField(
        max_length=8,
        
        null=True,
        blank=True,
    )

    obriens_right = models.CharField(
        max_length=8,
      
        null=True,
        blank=True,
    )
    obriens_left = models.CharField(
        max_length=8,
       
        null=True,
        blank=True,
    )

    # --- Context / meta ---

    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    comments = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"MSK Assessment - {self.player} - {self.date}"


class DailyWellnessTest(models.Model):
    # Common links
    player = models.ForeignKey(
        "Player",
        on_delete=models.CASCADE,
        related_name="daily_wellness_tests",
    )
    phase = models.ForeignKey(
        "CampTournament",
        on_delete=models.CASCADE,
        related_name="daily_wellness_tests",null=True,blank=True
    )

    date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    # 1) Urine color (single choice)
    URINE_COLOR_CHOICES = [
        ("NO_COLOR", "No Color"),
        ("PALE_STRAW", "Pale Straw Yellow"),
        ("TRANSLUCENT_YELLOW", "Translucent Yellow"),
        ("DARK_YELLOW", "Dark Yellow"),
        ("AMBER", "Amber"),
        ("BROWN", "Brown"),
    ]
    urine_color = models.CharField(
        max_length=32,
        choices=URINE_COLOR_CHOICES,
    )

    # 2) Soreness level 1–10
    soreness_level = models.PositiveSmallIntegerField()  # 1–10 in form validation

    # 3) Fatigue level 0–10
    fatigue_level = models.PositiveSmallIntegerField()

    # 4) Sleep hours 0–10 (you can use DecimalField if you want 7.5 etc.)
    sleep_hours = models.DecimalField(max_digits=4, decimal_places=1)

    # 5) Aches / pain / niggle
    has_pain = models.BooleanField()
    pain_comment = models.TextField(blank=True)

    # 6) Motivation level (1–10)
    motivation_level = models.PositiveSmallIntegerField()

    # 7) Number of balls bowled
    balls_bowled = models.PositiveIntegerField()

    # 8) Training session completed (multi-select)
    TRAINING_TYPE_CHOICES = [
        ("STRENGTH", "Strength"),
        ("CONDITIONING", "Conditioning"),
        ("BOWLING", "Bowling"),
        ("FIELDING", "Fielding"),
        ("BATTING", "Batting"),
        ("REST", "Rest"),
        ("MATCH", "Match"),
        ("OTHER", "Other"),
    ]
    # store as comma‑separated values or JSON depending on your DB
    training_session_types = models.JSONField(default=list)

    # 9) Total session RPE 0–10
    total_rpe = models.PositiveSmallIntegerField()

    # Audit fields if you use them elsewhere
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_daily_wellness_tests",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Daily Wellness Test"
        verbose_name_plural = "Daily Wellness Tests"

    def __str__(self):
        return f"{self.player} - {self.date}"
    


class RunA3x6Test(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    phase = models.ForeignKey(CampTournament, on_delete=models.CASCADE, null=True)
    
    # 3x6 trials
    trial1 = models.IntegerField(null=True, blank=True)
    trial2 = models.IntegerField(null=True, blank=True)
    trial3 = models.IntegerField(null=True, blank=True)
    trial4 = models.IntegerField(null=True, blank=True)
    trial5 = models.IntegerField(null=True, blank=True)
    trial6 = models.IntegerField(null=True, blank=True)
    
    # Calculated average from trials
    average = models.FloatField(null=True, blank=True)
    
    notes = models.TextField(blank=True, null=True)
    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='run_a_3x6_test'
    )
    gender = models.CharField(null=True, max_length=50)
    category = models.CharField(null=True, max_length=100)
    reported_by_designation = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # per-player stats on `average`
    min = models.FloatField(null=True, blank=True)
    max = models.FloatField(null=True, blank=True)
    individual_average = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def calculate_average(self):
        """Calculate average from 6 trials (ignore None/empty)"""
        trials = [self.trial1, self.trial2, self.trial3, self.trial4, self.trial5, self.trial6]
        valid_trials = [t for t in trials if t is not None]
        return round(sum(valid_trials) / len(valid_trials), 2) if valid_trials else None

    def save(self, *args, **kwargs):
        """
        - Calculate average from trials
        - denormalize gender/category
        - save
        - update per-player min/max/avg on `average`
        - update PlayerAggregate + GenderAggregate + CategoryAggregate + CampAggregate
        """
        TEST_NAME = 'run_a_3x6'  # Must exist in TestAndResult.TEST_CHOICES

        # Calculate average from trials
        self.average = self.calculate_average()

        # denormalize from player
        if self.player:
            self.gender = self.player.gender
            self.category = getattr(self.player, 'age_category', None)

        # first save to ensure pk
        super().save(*args, **kwargs)

        with transaction.atomic():
            qs_player = RunA3x6Test.objects.filter(
                player=self.player,
                average__isnull=False,
            )

            if self.average is not None:
                agg = qs_player.aggregate(
                    min_val=Min('average'),
                    max_val=Max('average'),
                    avg_val=Avg('average'),
                )

                # update this row
                self.min = agg['min_val']
                self.max = agg['max_val']
                self.individual_average = agg['avg_val']
                super().save(update_fields=['min', 'max', 'individual_average'])

                # PlayerAggregate for this player + test
                p_agg, _ = PlayerAggregate.objects.get_or_create(
                    player=self.player,
                    test=TEST_NAME,
                    defaults={
                        'individual_average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                p_agg.min = agg['min_val']
                p_agg.max = agg['max_val']
                p_agg.individual_average = agg['avg_val']
                p_agg.save(update_fields=['min', 'max', 'individual_average'])

            # GenderAggregate
            if self.gender:
                gender_qs = RunA3x6Test.objects.filter(
                    gender=self.gender,
                    average__isnull=False,
                )
                g_agg = gender_qs.aggregate(
                    min_val=Min('average'),
                    max_val=Max('average'),
                    avg_val=Avg('average'),
                )

                gender_agg, _ = GenderAggregate.objects.get_or_create(
                    gender=self.gender,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                gender_agg.min = g_agg['min_val']
                gender_agg.max = g_agg['max_val']
                gender_agg.average = g_agg['avg_val']
                gender_agg.save(update_fields=['min', 'max', 'average'])

            # CategoryAggregate
            if self.category:
                cat_qs = RunA3x6Test.objects.filter(
                    category=self.category,
                    average__isnull=False,
                )
                c_agg = cat_qs.aggregate(
                    min_val=Min('average'),
                    max_val=Max('average'),
                    avg_val=Avg('average'),
                )

                cat_agg, _ = CategoryAggregate.objects.get_or_create(
                    category=self.category,
                    test=TEST_NAME,
                    defaults={'average': None, 'min': None, 'max': None},
                )
                cat_agg.min = c_agg['min_val']
                cat_agg.max = c_agg['max_val']
                cat_agg.average = c_agg['avg_val']
                cat_agg.save(update_fields=['min', 'max', 'average'])

            # Camp/Phase Aggregate
            if self.phase:
                camp_qs = RunA3x6Test.objects.filter(
                    phase=self.phase,
                    average__isnull=False,
                )
                camp_vals = camp_qs.aggregate(
                    min_val=Min('average'),
                    max_val=Max('average'),
                    avg_val=Avg('average'),
                )

                camp_agg, _ = CampAggregate.objects.get_or_create(
                    phase=str(self.phase.name),
                    test=TEST_NAME,
                    defaults={
                        'average': None,
                        'left_min': None, 'left_max': None,
                        'right_min': None, 'right_max': None,
                        'min': None, 'max': None,
                    },
                )
                camp_agg.min = camp_vals['min_val']
                camp_agg.max = camp_vals['max_val']
                camp_agg.average = camp_vals['avg_val']
                camp_agg.save(update_fields=['min', 'max', 'average'])
