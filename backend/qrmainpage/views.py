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
import re
from .models import Restaurant, RestaurantImage
from .serializers import RestaurantSerializer  # Add this import if you have a serializers.py file
custom_page_size = (60 * cm, 60 * cm)  # A4 size 
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
import json
import string
import random
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
import shutil


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
def save_qr_pdf(data, output_path):
    from io import BytesIO
    import qrcode
    from PIL import Image
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm

    # Generate QR image
    qr = qrcode.make(data)
    img = qr.convert("RGB")
    img = img.resize((300, 300), Image.LANCZOS)
    image_reader = ImageReader(img)

    # Create PDF and save
    c = canvas.Canvas(output_path, pagesize=custom_page_size)

    # QR placement
    x = 10 * cm
    y = 10 * cm
    c.drawImage(image_reader, x, y, width=10 * cm, height=10 * cm)

    # Add "Scan Me" centered below QR code
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(x + 5 * cm, y - 1 * cm, "Scan Me")

    c.showPage()
    c.save()


# ----------------------------------------- append_qr_to_pdf------------------------------------------------
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


#-----------------------------------------------------Formulaire view---------------------------------------------------
def restaurant_qr_view(request):
    qr_image = None
    qr_content = None
    saved_paths = [] 
    pdf_url = None  
    qr_url = None


    if request.method == 'POST':
        name = request.POST.get('name')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        tiktok = request.POST.get('tiktok')
        phones = request.POST.getlist('phone[]')
        phones = [p.strip() for p in phones if p.strip()]  # Clean up empty fields

       
        uploaded_images = request.FILES.getlist('images')

        if len(uploaded_images) > 15:
         return HttpResponse("Too many images (max 15 allowed).", status=400)

        data = {
            'name': name,
            'facebook': facebook,
            'instagram': instagram,
            'tiktok': tiktok,
            "phone1": phones[0] if len(phones) > 0 else "",
            "phone2": phones[1] if len(phones) > 1 else "",
            "phone3": phones[2] if len(phones) > 2 else "",
        }

        serializer = RestaurantSerializer(data=data)
        if serializer.is_valid():
             restaurant = serializer.save()

              # Print restaurant details to console
             print("\n" + "="*50)
             print("✅ RESTAURANT CREATED SUCCESSFULLY")
             print("="*50)
             print(f"ID: {restaurant.id}")
             print(f"Name: {restaurant.name}")
             print(f"Facebook: {restaurant.facebook}")
             print(f"Instagram: {restaurant.instagram}")
             print(f"TikTok: {restaurant.tiktok}")
             print(f"Phone 1: {restaurant.phone1}")
             print(f"Phone 2: {restaurant.phone2}")
             print(f"Phone 3: {restaurant.phone3}")
             print("-"*50 + "\n")

        else:
            return HttpResponse("Invalid data", status=400)

        image_dir = os.path.join(settings.MEDIA_ROOT, 'restaurant_images')
        os.makedirs(image_dir, exist_ok=True)

        saved_paths = []
        for img in uploaded_images:
          img_path = os.path.join(image_dir, img.name)
          with open(img_path, 'wb+') as dest:
            for chunk in img.chunks():
              dest.write(chunk)
          saved_paths.append(img_path)

        # Combine data for QR content
        qr_content = (
            f"Restaurant: {name}\n"
            f"Phones: {', '.join(phones)}\n"
            f"Facebook: {facebook}\n"
            f"Instagram: {instagram}\n"
            f"TikTok: {tiktok}"
            
      )
        # Save images to RestaurantImage model
        for img in uploaded_images:
            restaurant_image = RestaurantImage(restaurant=restaurant, image=img)
            restaurant_image.save()
        
        # Generate QR image
        #qr = qrcode.make(qr_content)
        #buffered = io.BytesIO()
        #qr.save(buffered, format="PNG")
        #qr_image = base64.b64encode(buffered.getvalue()).decode()

        random_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        qr_url = f"https://codeitdz.com/{random_code}"
       
        filename = f"qr_menu_{restaurant.id}.pdf"
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'restaurant_pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, filename)
        save_qr_pdf(qr_url, output_path=pdf_path)

        pdf_url = settings.MEDIA_URL + f'restaurant_pdfs/{filename}'

        # ✅ Clean the name: lowercase, replace spaces with underscore, remove special characters
        safe_name = re.sub(r'\W+', '_', name.strip().lower())

        # ✅ Final folder name
        folder_name = f"{safe_name}"
        
        # ✅ Path to user's Downloads directory
        downloads_path = "/mnt/c/Users/tahri/Downloads"

        # ✅ Full new directory path
        image_dirs = os.path.join(downloads_path, folder_name)

        # ✅ Create the directory
        os.makedirs(image_dirs, exist_ok=True)

        # Get absolute path to the statictest folder (relative to this file)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        statictest_dir = os.path.join(base_dir, 'statictest')

        # Define file paths (adjust filenames if different)
        file1 = os.path.join(statictest_dir, 'AI Roadmap_ based on Stanford AI Graduate Certificate.pdf')
        file2 = os.path.join(statictest_dir, 'IBMDataScienceProfessionalCertificateV3_Badge20241118-24-6p8soi.pdf')

        # Copy to Downloads/<folder_name>/
        shutil.copy(file1, image_dirs)
        shutil.copy(file2, image_dirs)

       # pdf_response = save_qr_pdf(qr_content, filename)

    return render(request, 'qrmainpage/formulaire.html', {
        'qr_content': qr_content,
        'pdf_url': pdf_url
    })


