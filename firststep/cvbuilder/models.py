from django.db import models
from django.conf import settings
from django.utils import timezone

from accounts.models import User

TEMPLATE_CHOICES = [
    ('classic', 'Classic'),
    ('modern', 'Modern'),
    ('creative', 'Creative'),
]

class CV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    profile_summary = models.TextField(blank=True)
    experience_details = models.TextField(blank=True)
    education_details = models.TextField(blank=True)
    skills_list = models.TextField(blank=True)
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='classic')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class CVTemplate(models.Model):
    name = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='templates/previews/', null=True, blank=True)
    file_reference = models.CharField(max_length=255)  # used to load the correct HTML/PDF layout

    def __str__(self):
        return self.name

class CVSection(models.Model):
    SECTION_TYPES = [
        ('personal_info', 'Personal Info'),
        ('summary', 'Profile Summary'),
        ('experience', 'Work Experience'),
        ('education', 'Education'),
        ('skills', 'Skills'),
        ('projects', 'Projects'),
        ('certifications', 'Certifications'),
        ('languages', 'Languages'),
        ('references', 'References'),
    ]

    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.section_type} in {self.cv.title}"

class CVEntry(models.Model):
    section = models.ForeignKey(CVSection, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class CVVersion(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='versions')
    data_snapshot = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Version at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
