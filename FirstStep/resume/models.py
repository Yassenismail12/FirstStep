from django.db import models
from accounts.models import Account

class CVTemplate(models.Model):
    name = models.CharField(max_length=100)
    preview_image = models.URLField()
    template_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Resume(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    template = models.ForeignKey(CVTemplate, on_delete=models.SET_NULL, null=True)
    is_custom_design = models.BooleanField(default=False)
    sharing_status = models.CharField(max_length=100)
    share_token = models.CharField(max_length=100)
    pdf_path = models.URLField(blank=True, null=True)
    current_version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume for {self.user.username}"

class CVVersion(models.Model):
    cv = models.ForeignKey(Resume, on_delete=models.CASCADE)
    version_number = models.IntegerField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.version_number} of {self.cv}"

class CVSection(models.Model):
    cv = models.ForeignKey(Resume, on_delete=models.CASCADE)
    section_type = models.CharField(max_length=50)
    display_order = models.IntegerField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.section_type} for {self.cv}"

class CVImage(models.Model):
    cv = models.ForeignKey(Resume, on_delete=models.CASCADE)
    image_url = models.URLField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.cv}"

class CustomField(models.Model):
    cv = models.ForeignKey(Resume, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    field_value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.field_name} for {self.cv}"

class CVDesign(models.Model):
    cv = models.ForeignKey(Resume, on_delete=models.CASCADE)
    design_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Design for {self.cv}"
