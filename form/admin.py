from django.contrib import admin
from .models import Form, Question, Response, Answer, Multiple_choice, Sendform_mail, Form_activity
from .models import *


class ChoiceInline(admin.TabularInline):
    model = Multiple_choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'form')
    list_filter = ('question_type', 'form')
    search_fields = ('question_text',)
    inlines = [ChoiceInline]


class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'organization')
    search_fields = ('title', 'description')


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('form', 'created_at')
    list_filter = ('form',)
    search_fields = ('form__title',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'answer_text', 'file_upload', 'date', 'time')
    list_filter = ('response', 'question')
    search_fields = ('response__form__title', 'question__question_text', 'answer_text')


@admin.register(Multiple_choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question')
    search_fields = ('choice_text',)


class SendFormAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'form')
    search_fields = ('sender',)


admin.site.register(Form, FormAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Sendform_mail, SendFormAdmin)
admin.site.register(Form_activity)

admin.site.register(FormAssignment)
# admin.site.register(WellnessFormAssignment)
