from django.db import models
from django.utils import timezone
from accounts.models import *

class CVTemplate(models.Model):
    """
    Predefined CV templates
    """
    name = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='template_previews/')
    template_data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Resume(models.Model):
    """
    Main CV/Resume model
    """
    SHARING_STATUS_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
        ('link', 'Shareable Link'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    template = models.ForeignKey(CVTemplate, on_delete=models.PROTECT)
    is_custom_design = models.BooleanField(default=False)
    sharing_status = models.CharField(max_length=50, choices=SHARING_STATUS_CHOICES, default='private')
    share_token = models.CharField(max_length=100, blank=True, null=True)
    pdf_path = models.URLField(blank=True, null=True)
    current_version = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume #{self.id} for {self.user.username}"

class CVVersion(models.Model):
    """
    Version history of CV changes
    """
    cv = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('cv', 'version_number')
        ordering = ['-version_number']

    def __str__(self):
        return f"Version {self.version_number} of CV #{self.cv.id}"

class CVSection(models.Model):
    """
    Sections within a CV (Education, Experience, etc.)
    """
    SECTION_TYPE_CHOICES = [
        ('personal', 'Personal Information'),
        ('education', 'Education'),
        ('experience', 'Work Experience'),
        ('skills', 'Skills'),
        ('projects', 'Projects'),
        ('custom', 'Custom Section'),
    ]

    cv = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=50, choices=SECTION_TYPE_CHOICES)
    display_order = models.IntegerField()
    data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.get_section_type_display()} section for CV #{self.cv.id}"

class CVDesign(models.Model):
    """
    Custom design settings for a CV
    """
    cv = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='design')
    design_data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Design for CV #{self.cv.id}"

class CustomField(models.Model):
    """
    Additional custom fields for CV sections
    """
    cv = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='custom_fields')
    field_name = models.CharField(max_length=100)
    field_value = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Custom field '{self.field_name}' for CV #{self.cv.id}"
