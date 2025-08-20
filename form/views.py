from django.shortcuts import render, redirect, get_object_or_404
from form.forms import QuestionForm, FormForm, SendForm, SendWhatsappForm, mass_importform
from form.models import Form, Question, Answer, Response, Multiple_choice, Form_activity, WellnessFormAssignment, \
    DailyWellnessForm
from player_app.models import Player, Player_Group
from accounts.models import Organization
from accounts.models import Staff
import pandas as pd
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from django.db.models import Q
import os
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Form, FormAssignment
from player_app.models import Player, Player_Group
from .forms import AssignForm
from django.http import HttpResponseRedirect
from django.contrib import messages


def player_home(request):
    # Filter forms assigned to the currently logged-in player
    player_assignments = FormAssignment.objects.filter(player=request.user)  # assuming `player` is the User model
    forms = [assignment.form for assignment in player_assignments]

    context = {
        'forms': forms,
        'player': request.user,  # assuming the player is the logged-in user
    }
    return render(request, 'player_home.html', context)


def home(request):
    return render(request, 'home.html')


@login_required
def create_form2(request):
    organization_list = ""
    if request.method == 'POST':
        form_form = FormForm(request.POST)
        if form_form.is_valid():
            form_instance = form_form.save(commit=False)
            User = get_user_model()
            user = User.objects.get(id=request.user.id)
            if user.role == 'Staff':
                staff_ins = Staff.objects.filter(user=user)
                if not staff_ins or user.staff.add_form == False:
                    return HttpResponseForbidden(
                        "User is not authorised to access this page. This could be due to user doesn't have permission to create forms.")
                form_instance.user = user
                form_instance.organization = user.staff.organization
                form_visibility = request.POST.get('form_visibility')
                if form_visibility:
                    form_instance.form_visibility = form_visibility
                form_instance.save()
                q1, create = Question.objects.get_or_create(question_text="Date of Activity", question_type="date",
                                                            organisation=user.staff.organization)
                q2, create = Question.objects.get_or_create(question_text="Time of Activity performed",
                                                            question_type="time", organisation=user.staff.organization)
                form_instance.questions.add(q1, q2)
                ins = Form_activity.objects.create(form_instance=form_instance, action="created", by_user=user)
                return redirect('add_questions', form_id=form_instance.id)
            elif user.role == 'organization' or user.is_super_admin == True:
                if user.role == 'organization':
                    ins_org = Organization.objects.filter(user=user)
                    if not ins_org:
                        return HttpResponseForbidden("There is no organization associated with this user.")
                    form_instance.user = user
                    form_instance.organization = ins_org
                    form_visibility = request.POST.get('form_visibility')
                    form_instance.form_visibility = form_visibility
                    form_instance.save()
                    Form_activity.objects.create(form_instance=form_instance, action="created", by_user=user)
                    q1, create = Question.objects.get_or_create(question_text="Date of Activity", question_type="date",
                                                                organisation=ins_org)
                    q2, create = Question.objects.get_or_create(question_text="Time of Activity performed",
                                                                question_type="time", organisation=ins_org)
                    form_instance.questions.add(q1, q2)
                else:
                    form_instance.user = user
                    organization_list = Organization.objects.all()
                    organization = Organization.objects.get(id=request.POST.get('organization'))
                    form_instance.organization = organization
                    form_visibility = request.POST.get('form_visibility')
                    form_instance.form_visibility = form_visibility
                    form_instance.save()
                    Form_activity.objects.create(form_instance=form_instance, action="created", by_user=user)
                    q1, create = Question.objects.get_or_create(question_text="Date of Activity", question_type="date",
                                                                organisation=organization)
                    q2, create = Question.objects.get_or_create(question_text="Time of Activity performed",
                                                                question_type="time", organisation=organization)
                    form_instance.questions.add(q1, q2)
                return redirect('form:add_questions', form_id=form_instance.id)
            else:
                return HttpResponseForbidden(
                    "User is not authorised to access this page. This could be due to user doesn't have permission to create forms.")
    else:
        form_form = FormForm()
    organization_list = Organization.objects.all()
    print(organization_list, 'yes')
    return render(request, 'forms/create_form2.html', {'form_form': form_form, 'organization_list': organization_list})


