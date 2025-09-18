from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Entity, Incident, Report



class UserAdmin(BaseUserAdmin):
    model = User


    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'clearance_level',
        'role',
        'avatar_tag',  
        'is_staff',
        'is_active',
    )
    list_filter = ('is_staff', 'is_active', 'clearance_level', 'role')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('username',)


    fieldsets = BaseUserAdmin.fieldsets + (
        ("Anomaly Control Info", {"fields": ("clearance_level", "role", "avatar")}),
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
                'avatar',  
                'is_staff',
                'is_active',
            ),
        }),
    )


    readonly_fields = ('avatar_tag',)


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
