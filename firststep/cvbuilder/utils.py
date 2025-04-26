import docx
import PyPDF2

def extract_cv_data(file):
    """
    Extracts simple CV data from uploaded DOCX or PDF file.
    For now, it just does very basic parsing.
    In future, we can use AI or better NLP models.
    """
    data = {
        'full_name': '',
        'profession': '',
        'profile_summary': '',
        'experience_details': '',
        'education_details': '',
        'skills_list': '',
    }

    try:
        if file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        elif file.name.endswith('.docx'):
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            return data  # Unsupported file type

        # Very simple extraction logic (improve later)
        lines = text.splitlines()
        if lines:
            data['full_name'] = lines[0]  # Assume name is first line
        if len(lines) > 1:
            data['profession'] = lines[1]  # Assume profession second

        data['profile_summary'] = "\n".join(lines[2:5]) if len(lines) > 4 else ''
        data['experience_details'] = "\n".join(lines[5:10]) if len(lines) > 9 else ''
        data['education_details'] = "\n".join(lines[10:15]) if len(lines) > 14 else ''
        data['skills_list'] = "\n".join(lines[15:20]) if len(lines) > 19 else ''

    except Exception as e:
        print(f"Error extracting CV data: {e}")

    return data
