from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User, UserSettings, ActivityLog

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('firstname', 'lastname', 'profile_photo', 'created_at', 'updated_at')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(UserSettings)
admin.site.register(ActivityLog)
