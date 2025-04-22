from FirstStep.accounts.models import *
from FirstStep.resume.models import *  # Import all models from resume
from rest_framework import serializers
from FirstStep.resume.models import CVDesign  # Explicitly import CVDesign

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password']  # hide hash

class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

class CVTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVTemplate
        fields = '__all__'

class CVSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVSection
        fields = '__all__'

class CVImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVImage
        fields = '__all__'

class CVVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVVersion
        fields = '__all__'

class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = '__all__'

class CVDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVDesign
        fields = '__all__'

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'
