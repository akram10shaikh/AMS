from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser, Staff, Organization

class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Ensure is_super_admin is correctly set based on role
        if obj.role == 'SuperAdmin':
            obj.is_super_admin = True
        else:
            obj.is_super_admin = False
        super().save_model(request, obj, form, change)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone_number', 'address')
    search_fields = ('name', 'phone_number')


class StaffAdmin(UserAdmin):
    list_display = ('name', 'email', 'mobile_number', 'organization', 'designation', 'is_staff')
    search_fields = ('email', 'name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'age', 'mobile_number', 'designation', 'organization')}),
        ('Modules', {'fields': ('modules',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'name', 'age', 'mobile_number', 'designation', 'organization', 'password1', 'password2', 'modules',
            'is_staff')
        }),
    )

    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions', 'modules')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'organization', 'player_management', 'injury_tracking')

