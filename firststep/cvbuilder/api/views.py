from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
import io
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.conf import settings
from reportlab.pdfgen import canvas
from django.core.files.storage import default_storage
import fitz  # PyMuPDF
import docx
import os
from cvbuilder.models import CV, CVSection, CVEntry, CVTemplate, CVVersion
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from cvbuilder.api.serializers import (
    CVSerializer,
    CVSectionSerializer,
    CVEntrySerializer,
    CVTemplateSerializer,
    CVVersionSerializer,
)

class CVViewSet(viewsets.ModelViewSet):
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CV.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def save_version(self, request, pk=None):
        cv = self.get_object()
        serializer = self.get_serializer(cv)
        CVVersion.objects.create(cv=cv, data_snapshot=serializer.data)
        return Response({'status': 'version saved'})

    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        cv = self.get_object()
        versions = CVVersion.objects.filter(cv=cv)
        return Response(CVVersionSerializer(versions, many=True).data)


class CVTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CVTemplate.objects.all()
    serializer_class = CVTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CVSectionViewSet(viewsets.ModelViewSet):
    serializer_class = CVSectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CVSection.objects.filter(cv__user=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def reorder(self, request, pk=None):
        section = self.get_object()
        section.order = request.data.get('order', section.order)
        section.save()
        return Response({'status': 'reordered'})


class CVEntryViewSet(viewsets.ModelViewSet):
    serializer_class = CVEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CVEntry.objects.filter(section__cv__user=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def reorder(self, request, pk=None):
        entry = self.get_object()
        entry.order = request.data.get('order', entry.order)
        entry.save()
        return Response({'status': 'reordered'})


class CVVersionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CVVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CVVersion.objects.filter(cv__user=self.request.user)

class UploadCVExtractView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file uploaded."}, status=400)

        ext = os.path.splitext(file_obj.name)[-1].lower()
        content = ""

        path = default_storage.save(f"temp/{file_obj.name}", file_obj)
        file_path = os.path.join(default_storage.location, path)

        try:
            if ext == ".pdf":
                doc = fitz.open(file_path)
                for page in doc:
                    content += page.get_text()
            elif ext in [".doc", ".docx"]:
                doc = docx.Document(file_path)
                content = "\n".join([p.text for p in doc.paragraphs])
            else:
                return Response({"error": "Unsupported file format."}, status=400)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

        return Response({"extracted_text": content})
    

@api_view(['POST'])
def assistant_create_cv(request):
    user = request.user
    data = request.data

    cv = CV.objects.create(
        user=user,
        title=data.get('title', 'CV Assistant Draft'),
        description=data.get('description', ''),
        is_draft=True
    )

    for section_type, entries in data.get('sections', {}).items():
        section = CVSection.objects.create(cv=cv, section_type=section_type)
        for entry in entries:
            CVEntry.objects.create(
                section=section,
                title=entry.get('title'),
                subtitle=entry.get('subtitle'),
                description=entry.get('description'),
                start_date=entry.get('start_date'),
                end_date=entry.get('end_date'),
                location=entry.get('location'),
            )

    return Response(CVSerializer(cv).data, status=201)



class ExportCVPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        cv = CV.objects.get(pk=pk, user=request.user)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"CV: {cv.title}")
        p.drawString(100, 780, f"Description: {cv.description}")
        p.drawString(100, 760, "Generated PDF (simple preview)")
        p.showPage()
        p.save()

        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')