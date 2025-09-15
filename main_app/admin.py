from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Entity, Incident, Report

# Customize the User admin

class UserAdmin(BaseUserAdmin):
    model = User

    # Show fields in the list view, including avatar preview
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'clearance_level',
        'role',
        'avatar_tag',  # preview avatar
        'is_staff',
        'is_active',
    )
    list_filter = ('is_staff', 'is_active', 'clearance_level', 'role')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('username',)

    # Extend the default fieldsets (edit user)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Anomaly Control Info", {"fields": ("clearance_level", "role", "avatar")}),
    )

    # Extend the default add_fieldsets (create user)
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
                'avatar',  # allow avatar upload
                'is_staff',
                'is_active',
            ),
        }),
    )

    # Make avatar read-only in admin list/detail
    readonly_fields = ('avatar_tag',)

    # Function to display avatar in admin list/detail view
    def avatar_tag(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.avatar.url)
        return "-"
    avatar_tag.short_description = 'Avatar'





# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Entity)
admin.site.register(Incident)
admin.site.register(Report)
