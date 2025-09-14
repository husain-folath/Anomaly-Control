from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Entity, Incident, Report


# Customize the User admin
class UserAdmin(BaseUserAdmin):
    model = User

    # Show more fields in the list view
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'clearance_level',
        'role',
        'is_staff',
        'is_active',
    )
    list_filter = ('is_staff', 'is_active', 'clearance_level', 'role')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('username',)

    # Extend the default fieldsets instead of replacing them
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Anomaly Control Info", {"fields": ("clearance_level", "role")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'clearance_level',
                'role',
                'is_staff',
                'is_active',
            ),
        }),
    )


# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Entity)
admin.site.register(Incident)
admin.site.register(Report)
