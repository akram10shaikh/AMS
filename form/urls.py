from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'form'

urlpatterns = [
    path('', list_forms, name='list_forms'),
    path('create_form2/', create_form2, name='create_form2'),
    path('add_questions/<int:form_id>/', add_questions, name='add_questions'),
    path('create_question/<int:form_id>/', create_questions, name='create_question'),
    path('edit_form/<int:form_id>/', edit_form, name='edit_form'),
    path('form_detail/<int:form_id>/', form_detail, name='form_detail'),
    path('move_to_recycle/<int:form_id>/', move_to_recycle, name='move_to_recycle'),
    path('recycle_data/', recycle_data, name='recycle_data'),
    path('restore_data/<int:form_id>/', restore_data, name='restore_data'),
    path('delete_form/<int:form_id>/', delete_form, name='delete_form'),
    path('remove_question/<int:question_id>/<int:form_id>/', remove_question, name='remove_question'),
    path('add_player/<int:question_id>/<int:form_id>/', add_player_ques, name='add_player'),
    path('add_response/<int:form_id>/', add_response, name='add_response'),
    path('edit_response/<int:response_id>/', edit_response, name='edit_response'),
    path('delete_response/<int:response_id>', delete_response, name='delete_response'),
    path('sendform/<int:form_id>', send_formlink, name='sendform'),
    path('sendwhatsapp/<int:form_id>', whatsapp_message, name='sendwhatsapp'),
    path('mass_import/', import_excel, name='mass_import'),
    path('form_template/<int:form_id>', downloadExcelFormTemplate, name='form_template'),
    path('form_data', submitted_data_excel, name='form_data'),
    path('form_activity_list/', form_activity_view, name='form_activity_list'),
    path('view_answer/<int:form_id>', view_answer, name='view_answer'),
    path('excel_data_input/<int:form_id>', form_input_excel, name='excel_data_input'),
    path('assign-form/', assign_form, name='assign_form'),
    path('view-assignments/', view_assignments, name='view_assignments'),
    path('unassign/<int:assignment_id>/', unassign_form, name='unassign_form'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
