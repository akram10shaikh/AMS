
from django.urls import path
from django.shortcuts import redirect
from accounts import views
from accounts.views import  staff_dashboard

urlpatterns = [
    path('', lambda request: redirect('main_login')),  # Redirect root URL to login
    path('main_login/', views.main_login, name='main_login'),
    path('login/', views.super_admin_login, name='super_admin_login'),
    path('dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('', views.homepage, name='homepage'),
    path('add-staff/', views.staff_register, name='add_staff'),
    path('player_dashboard/', views.player_dashboard, name='player_dashboard'),
    path('organization/add/', views.organization_register, name='add_organization'),
    path('organization/login/', views.organization_login, name='organization_login'),
    path('organization/dashboard/', views.organization_dashboard, name='organization_dashboard'),
    path('dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('player_login/', views.player_login, name='player_login'),
    path('organizations_list', views.organization_list, name='organization_list'),
    path('edit/<int:pk>/', views.edit_organization, name='edit_organization'),
    path('delete/<int:pk>/', views.delete_organization, name='delete_organization'),

    path('staff_register/', views.staff_register, name='staff_register'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/<int:staff_id>/edit/', views.staff_edit, name='staff_edit'),
    path('staff/<int:staff_id>/update/', views.staff_update, name='staff_update'),
    path('staff/<int:staff_id>/delete/', views.staff_delete, name='staff_delete'),
    path('add_result', views.add_result, name='add_result'),
    path('view_result', views.add_result, name='view_result'),

   
    path('staff_org_register/', views.staff_register_org, name='staff_register_org'),
    path('staff_org/', views.staff_list_org, name='staff_list_org'),
    path('staff_org/dashboard/', views.staff_dashboard_org, name='staff_dashboard_org'),
    
    path('logout/', views.custom_logout, name='logout'),



]