from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import CV
from .forms import CVForm, AssistantCVForm, UploadCVForm  # Forms we'll create now
from .utils import extract_cv_data  # Extraction logic we'll make
from .pdf_utils import render_pdf_from_cv  # PDF export logic

# 1. Choose how to create CV
@login_required
def cv_start(request):
    return render(request, 'cvbuilder/cv_start.html')

# 2. Manual creation
@login_required
def cv_create_manual(request):
    if request.method == 'POST':
        form = CVForm(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()
            return redirect('cv_preview', pk=cv.pk)
    else:
        form = CVForm()
    return render(request, 'cvbuilder/cv_form.html', {'form': form, 'form_title': 'Create CV Manually'})

# 3. Upload CV (PDF/DOC)
@login_required
def cv_upload(request):
    if request.method == 'POST':
        form = UploadCVForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['cv_file']
            data = extract_cv_data(file)

            cv = CV.objects.create(
                user=request.user,
                full_name=data.get('full_name', ''),
                profession=data.get('profession', ''),
                profile_summary=data.get('profile_summary', ''),
                experience_details=data.get('experience_details', ''),
                education_details=data.get('education_details', ''),
                skills_list=data.get('skills_list', ''),
            )
            return redirect('cv_preview', pk=cv.pk)
    else:
        form = UploadCVForm()
    return render(request, 'cvbuilder/cv_upload.html', {'form': form})

# 4. Assistant guided creation
@login_required
def cv_assistant(request):
    if request.method == 'POST':
        form = AssistantCVForm(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = request.user
            cv.save()
            return redirect('cv_preview', pk=cv.pk)
    else:
        form = AssistantCVForm()
    return render(request, 'cvbuilder/cv_assistant.html', {'form': form})

# 5. Edit existing CV
@login_required
def cv_edit(request, pk):
    cv = get_object_or_404(CV, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CVForm(request.POST, instance=cv)
        if form.is_valid():
            form.save()
            return redirect('cv_preview', pk=cv.pk)
    else:
        form = CVForm(instance=cv)
    return render(request, 'cvbuilder/cv_form.html', {'form': form, 'form_title': 'Edit CV'})

# 6. Preview CV
@login_required
def cv_preview(request, pk):
    cv = get_object_or_404(CV, pk=pk, user=request.user)
    return render(request, 'cvbuilder/cv_preview.html', {'cv': cv})

# 7. Export to PDF
@login_required
def cv_export_pdf(request, pk):
    cv = get_object_or_404(CV, pk=pk, user=request.user)
    pdf = render_pdf_from_cv(cv)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CV_{cv.full_name}.pdf"'
    return response
class CVDeleteView(DeleteView):
    model = CV
    template_name = 'cvbuilder/cv_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "CV deleted successfully!")
        return super().delete(request, *args, **kwargs)
    
class TemplateSelectionView(UpdateView):
    model = CV
    fields = ['template']
    template_name = 'cvbuilder/template_selection.html'

    def get_success_url(self):
        return reverse_lazy('cv_edit', kwargs={'pk': self.object.pk})
    
    

def select_template_view(request):
    templates = [
        {"name": "Modern", "image": "/static/cvbuilder/images/modern_preview.png"},
        {"name": "Classic", "image": "/static/cvbuilder/images/classic_preview.png"},
        {"name": "Creative", "image": "/static/cvbuilder/images/creative_preview.png"},
    ]
    context = {"templates": templates}
    return render(request, "cvbuilder/select_template.html", context)