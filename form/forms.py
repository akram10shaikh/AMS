from django import forms
from .models import Form, Question, Multiple_choice,Sendform_mail,DailyWellnessForm
from player_app.models import Player, Player_Group

class FormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title', 'description','termsandconditions','image']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type']



class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Multiple_choice
        fields = ['choice_text']

class ResponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        form_instance = kwargs.pop('form_instance', None)
        super(ResponseForm, self).__init__(*args, **kwargs)

        if form_instance:
            for question in form_instance.questions.all():
                field_name = f'question_{question.id}'

                if question.question_type == 'short_answer':
                    self.fields[field_name] = forms.CharField(label=question.question_text)
                elif question.question_type == 'paragraph':
                    self.fields[field_name] = forms.CharField(label=question.question_text, widget=forms.Textarea)
                elif question.question_type == 'multiple_choice':
                    choices = [(choice.id, choice.choice_text) for choice in question.options.all()]
                    self.fields[field_name] = forms.ChoiceField(label=question.question_text, choices=choices,
                                                                widget=forms.RadioSelect)
                elif question.question_type == 'checkbox':
                    choices = [(choice.id, choice.choice_text) for choice in question.options.all()]
                    self.fields[field_name] = forms.MultipleChoiceField(label=question.question_text, choices=choices,
                                                                        widget=forms.CheckboxSelectMultiple)
                elif question.question_type == 'dropdown':
                    choices = [(choice.id, choice.choice_text) for choice in question.options.all()]
                    self.fields[field_name] = forms.ChoiceField(label=question.question_text, choices=choices,
                                                                widget=forms.Select)
                elif question.question_type == 'file_upload':
                    self.fields[field_name] = forms.FileField(label=question.question_text, required=False)
                elif question.question_type == 'date':
                    self.fields[field_name] = forms.DateField(label=question.question_text,
                                                              widget=forms.DateInput(attrs={'type': 'date'}),
                                                              required=False)
                elif question.question_type == 'time':
                    self.fields[field_name] = forms.TimeField(label=question.question_text,
                                                              widget=forms.TimeInput(attrs={'type': 'time'}),
                                                              required=False)


class SendForm(forms.ModelForm):
    class Meta:
        model=Sendform_mail
        fields=['subject','message','recipient']

class SendWhatsappForm(forms.Form):
    recipient=forms.MultipleChoiceField(choices=[])
    message = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super( SendWhatsappForm,self).__init__(*args, **kwargs)
        player_choices = [(f'player_{player.id}', f'{player.firstname} {player.lastname}') for player in Player.objects.all()]
        team_choices = [(f'team_{team.id}', f'Team_{team.title}') for team in Player_Group.objects.all()]
        self.fields['recipient'].choices = player_choices + team_choices

class mass_importform(forms.Form):
    form_id=forms.ModelChoiceField(queryset=Form.objects.all())
    file_upload=forms.FileField()
    


# --------------------------------------



class AssignForm(forms.Form):
    form = forms.ModelChoiceField(queryset=Form.objects.all(), label="Select Form")
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Players",
        required=False  
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Player_Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Groups",
        required=False  
    )
