from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_pdf_from_cv(cv):
    """
    Takes a CV object and renders it into a PDF.
    """
    template = get_template('cvbuilder/pdf_template.html')
    html = template.render({'cv': cv})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
    if not pdf.err:
        return result.getvalue()
    return None