def add_questions(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id)
    if request.user.role == 'Player':
        return HttpResponseForbidden("You do not have permission to create")
    elif (request.user.role == 'Staff' and request.user != form_instance.user) or (
            request.user.role == 'OrganizationAdmin' and request.user.organization != form_instance.organization):
        return HttpResponseForbidden("You do not have permission to create")
    questions = Question.objects.filter(organisation=form_instance.organization)
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        question = Question.objects.get(id=question_text)
        add_player = bool(request.POST.get('input_add_player'))
        print(add_player)
        question.input_add_player = add_player
        question.save()
        form_instance.questions.add(question)
        return redirect('add_questions', form_id=form_instance.id)
    question = form_instance.questions.all()
    return render(request, 'forms/add_questions.html',
                  {'form': form_instance, 'questions': questions, 'exist_question': question})


@login_required
def create_questions(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id)
    if request.user.role == 'Player':
        return HttpResponseForbidden("You do not have permission to create")
    elif (request.user.role == 'Staff' and request.user != form_instance.user) or (
            request.user.role == 'OrganizationAdmin' and request.user.organization != form_instance.organization):
        return HttpResponseForbidden("You do not have permission to create")
    else:
        players = Player.objects.filter(organization=form_instance.organization).values()
        if request.method == 'POST':
            question_text = request.POST.get('question_text')
            question_type = request.POST.get('question_type')
            question_image = request.FILES.get('question_image')
            if question_image:
                question, created = Question.objects.get_or_create(question_text=question_text,
                                                                   question_type=question_type,
                                                                   question_image=question_image,
                                                                   organisation=form_instance.organization)
            else:
                question, created = Question.objects.get_or_create(question_text=question_text,
                                                                   question_type=question_type,
                                                                   organisation=form_instance.organization)
            choices = request.POST.get('options')
            if question_type in ['multiple_choice', 'checkbox', 'dropdown']:
                choice_list = choices.split(',')
                for choice_text in choice_list:
                    choice = choice_text.strip()
                    Multiple_choice.objects.create(question=question, choice_text=choice.lower())
            elif question_type in ['multiple_choice_grid']:
                add_players_list = set(request.POST.get('player_lists').split(','))
                print(add_players_list)
                choice_list = choices.split(',')
                for choice_text in choice_list:
                    choice = choice_text.strip()
                    Multiple_choice.objects.create(question=question, choice_text=choice.lower())
                question.player_list.add(*add_players_list)
                question.input_add_player = bool(request.POST.get('input_add_player'))
                question.save()
            form_instance.questions.add(question)
            return redirect('add_questions', form_id=form_instance.id)
    return render(request, 'forms/create_question.html', {'form': form_instance, 'player_list': players})


def remove_question(request, question_id, form_id):
    form = get_object_or_404(Form, id=form_id)
    question = get_object_or_404(Question, id=question_id)
    if request.user.role == 'Player' or request.user.role == 'Staff' and request.user != form.user:
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission.")
    elif request.user.role == 'OrganizationAdmin' and request.user.organization != form.organization:
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission.")
    if question.question_text not in ['Time of Activity performed', 'Date of Activity']:
        form.questions.remove(question)
        return redirect('list_forms')
    else:
        messages.error(request, 'Cannot remove this question its mandatory.')
    return render(request, 'forms/form_detail.html', {'form_instance': form})


