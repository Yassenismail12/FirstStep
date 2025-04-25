# serializers.py
from rest_framework import serializers
from cvbuilder.models import Resume, CVTemplate, CVVersion, CVSection, CVDesign, CustomField

class CVTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVTemplate
        fields = '__all__'

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ('user', 'current_version', 'created_at', 'updated_at')

class CVVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVVersion
        fields = '__all__'
        read_only_fields = ('created_at',)

class CVSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVSection
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class CVDesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVDesign
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
