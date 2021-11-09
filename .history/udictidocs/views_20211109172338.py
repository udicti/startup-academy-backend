from django.shortcuts import render
from applications.models import *

# Create your views here.


from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML

def selected_applicants_pdf_view(request):
    all = Applicant.objects.filter(application_window = ApplicationWindow.objects.filter(id=1).first()).filter(is_selected=True).all()

    html_string = render_to_string('pdf_templates/selected_applicants.html', {'all': all})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response

def new_applicants_pdf_view(request):
    all = Applicant.objects.filter(application_window = ApplicationWindow.objects.filter(id=1).first()).filter(is_selected=True).all()

    html_string = render_to_string('pdf_templates/selected_applicants.html', {'all': all})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/mypdf.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

    return response