@login_required
def list_forms(request):
    User = get_user_model()
    form_user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        value = request.POST.get('search_value')
        if value and value.isdigit():
            if request.user.role == 'Staff':
                access = form_user.staff.add_result
                if access == False:
                    search_ans = Form.objects.filter(id=int(value), user=form_user, IsDelete=False)
                else:
                    search_ans = Form.objects.filter(Q(id=int(value)) & (Q(user=form_user) | (
                                Q(organization=form_user.staff.organization) & Q(form_visibility='public'))) & Q(
                        IsDelete=False))
                return render(request, 'forms/list_forms.html', {'forms': search_ans})
            elif form_user.role == 'OrganizationAdmin':
                organisation = form_user.organization
                search_ans = Form.objects.filter(Q(id=int(value)) & Q(organization=organisation) & Q(IsDelete=False))
                return render(request, 'forms/list_forms.html', {'forms': search_ans})
            else:
                search_ans = Form.objects.filter(id=int(value), IsDelete=False)
                return render(request, 'forms/list_forms.html', {'forms': search_ans})
        elif value != None:
            if form_user.role == 'Staff':
                access = form_user.staff.add_result
                if access == False:
                    search_ans = Form.objects.filter(title__icontains=value, user=form_user, IsDelete=False)
                else:
                    search_ans = Form.objects.filter(Q(title__icontains=value) & (Q(user=form_user) | (
                                Q(organization=form_user.staff.organization) & Q(form_visibility='public')))).values()
            elif form_user.role == 'OrganizationAdmin':
                search_ans = Form.objects.filter(title__icontains=value, organization=form_user.organization,
                                                 IsDelete=False).values()
            elif form_user.role == 'SuperAdmin':
                search_ans = Form.objects.filter(title__icontains=value, IsDelete=False).values()
            else:
                return HttpResponseForbidden("You are not allowed to access this page")
            return render(request, 'forms/list_forms.html', {'forms': search_ans})
        else:
            messages.error(request, 'Please enter a valid search value ')
            return render(request, 'forms/list_forms.html')
    if request.user.role == 'Staff':
        staff = Staff.objects.filter(user=form_user, add_result=True)
        if staff:
            forms = Form.objects.filter(
                (Q(user=request.user) | Q(form_visibility='public')) & Q(organization=form_user.staff.organization) & Q(
                    IsDelete=False))
            return render(request, 'forms/list_forms.html', {'forms': forms, 'staff': staff})
        else:
            forms = Form.objects.filter(user=form_user)
            return render(request, 'forms/list_forms.html', {'forms': forms, 'staff': staff})
    elif request.user.role == 'OrganizationAdmin':
        organization = form_user.organization
        forms = Form.objects.filter(organization=organization, IsDelete=False)
        return render(request, 'forms/list_forms.html', {'forms': forms})
    elif request.user.role == 'SuperAdmin':
        forms = Form.objects.filter(IsDelete=False)
        return render(request, 'forms/list_forms.html', {'forms': forms})
    else:
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission to access form dashboard.")


@login_required
def form_detail(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id)
    if (request.user != form_instance.user and request.user.role == 'Staff') or request.user.role == 'Player':
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission to view forms.")
    elif (request.user.role == 'OrganizationAdmin') and (request.user.organization != form_instance.organization):
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission to view forms.")
    responses = Response.objects.filter(form=form_instance).order_by('-created_at')
    # print(form_instance.image.url)
    # Handle the edit response functionality
    if request.method == 'POST' and 'edit_response_id' in request.POST:
        response_id = request.POST.get('edit_response_id')
        return redirect('edit_response', response_id=response_id)

    return render(request, 'forms/form_detail.html', {
        'form_instance': form_instance,
        'responses': responses
    })


@login_required
def edit_form(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id)
    questions = form_instance.questions.all  # Use the many-to-many relationship
    if (request.user != form.user and request.user.role == 'Staff') or request.user.role == 'Player':
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission to edit forms.")
    elif (request.user.role == 'OrganizationAdmin') and (request.user.organization != form_instance.organization):
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission to edit forms.")
    if request.method == "POST":
        form = FormForm(request.POST, instance=form_instance)
        if form.is_valid():
            ins = form.save(commit=False)
            ins.title = request.POST['title']
            ins.description = request.POST['description']
            ins.termsandconditions = request.POST['termsandconditions']
            ins.image = request.POST.get('image')
            ins.save()
            ins = Form_activity.objects.create(form_instance=form_instance, action="updated", by_user=request.user)
            count = 1
            for question in questions:
                question.question_text = request.POST[f"ques{count}"]
                question.question_type = request.POST[f"questype{count}"]
                question.save()
            return redirect('forms/form_detail')
        else:
            form = FormForm(instance=form_instance)
    return render(request, 'forms/editform.html', {"questions": questions})


