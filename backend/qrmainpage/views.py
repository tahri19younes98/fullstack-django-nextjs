from django import forms
from django.shortcuts import render
from django.http import HttpResponse
import qrcode
import io
import base64
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import json

from django.http import JsonResponse


# --- Forms (still inside views.py)
class QRForm(forms.Form):
    data = forms.CharField(label='Enter text or URL', max_length=200)
    format = forms.ChoiceField(choices=[
        ('view', 'View'), ('jpeg', 'Download JPEG'),
        ('png', 'Download PNG'), ('pdf', 'Download PDF')], required=False)

class FileQRForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    file = forms.FileField(label="Upload File")


# --- Main view
def index(request):
    qr_image = None
    qr_form = QRForm()
    file_form = FileQRForm()
    show_add_menu = request.GET.get('menu') == 'add' or request.POST.get('action') == 'upload'

    if request.method == 'POST':
        if request.POST.get('action') == 'upload':
            file_form = FileQRForm(request.POST, request.FILES)
            if file_form.is_valid():
                name = file_form.cleaned_data['name']
                qr_content = f"https://codeitdz.com/{name}"
                img = qrcode.make(qr_content)
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                qr_image = base64.b64encode(buf.getvalue()).decode()
        else:
            qr_form = QRForm(request.POST)
            if qr_form.is_valid():
                data = qr_form.cleaned_data['data']
                action = qr_form.cleaned_data.get('format', 'view')

                qr = qrcode.make(data)
                buf = io.BytesIO()
                qr.save(buf, format='PNG')
                qr_data = buf.getvalue()

                if action == 'png':
                    return HttpResponse(qr_data, content_type='image/png',
                        headers={'Content-Disposition': 'attachment; filename="qr_code.png"'})
                elif action == 'jpeg':
                    png_buf = io.BytesIO(qr_data)
                    img = Image.open(png_buf).convert('RGB')
                    jpeg_buf = io.BytesIO()
                    img.save(jpeg_buf, format='JPEG')
                    return HttpResponse(jpeg_buf.getvalue(), content_type='image/jpeg',
                        headers={'Content-Disposition': 'attachment; filename="qr_code.jpeg"'})
                elif action == 'pdf':
                    pdf_buf = io.BytesIO()
                    c = canvas.Canvas(pdf_buf, pagesize=letter)
                    image = ImageReader(io.BytesIO(qr_data))
                    c.drawImage(image, 100, 500, width=200, height=200)
                    c.showPage()
                    c.save()
                    pdf_buf.seek(0)
                    return HttpResponse(pdf_buf.getvalue(), content_type='application/pdf',
                        headers={'Content-Disposition': 'attachment; filename="qr_code.pdf"'})
                else:
                    buf.seek(0)
                    qr_image = base64.b64encode(buf.getvalue()).decode()

    return render(request, 'qrmainpage/index.html', {
        'form': qr_form,
        'file_form': file_form,
        'qr_image': qr_image,
        'show_add_menu': show_add_menu
    })




