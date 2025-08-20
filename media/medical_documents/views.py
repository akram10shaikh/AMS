from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model, login, authenticate, logout # Import to use the custom user model
from django.contrib import messages
from accounts.models import Organization, Staff, CustomUser
from player_app.models import Player
from accounts.forms import OrganizationRegistrationForm, OrganizationLoginForm, OrganizationForm, LoginForm, StaffForm, StaffRegistrationForm, UserForm
from django.db import IntegrityError
from django.urls import reverse



def main_login(request):
    return render(request, 'login_all.html')

def custom_logout(request):
    logout(request)  # This logs the user out
    return render(request, 'login_all.html')

def super_admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role == 'SuperAdmin':  # Check if user has SuperAdmin role
                login(request, user)
                return redirect('super_admin_dashboard')
            else:
                return HttpResponse("You are not authorized as Super Admin")
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'super_admin_login.html')

# Super Admin Dashboard view (protected)
@login_required
def super_admin_dashboard(request):
    selected_org_id = request.GET.get('organization')  # Get selected organization from dropdown
    organizations = Organization.objects.all()  # Get all organizations
    selected_org = Organization.objects.filter(id=selected_org_id).first() if selected_org_id else None  # Get selected org object


    players = []
    staff_members = []

    if selected_org_id:
        players = Player.objects.filter(organization_id=selected_org_id)  # Filter players
        staff_members = Staff.objects.filter(organization_id=selected_org_id)  # Filter staff

    return render(request, 'super_admin_dashboard.html', {
        'organizations': organizations,
        'players': players,
        'staff_members': staff_members,
        'selected_org_id': int(selected_org_id) if selected_org_id else None
    })


def add_organization(request):
    return render(request, 'add_organization.html')
def add_result(request):
    return render(request, 'add_result.html')
def view_result(request):
    return render(request, 'view_result.html')

def homepage(request):
    return render(request, 'homepage.html')
def add_staff(request):
    return render(request, 'add_staff.html')

def organization_register(request):
    if request.method == 'POST':
        form = OrganizationRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization add successfully. Please log in.')
            return redirect('organization_list')
    else:
        form = OrganizationRegistrationForm()
    return render(request, 'organization_register.html', {'form': form})


def organization_login(request):
    if request.method == 'POST':
        form = OrganizationLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == 'OrganizationAdmin':
                login(request, user)
                return redirect('organization_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = OrganizationLoginForm()
    return render(request, 'organization_login.html', {'form': form})

@login_required
def organization_dashboard(request):
    # organization = request.user.organization  # Assuming the user has a related Organization
    return render(request, 'organization_dashboard.html')



@login_required
def player_dashboard(request):
    return render(request, 'player_dashboard.html')



# Get the custom user model
CustomUser = get_user_model()


def add_staff_view(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)

        if form.is_valid():
            try:
                # Create a new user using the custom user model
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['email'],  # or another unique field
                    password='defaultpassword123',  # Use a default password or generate one
                    role="Staff"
                )
                # Save the staff data with the newly created user
                staff = form.save(commit=False)
                staff.user = user
                staff.organization = form.cleaned_data['organization']  # Set the organization
                staff.save()

                return redirect('staff_list')  # Redirect to staff list or another page

            except IntegrityError as e:
                form.add_error(None, "An error occurred while creating staff: " + str(e))
    else:
        form = StaffForm()

    return render(request, 'add_staff.html', {'form': form})



def staff_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Attempt to authenticate the staff user
            staff = authenticate(request, email=email, password=password)
            if staff is not None:
                login(request, staff)
                return redirect('staff_dashboard')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'staff_login.html', {'form': form})





def organization_list(request):
    organizations = Organization.objects.all()
    return render(request, 'organization_list.html', {'organizations': organizations})

def edit_organization(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    form = OrganizationForm(instance=organization)
    return render(request, 'edit_organization.html', {'form': form, 'organization': organization})

def delete_organization(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    organization.delete()
    return redirect('organization_list')


from django.contrib.auth.decorators import login_required

@login_required
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')


# views.py
from django.http import JsonResponse


# Staff list view
def staff_list(request):
    staff_members = Staff.objects.all()
    organizations = Organization.objects.all()
    return render(request, 'staff_list.html', {'staff_members': staff_members, 'organizations': organizations})

# Edit view to fetch staff data for the modal
def staff_edit(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    data = {
        'id': staff.id,
        'name': staff.name,
        'age': staff.age,
        'mobile_number': staff.mobile_number,
        'email': staff.email,
        'address': staff.address,
        'organization': staff.organization.id,
        'player_management': staff.player_management,
        'injury_tracking': staff.injury_tracking,
        'add_form': staff.add_form,
        'add_result': staff.add_result,
        'view_result': staff.view_result
    }
    return JsonResponse(data)

# Update view to handle staff updates
def staff_update(request, staff_id):
    if request.method == 'POST':
        staff = get_object_or_404(Staff, id=staff_id)
        staff.name = request.POST.get('name')
        staff.age = request.POST.get('age')
        staff.mobile_number = request.POST.get('mobile_number')
        staff.email = request.POST.get('email')
        staff.address = request.POST.get('address')
        staff.organization = request.POST.get('organization')  # Set organization
        staff.player_management = request.POST.get('player_management') == 'true'
        staff.injury_tracking = request.POST.get('injury_tracking') == 'true'
        staff.add_form = request.POST.get('add_form') == 'true'
        staff.add_result = request.POST.get('add_result') == 'true'
        staff.view_result = request.POST.get('view_result') == 'true'
        staff.save()
        return JsonResponse({'success': True})

# Delete view to handle staff deletion
def staff_delete(request, staff_id):
    if request.method == 'POST':
        staff = get_object_or_404(Staff, id=staff_id)
        staff.delete()
        return JsonResponse({'success': True})



def staff_register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        staff_form = StaffRegistrationForm(request.POST)

        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()

            messages.success(request, "Staff registration successful!")
            return redirect('staff_list')  # Redirect to login page after registration
    else:
        user_form = UserForm()
        staff_form = StaffRegistrationForm()

    return render(request, 'staff_register.html', {
        'user_form': user_form,
        'staff_form': staff_form,
    })


def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role =='Staff':
            login(request, user)
            return redirect('staff_dashboard')  # Redirect to dashboard on successful login
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'staff_login.html')

def player_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Try to get the user by email
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            user = None

        if user:
            # Authenticate user
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                # Successfully authenticated
                if hasattr(user, 'player'):
                    login(request, user)
                    return redirect('player_home', pk=user.player.pk)
                else:
                    messages.error(request, "You do not have access to the player dashboard.")
                    return render(request, 'player_login.html')
            else:
                # Incorrect password
                messages.error(request, "Invalid password. Please try again.")
                return render(request, 'player_login.html')

        else:
            # User not found with the given email
            messages.error(request, "No account found with this email address.")
            return render(request, 'player_login.html')

    return render(request, 'player_login.html')