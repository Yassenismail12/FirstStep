from rest_framework import serializers
from cvbuilder.models import CV, CVSection, CVEntry, CVTemplate, CVVersion
from accounts.models import User

class CVEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CVEntry
        fields = ['id', 'title', 'subtitle', 'description', 'start_date', 'end_date', 'location', 'order']

class CVSectionSerializer(serializers.ModelSerializer):
    entries = CVEntrySerializer(many=True, required=False)

    class Meta:
        model = CVSection
        fields = ['id', 'section_type', 'order', 'entries']

    def create(self, validated_data):
        entries_data = validated_data.pop('entries', [])
        section = CVSection.objects.create(**validated_data)
        for entry_data in entries_data:
            CVEntry.objects.create(section=section, **entry_data)
        return section

    def update(self, instance, validated_data):
        entries_data = validated_data.pop('entries', [])
        instance.section_type = validated_data.get('section_type', instance.section_type)
        instance.order = validated_data.get('order', instance.order)
        instance.save()

        # Optional: you can add logic to update entries if needed
        return instance

class CVTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVTemplate
        fields = ['id', 'name', 'preview_image', 'file_reference']

class CVSerializer(serializers.ModelSerializer):
    sections = CVSectionSerializer(many=True, required=False)
    template = CVTemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(
        queryset=CVTemplate.objects.all(), source='template', write_only=True, required=False
    )

    class Meta:
        model = CV
        fields = '__all__'
        read_only_fields = ('user',)
        
    def create(self, validated_data):
        sections_data = validated_data.pop('sections', [])
        cv = CV.objects.create(**validated_data)
        for section_data in sections_data:
            entries_data = section_data.pop('entries', [])
            section = CVSection.objects.create(cv=cv, **section_data)
            for entry_data in entries_data:
                CVEntry.objects.create(section=section, **entry_data)
        return cv

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.template = validated_data.get('template', instance.template)
        instance.is_draft = validated_data.get('is_draft', instance.is_draft)
        instance.save()
        return instance

class CVVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVVersion
        fields = ['id', 'cv', 'data_snapshot', 'created_at']
