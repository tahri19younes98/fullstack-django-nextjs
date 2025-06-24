from django import forms
from django.shortcuts import render
from django.http import HttpResponse
import qrcode
import io
import base64
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
custom_page_size = (60 * cm, 60 * cm)  # A4 size 
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
import json
import string
import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# ------------------------------------- Forms (still inside views.py)-------------------------------------
class QRForm(forms.Form):
    data = forms.CharField(label='Enter text or URL', max_length=200)
    format = forms.ChoiceField(choices=[
        ('view', 'View'), ('jpeg', 'Download JPEG'),
        ('png', 'Download PNG'), ('pdf', 'Download PDF')], required=False)

class FileQRForm(forms.Form):
    #name = forms.CharField(label="Name", max_length=100)
    file = forms.FileField(label="Upload File")

# ----------------------------------------- generate_qr_image------------------------------------------------
def generate_qr_image(data):
    qr = qrcode.QRCode(
        version=None,  # Let it auto-size based on data
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,  # Controls pixel size of each QR "box"
        border=4,     # Border size (in boxes)
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Resize to 10x10 cm at 300 DPI (~1181x1181 pixels)
    img = img.resize((181, 181), Image.LANCZOS)

    return img
# ----------------------------------------- save_qr_pdf------------------------------------------------
def save_qr_pdf(data,  filename="qr_code.pdf"):
    img = generate_qr_image(data)

    # Convert image to byte stream
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    img_reader = ImageReader(img_byte_arr)

    pdf_buffer = io.BytesIO()
    # Create PDF with A4 page size
    c = canvas.Canvas(pdf_buffer, pagesize=custom_page_size)
    # Draw QR image at (10cm, 10cm) from bottom-left, with 10cm width/height
    c.drawImage(img_reader, x=10*cm, y=10*cm, width=10*cm, height=10*cm)

    c.showPage()
    c.save()

    pdf_buffer.seek(0)
    
    return HttpResponse(
        pdf_buffer.getvalue(),
        content_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )

   
def append_qr_to_pdf(qr_image):
    import os
    import json
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    from reportlab.lib.utils import ImageReader

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    batch_dir = os.path.join(BASE_DIR, 'qrmainpage', 'pdf_batches')
    state_file = os.path.join(batch_dir, 'qr_batch_state.json')
    os.makedirs(batch_dir, exist_ok=True)

    # Load or initialize state
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)
    else:
        state = {"current_batch": 1, "current_index": 0}

    index = state["current_index"]
    batch = state["current_batch"]

    # Prepare folders and paths
    qr_images_dir = os.path.join(batch_dir, f'batch_{batch}_qr_images')
    os.makedirs(qr_images_dir, exist_ok=True)

    qr_path = os.path.join(qr_images_dir, f'{index}.png')
    qr_image.save(qr_path, format='PNG')

    pdf_path = os.path.join(batch_dir, f'qr_batch_{batch}.pdf')
    custom_page_size = (60 * cm, 60 * cm)

    # Redraw all images for this batch
    c = canvas.Canvas(pdf_path, pagesize=custom_page_size)
    for i in range(index + 1):  # includes current QR
        col = i % 10
        row = i // 10
        x = 1 * cm + col * 5 * cm
        y = custom_page_size[1] - (1 * cm + (row + 1) * 5 * cm)
        img_path = os.path.join(qr_images_dir, f'{i}.png')
        if os.path.exists(img_path):
            c.drawImage(img_path, x, y, width=4.5 * cm, height=4.5 * cm)
    c.save()

    # ✅ Update state after drawing
    state["current_index"] += 1
    if state["current_index"] >= 100:
        state["current_batch"] += 1
        state["current_index"] = 0

    with open(state_file, 'w') as f:
        json.dump(state, f)

    return pdf_path






# ------------------------------------------------------- Main view ----------------------------------------------------
def index(request):
    qr_image = None
    qr_form = QRForm()
    file_form = FileQRForm()
    show_add_menu = request.GET.get('menu') == 'add' or request.POST.get('action') == 'upload'
    qr_content = None
    if request.method == 'POST':
        if request.POST.get('action') == 'upload':
            file_form = FileQRForm(request.POST, request.FILES)
            if file_form.is_valid():
                #name = file_form.cleaned_data['name']
                random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                qr_content = f"https://codeitdz.com/{random_code}"
                #img = qrcode.make(qr_content)
                #img = generate_qr_image(qr_content)
               
               # filename = f"qr_menu_{random_code}.pdf"
                img = generate_qr_image(qr_content)  
                pdf_path = append_qr_to_pdf(img)
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                qr_image = base64.b64encode(buf.getvalue()).decode()
               # return save_qr_pdf(qr_content, filename)
               # Render the page with preview + download link
                return render(request, 'qrmainpage/index.html', {
                    'form': qr_form,
                    'file_form': file_form,
                    'qr_image': qr_image,
                    'qr_url': qr_content,
                    'random_code': random_code,
                    #'pdf_filename': filename,
                    'pdf_filename': os.path.basename(pdf_path),
                    'pdf_data': qr_content,
                    'show_add_menu': True
                })
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
                    c = canvas.Canvas(pdf_buf, pagesize=custom_page_size)
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
        'qr_content': qr_content, 
        'show_add_menu': show_add_menu
    })




from django.views.decorators.http import require_GET

@require_GET
def download_pdf(request):
    data = request.GET.get('data')
    filename = request.GET.get('filename', 'qr_code.pdf')

    if not data:
        return HttpResponse("Missing data", status=400)

    return save_qr_pdf(data, filename)