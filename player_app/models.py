from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import Organization,Staff
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import age_for_current_season

# Group model
class Player_Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


User = get_user_model()  # Use the CustomUser model if defined

# Player model
class Player(models.Model):
    Age_category_choices = [
        ('boys_under-16', 'Boys under 16'),
        ('boys_under-19', 'Boys under 19'),
        ('men_under-23', 'Men Under 23'),
        ('men_senior', 'Men Senior'),
        ('girls_under-15','Girls under 15'),
        ('girls_under-19','Girls under 19'),
        ('women_under-23','Women Under 23'),
        ('women_senior','Women Senior'),

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
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
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

    player_status = models.CharField(max_length=40, choices=PLAYERS_STATAUS,null=True)
    skill_status = models.CharField(max_length=500, null=True, blank=True)
    traning_status = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def save(self, *args, **kwargs):
        if self.date_of_birth:
            self.current_age = age_for_current_season(self.date_of_birth)
        super().save(*args, **kwargs)

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
    cause_of_injury = models.CharField(max_length=100,null=True)
    nature_of_injury = models.CharField(max_length=100,null=True)
    expected_date_of_return = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    affected_body_part = models.CharField(max_length=255,null=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES,null=True)
    severity_rating = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open') 
    updated_at = models.DateTimeField(auto_now=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    unknown_injury_date = models.BooleanField(default=False)


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
        ('SL Lunge Calf Raises', 'SL Lunge Calf Raises'),
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
    individual_average = models.FloatField(null=True)
    updated_at = models.DateTimeField(auto_now=True)


class GenderAggregate(models.Model):
    gender = models.CharField(max_length=10)  # e.g., Male, Female
    test = models.CharField(max_length=32, choices=TestAndResult.TEST_CHOICES)
    average = models.FloatField(null=True)
    updated_at = models.DateTimeField(auto_now=True)


class CategoryAggregate(models.Model):
    category = models.CharField(max_length=64)
    test = models.CharField(max_length=32, choices=TestAndResult.TEST_CHOICES)
    average = models.FloatField(null=True)
    updated_at = models.DateTimeField(auto_now=True)


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
    coach_name = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)

    # Wellbeing & logistics
    concerns = models.TextField(blank=True)
    niggles = models.BooleanField(default=False)

    # Recovery sessions (comma-separated list: "ice_bath,stretching")
    recovery_sessions = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('team', 'date')
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