def move_to_recycle(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    if (request.user == form.user and request.user.role == 'Staff') or request.user.role == 'SuperAdmin' or (
            request.user.role == 'OrganizationAdmin' and form.organization == request.user.organization):
        form.IsDelete = True
        form.save()
        Form_activity.objects.create(form_instance=form, action="move_to_trash", by_user=request.user)
        return redirect('recycle_data')
    else:
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission to delete forms.")


@login_required
def recycle_data(request):
    if request.user.role == 'Player':
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission.")
    if request.user.role == 'Staff':
        forms = Form.objects.filter(IsDelete=True, user=request.user)
    elif request.user.role == 'SuperAdmin':
        forms = Form.objects.filter(IsDelete=True)
    elif request.user.role == 'OrganizationAdmin':
        forms = Form.objects.filter(IsDelete=True, organization=request.user.organization)
    context = {
        "forms": forms,
    }
    return render(request, "forms/recycle.html", context)


def restore_data(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id)
    form_instance.IsDelete = False
    form_instance.save()
    return redirect('list_forms')


def delete_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    if (request.user == form.user and request.user.role == 'Staff') or request.user.role in ['Organisation_Admin',
                                                                                             'Super_Admin']:
        form.questions.clear()
        form.delete()
        Form_activity.objects.create(form_instance=form, action="deleted", by_user=request.user)
    return redirect('forms/recycle')


def add_player_ques(request, question_id, form_id):
    question_instance = get_object_or_404(Question, id=question_id)
    form = get_object_or_404(Form, id=form_id)
    user = form.user
    players = Player.objects.filter(organization=form.organization)
    if request.method == 'POST':
        player_id = request.POST.get('player_list')
        if request.user.role == 'Staff':
            if request.user == user or request.user.staff.add_result == True:
                if question_instance.input_add_player == False:
                    messages.error(request, 'User is not allowed to add players')
                    return redirect('add_response', id=form.id)
                else:
                    if player_id is not None:
                        player = Player.objects.get(id=player_id)
                        question_instance.player_list.add(player)
                        question_instance.save()
                        return redirect('forms/add_response', form_id=form.id)
        elif request.user.role in ['OrganizationAdmin', 'SuperAdmin']:
            if player_id is not None:
                player = Player.objects.get(id=player_id)
                question_instance.player_list.add(player)
                question_instance.save()
                return redirect('forms/add_response', form_id=form.id)
        else:
            return HttpResponseForbidden(
                "User is not authorised to access this page. This could be due to user doesn't have permission")
    context = {
        "question_instance": question_instance,
        "player_list": players
    }
    print(players)
    return render(request, 'forms/add_player_ques.html', context)


@login_required
def add_response(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id)

    # Retrieve the Player instance for players
    if request.user.role == 'Player':
        try:
            player_instance = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            return HttpResponseForbidden("You are not registered as a Player.")

        # Check if the player is assigned to the form
        if not FormAssignment.objects.filter(form=form_instance, player=player_instance).exists():
            return HttpResponseForbidden("You are not authorized to respond to this form.")

    # Additional logic for other roles (Staff, OrganizationAdmin, etc.)
    elif request.user.role == 'Staff':
        if not request.user.staff.add_result and request.user != form_instance.user:
            return HttpResponseForbidden("You are not authorized to respond to this form.")
    elif request.user.role == 'OrganizationAdmin' and form_instance.organization != request.user.organization:
        return HttpResponseForbidden("You are not authorized to respond to this form.")

    # Fetch the list of players in the same organization
    player_list = Player.objects.filter(organization=form_instance.organization)

    # Handle form submission
    if request.method == 'POST':
        player_id = request.POST.get('player')
        if player_id:
            player = Player.objects.get(id=player_id)
            response_instance = Response.objects.create(form=form_instance, related_player=player)
        else:
            response_instance = Response.objects.create(form=form_instance)

        # Save responses for each question in the form
        for question in form_instance.questions.all():
            answer_text = request.POST.get(f'question_{question.id}', '')
            file_upload = request.FILES.get(f'question_{question.id}')
            if question.question_type == 'file_upload' and file_upload:
                Answer.objects.create(
                    response=response_instance,
                    question=question,
                    file_upload=file_upload
                )
            else:
                Answer.objects.create(
                    response=response_instance,
                    question=question,
                    answer_text=answer_text
                )

        # Log the activity
        Form_activity.objects.create(form_instance=form_instance, action="data_input", by_user=request.user)

        return redirect('form:add_response', form_id=form_instance.id)

    # Fetch existing responses
    existing_responses = Response.objects.filter(form=form_instance).prefetch_related('answers__question')

    return render(request, 'forms/add_response.html', {
        'form_instance': form_instance,
        'existing_responses': existing_responses,
        'players': player_list,
        'user_role': request.user.role  # Pass user role to the template
    })



def delete_response(request, response_id):
    response_instance = get_object_or_404(Response, id=response_id)
    form_instance = response_instance.form
    if request.user.role == 'Player' or (request.user.role == 'Staff' and request.user != form_instance.user):
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission.")
    elif request.user.role == 'OrganizationAdmin' and form_instance.organization != request.user.organization:
        return HttpResponseForbidden(
            "User is not authorised to access this page. This could be due to user doesn't have permission to input data.")
    else:
        response_instance.delete()
        Form_activity.objects.create(form_instance=form_instance, action="input_deleted", by_user=request.user)
        return redirect('forms/list_forms')


def edit_response(request, response_id):
    response_instance = get_object_or_404(Response, id=response_id)
    answers = response_instance.answers.all()
    answer_dict = {}
    for answer in answers:
        if answer.question.question_type in ['multiple_choice']:
            answer_dict[answer.question.id] = answer.answer_text.split(',')
        elif answer.question.question_type in ['multiple_choice_grid']:
            answer_dict[answer.question.id] = answer.answer_text.split(',')
        else:
            answer_dict[answer.question.id] = answer.answer_text
    form_instance = response_instance.form  # Get the related Form instance
    staff = Staff.objects.filter(user=request.user, add_result=True)
    if request.user.role == 'Player':
        return HttpResponseForbidden("User does not have permission to edit the response ")
    elif request.user.role == 'Staff' and (request.user != form_instance.user or staff == None):
        return HttpResponseForbidden("User does not have permission to edit the response ")
    elif request.user.role == 'OrganizationAdmin' and form_instance.organization != request.user.organization:
        return HttpResponseForbidden("User does not have permission to edit the response ")
    if request.method == 'POST':
        # Handle form submission
        for question in form_instance.questions.all():
            if question.question_type == "multiple_choice_grid":
                answers = []
                for player in question.player_list.all():
                    answers.append(f"{player.name}_{request.POST.get(f'question_{player.id}', '')}")
                answer_text = f' ,'.join(answers)
            else:
                answer_text = request.POST.get(f'question_{question.id}', '')
            file_upload = request.FILES.get(f'question_{question.id}')
            answer_instance, created = Answer.objects.get_or_create(
                response=response_instance,
                question=question
            )

            if question.question_type == 'file_upload':
                answer_instance.file_upload = file_upload
            else:
                answer_instance.answer_text = answer_text
            answer_instance.save()
            Form_activity.objects.create(form_instance=form_instance, action="input_updation", by_user=request.user)
        return redirect('form:view_answer', form_id=form_instance.id)

    # Prepare initial data for the form

    return render(request, 'forms/edit_response.html', {
        'form_instance': form_instance,
        'response_instance': response_instance,
        'answers': answer_dict
    })


def send_formlink(request, form_id):
    domain = '127.0.0.1:8000'
    # Generate a unique URL for the form page
    form_url = reverse('form_detail', kwargs={'form_id': form_id})
    full_url = f'http://{domain}{form_url}'
    players = Player.objects.filter(organization=request.user.organization)
    teams = Player_Group.objects.filter(organization=request.user.organization)
    if request.method == 'POST':
        form = SendForm(request.POST)
        recipients = request.POST.getlist('recipient')
        playerlist = []
        players_email = set()
        teamid = []
        for recipient in recipients:
            if recipient.startswith('player_'):
                playerid = int(recipient.split('_')[1])
                playerlist.append(playerid)
            elif recipient.startswith('team_'):
                team_id = int(recipient.split("_")[1])
                teamid.append(team_id)
        player_ins = Player.objects.filter(id__in=playerlist)
        for player in player_ins:
            players_email.add(player.emailid)

        if teamid:
            team_member = Player.objects.filter(team__id__in=teamid)
            for member in team_member:
                players_email.add(member.emailid)
        if form.is_valid():
            ins = form.save(commit=False)
            sender = request.user
            ins.sender = sender
            sender = sender.email
            formins = Form.objects.get(id=form_id)
            ins.form = formins
            ins.save()
            message = f"{request.POST.get('message')}.Open this link to fill out form {full_url}"
            subject = request.POST.get('subject')
            print(request.POST.get('recipient'))
            send_mail(subject=subject, message=message, from_email=sender, recipient_list=list(players_email),
                      fail_silently=False)
            return redirect('list_forms')
        else:
            form = SendForm()
    return render(request, 'communication/sendmail.html', {'players': players, 'teamlist': teams, 'is_email': True})


def whatsapp_message(request, form_id):
    domain = '127.0.0.1:8000'
    form_url = reverse('form_detail', kwargs={'form_id': form_id})
    full_url = f'http://{domain}{form_url}'
    players = Player.objects.all()
    teams = Player_Group.objects.all()
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    if request.method == 'POST':
        form = SendWhatsappForm(request.POST)
        players_number = set()
        id_list = []
        teams_id = []
        receiverlist = request.POST.getlist('recipient')
        for user in receiverlist:
            if user.startswith('player_'):
                player_id = user.split("_")[1]
                id_list.append(player_id)
            elif user.startswith('Team_'):
                team_id = user.split("_")[1]
                teams_id.append(team_id)
        for pid in id_list:
            number = Player.objects.get(id=pid).mobile
            players_number.add(number)
        if teams_id:
            team_mem = Player.objects.filter(team_id_in=teams_id)
            for mem in team_mem:
                players_number.add(mem.mobile)
        print(form.is_valid())
        if form.is_valid:
            message = f"{request.POST.get('message')}. The link is as follow: {full_url}"
            for contact in players_number:
                client.messages.create(body=message, from_=settings.TWILIO_WHATSAPP_NUMBER, to=f'whatsapp:{contact}')
        else:
            form = SendWhatsappForm()
    return render(request, 'communication/sendmail.html', {'players': players, 'teamlist': teams, 'is_email': False})


def downloadExcelFormTemplate(request, form_id):
    form_ins = Form.objects.get(id=form_id)
    staff = Staff.objects.filter(user=request.user)
    formQuestions = form_ins.questions.all()
    columns = ['Sno', 'Player Name', 'Mobile No']
    for ques in formQuestions:
        columns.append(ques)
    df = pd.DataFrame(columns=columns)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename='f"{form_ins.title}.xlsx"''
    df.to_excel(response, index=False)
    return response


def result(file, error_list):
    try:
        data = pd.read_excel(file)
        if 'error' not in data.columns:
            data['error'] = ""
        else:
            data['error'] = data['error'].astype(str)
        for index, row in data.iterrows():
            error = error_list.get(f"{row['Player Name']}")
            if error:
                error = error.values()
                all_error = "".join(error)
                print(all_error)
                data.at[index, 'error'] = all_error
                print(data.head())
                downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                new_file = os.path.join(downloads_folder, "updated_file")
                data.to_excel(new_file, index=False)
            else:
                continue
    except Exception as e:
        print("Error reading Excel file:", e)


def import_excel(request):
    staff = Staff.objects.filter(user=request.user, add_result=True)
    if request.user.role == 'Staff':
        if staff:
            forms = Form.objects.filter(organization=staff.organization)
        else:
            forms = Form.objects.filter(user=request.user)
    elif request.user.role == 'OrganizationAdmin':
        forms = Form.objects.filter(organization=request.user.organization)
    elif request.user.role == 'SuperAdmin':
        forms = Form.objects.all()
    else:
        return HttpResponseForbidden("User does not have permission to import result")
    if request.method == "POST":
        form = mass_importform(request.POST, request.FILES)
        if form.is_valid():
            error_list = {}
            questions = Question.objects.filter(form=request.POST['form_id'])
            file = request.FILES['file_upload']
            try:
                data = pd.read_excel(file)
            except Exception as e:
                print("Error reading Excel file:", e)
                return render(request, 'forms/mass_import.html',
                              {'forms': forms, 'error': 'Failed to read the uploaded file.'})
            form_ins = Form.objects.get(id=request.POST['form_id'])
            for index, row in data.iterrows():
                error = {}
                if row.isnull().all():
                    continue
                else:
                    player = Player.objects.filter(name=row['Player Name'], mobile=str(row['Mobile No'])).first()
                    if player:
                        dup_response = Response.objects.filter(form=form_ins, related_player=player)
                        if len(dup_response) > 0:
                            ins = Question.objects.filter(question_text='Date of Activity').first()
                            ins2 = Question.objects.filter(question_text='Time of Activity performed').first()
                            dup = Answer.objects.filter(response__in=list(dup_response), question=ins,
                                                        answer_text=row['Date of Activity'])
                            dup1 = Answer.objects.filter(response__in=list(dup_response), question=ins2,
                                                         answer_text=row['Time of Activity performed'])
                            if len(dup) == 0 and len(dup1) == 0:
                                res_ins = Response.objects.create(form=form_ins, related_player=player)
                            else:
                                error[row["Player Name"]] = "Player already have responded"
                                error_list[row['Player Name']] = error
                                continue
                        else:
                            res_ins = Response.objects.create(form=form_ins, related_player=player)
                        count = 0
                        for ques in questions:
                            print(ques)
                            try:
                                if not pd.isnull(row[ques.question_text]):
                                    if ques.question_type == "file_upload":
                                        Answer.objects.create(
                                            response=res_ins,
                                            question=ques,
                                            answer_text=row[ques.question_text],
                                            defaults={'file_upload': row[ques.question_text]})
                                        count += 1
                                    elif ques.question_type in ['multiple_choice', 'checkbox', 'dropdown']:
                                        choices = Multiple_choice.objects.filter(question=ques).values_list(
                                            'choice_text', flat=True)
                                        ans = row[ques.question_text]
                                        ans = ans.lower()
                                        if ans in choices:
                                            Answer.objects.create(
                                                response=res_ins,
                                                question=ques,
                                                answer_text=ans)
                                            count += 1
                                        else:
                                            error[
                                                f'Error in answer of {ques.question_text}'] = f"The choice doesn't exist.please input valid choice"
                                    elif ques.question_type in ['date', 'time']:
                                        Answer.objects.create(
                                            response=res_ins,
                                            question=ques,
                                            answer_text=row[ques.question_text])
                                        count += 1
                                    elif ques.question_type in ['multiple_choice_grid']:
                                        continue
                                    else:
                                        Answer.objects.create(
                                            response=res_ins,
                                            question=ques,
                                            answer_text=row[ques.question_text])
                                        count += 1
                                else:
                                    break
                            except KeyError as e:
                                error[
                                    f"KeyError: The key '{e}' was not found in the row"] = " Please check the column name with the question text."
                            except Exception as e:
                                print("Some error occurred:", e)
                        activity_instance = Form_activity.objects.create(form_instance=form_ins, action="data_input")
                        activity_instance.by_user.add(request.user.id)
                    else:
                        error[row['Player Name']] = f"{row['Player Name']} doesn't exist"
                error_list[row['Player Name']] = error
            if error_list:
                result(file, error_list)

    else:
        form = mass_importform()
    return render(request, 'forms/mass_import.html', {'forms': forms})


def submitted_data_excel(request):
    responses = Response.objects.all()
    forms = Form.objects.all()
    sheets = {}
    if len(responses) > 0:
        for form in forms:
            data_set = []
            count = 1
            for ins in responses:
                data = {}
                data['Sno'] = count
                if ins.form.id == form.id:
                    answers = Answer.objects.filter(response=ins)
                    for answer in answers:
                        data[answer.question.question_text] = str(answer.answer_text)
                        data["file_upload"] = answer.file_upload if answer.file_upload else "-"
                    count += 1
                    data_set.append(data)
            sheets[form.title] = pd.DataFrame(data_set)
        date = pd.to_datetime('today').date()
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachement; filename='f"Form{date}.xlsx"''
        with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
            for name, df in sheets.items():
                df.to_excel(writer, sheet_name=name, index=False)
        return response


def form_activity_view(request):
    if request.user.role == 'SuperAdmin':
        form_activity_list = Form_activity.objects.all()
    elif request.user.role == 'OrganizationAdmin':
        form_list = Form.objects.filter(organization=request.user.organization)
        form_activity_list = Form_activity.objects.filter(form_instance__in=list(form_list))
    else:
        return HttpResponseForbidden("User does not have permission to view form activity")
    return render(request, 'forms/form_activity.html', {'activity_list': form_activity_list})


def view_answer(request, form_id):
    form = Form.objects.get(id=form_id)
    if form:
        responselist = Response.objects.filter(form=form).prefetch_related('answers')
        processed_responses = []
        for response in responselist:
            responses = {'response': response, 'answers': []}
            for question in form.questions.all():
                answer = response.answers.filter(question=question).first()
                if answer:
                    if answer.file_upload:
                        responses['answers'].append(answer.file_upload)
                    elif answer.answer_text:
                        responses['answers'].append(answer.answer_text)
                    else:
                        responses['answers'].append('None')
                else:
                    responses['answers'].append('None')
            processed_responses.append(responses)
        return render(request, 'forms/view_answer.html',
                      {'responselist': processed_responses, 'form': form, 'questionlist': form.questions.all()})


def form_input_excel(request, form_id):
    form = Form.objects.get(id=form_id)
    responses = Response.objects.filter(form=form)
    count = 1
    input_data = []
    for ins in responses:
        data = {}
        data['Sno'] = count
        data['Form Title'] = ins.form.title
        data['Response_id'] = ins.id
        answers = Answer.objects.filter(response=ins)
        for answer in answers:
            data[answer.question.question_text] = str(answer.answer_text)
            data["file_upload"] = answer.file_upload if answer.file_upload else "-"
        count += 1
        input_data.append(data)
    df = pd.DataFrame(input_data)
    date = pd.to_datetime('today').date()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachement; filename='f"{form.title}-{date}.xlsx"''
    df.to_excel(response, index=False)
    return response


# --------------------------------------------


# =================================================

def assign_form(request):
    if request.method == "POST":
        form = AssignForm(request.POST)
        if form.is_valid():
            form_instance = form.cleaned_data['form']
            players = form.cleaned_data.get('players', [])
            groups = form.cleaned_data.get('groups', [])

            if not players and not groups:
                messages.error(request, "Please select at least one player or group.")
                return render(request, 'forms/assign_form.html', {'form': form})

            # Assign forms to selected players
            for player in players:
                FormAssignment.objects.create(form=form_instance, player=player)

            # Assign forms to selected groups
            for group in groups:
                FormAssignment.objects.create(form=form_instance, group=group)

            messages.success(request, "Form assigned successfully!")
            return redirect('form:view_assignments')
    else:
        form = AssignForm()

    return render(request, 'forms/assign_form.html', {'form': form})


def view_assignments(request):
    assignments = FormAssignment.objects.all()
    players = Player.objects.all()
    groups = Player_Group.objects.all()
    return render(request, 'forms/view_assignments.html', {
        'assignments': assignments,
        'players': players,
        'groups': groups
    })


def unassign_form(request, assignment_id):
    assignment = get_object_or_404(FormAssignment, id=assignment_id)
    assignment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

