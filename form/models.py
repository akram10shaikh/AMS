from django.db import models
from player_app.models import Player, Player_Group
from accounts.models import Organization
from django.utils import timezone
from django.utils.timezone import now
from django.conf import settings

form_choices = [('private', 'private'), ('public', 'public')]


class Form(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    termsandconditions = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="form_image/", null=True, blank=True)
    IsDelete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None)
    form_visibility = models.CharField(max_length=100, choices=form_choices)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ('short_answer', 'Short Answer'),
        ('paragraph', 'Paragraph'),
        ('multiple_choice', 'Multiple Choice'),
        ('multiple_choice_grid', 'Multiple Choice Grid'),
        ('checkbox', 'Check Boxes'),
        ('dropdown', 'Dropdowns'),
        ('file_upload', 'File Upload'),
        ('date', 'Date'),
        ('time', 'Time'),
    ]

    form = models.ManyToManyField(Form, related_name='questions')
    question_text = models.CharField(max_length=255)
    question_image = models.ImageField(upload_to="question_image/", null=True, blank=True)
    organisation = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    player_list = models.ManyToManyField(Player, related_name='player_list', blank=True)
    input_add_player = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text


class Multiple_choice(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text


class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    related_player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'Response for {self.form.title}:{self.id}'


class Answer(models.Model):
    response = models.ForeignKey(Response, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(default='', blank=True)
    file_upload = models.FileField(upload_to='uploads/', null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.question.question_text}: {self.answer_text or "File Uploaded"}'


class Sendform_mail(models.Model):
    recipient = models.TextField(default="player1")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    subject = models.CharField(max_length=300)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)


# have to convert form relationship to many to many

class Form_activity(models.Model):
    choice_set = [("created", "Created"), ("updated", "Updated"), ("data_input", "Data Input"),
                  ("move_to_trash", "Move To Trash"), ("deleted", "Deleted"), ("input_deleted", "Input Deleted"),
                  ("input_updation", "Input Updation")]
    form_instance = models.ForeignKey(Form, related_name="forms", on_delete=models.CASCADE)
    by_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE)
    action = models.CharField(max_length=200, choices=choice_set)
    dateofactivity = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.form_instance.title}'


# ----------------------------

class DailyWellnessForm(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='forms_created')
    is_deleted = models.BooleanField(default=False)  # Soft delete field

    # Task 7 - Aadarsh
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=now)

    def __str__(self):
        return self.name
    

class WellnessFormAssignment(models.Model):
    wellness_form = models.ForeignKey(DailyWellnessForm, on_delete=models.SET_NULL, null=True)
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Player_Group, null=True, blank=True, on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assignment of {self.wellness_form} to {self.player or self.group or self.camp or self.tournament}"
    

    # ================================

class FormAssignment(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Player_Group, on_delete=models.CASCADE, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.player:
            return f"{self.form.title} assigned to {self.player.name}"
        elif self.group:
            return f"{self.form.title} assigned to Group: {self.group.name}"


