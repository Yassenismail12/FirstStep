from django.contrib import admin
from .models import (
    Account, UserSettings, Resume, CVImage, CVSection, CVVersion,
    CustomField, CVDesign, CVTemplate, ActivityLog
)

admin.site.register(Account)
admin.site.register(UserSettings)
admin.site.register(Resume)
admin.site.register(CVImage)
admin.site.register(CVSection)
admin.site.register(CVVersion)
admin.site.register(CustomField)
admin.site.register(CVDesign)
admin.site.register(CVTemplate)
admin.site.register(ActivityLog)
