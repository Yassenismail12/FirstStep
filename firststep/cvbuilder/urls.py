from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from cvbuilder.api.views import (
    CVViewSet,
    CVSectionViewSet,
    CVEntryViewSet,
    CVTemplateViewSet,
    CVVersionViewSet,
)

router = DefaultRouter()
router.register('cvs', CVViewSet, basename='cv')
router.register('sections', CVSectionViewSet, basename='cvsection')
router.register('entries', CVEntryViewSet, basename='cventry')
router.register('templates', CVTemplateViewSet, basename='cvtemplate')
router.register('versions', CVVersionViewSet, basename='cvversion')

urlpatterns = [
    path('', include(router.urls)),
    path('start/', cv_start, name='cv_start'),
    path('create/manual/', cv_create_manual, name='cv_create_manual'),
    path('upload/', cv_upload, name='cv_upload'),
    path('assistant/', cv_assistant, name='cv_assistant'),
    path('<int:pk>/edit/', cv_edit, name='cv_edit'),
    path('<int:pk>/preview/', cv_preview, name='cv_preview'),
    path('<int:pk>/export/', cv_export_pdf, name='cv_export_pdf'),
    path('cv/<int:pk>/delete/', CVDeleteView.as_view(), name='cv_delete'),
    path('cv/<int:pk>/choose-template/', TemplateSelectionView.as_view(), name='cv_choose_template'),
    path('select-template/', select_template_view, name='select_template'),
]
