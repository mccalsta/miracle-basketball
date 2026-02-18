from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from io import BytesIO
import base64

def generate_pdf(registration, qr_base64, logo_path='static/images/logo.png', brand_color="#1F77B4"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    logo = ImageReader(logo_path)
    c.drawImage(logo, 50, height - 100, width=100, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(HexColor(brand_color))
    c.drawString(200, height - 80, "Registration Receipt")
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#000000"))
    c.drawString(50, height - 150, f"Name: {registration['name']}")
    c.drawString(50, height - 170, f"Email: {registration.get('email','')}")
    c.drawString(50, height - 190, f"Phone: {registration.get('phone','')}")
    c.drawString(50, height - 210, f"DOB: {registration.get('dob','')}")
    c.drawString(50, height - 230, f"Gender: {registration.get('gender','')}")
    c.drawString(50, height - 250, f"Occupation: {registration.get('occupation','')}")
    c.drawString(50, height - 270, f"City: {registration.get('city','')}")
    c.drawString(50, height - 290, f"Date: {registration['date']}")
    qr_bytes = BytesIO(base64.b64decode(qr_base64))
    qr_image = ImageReader(qr_bytes)
    c.drawImage(qr_image, width - 200, height - 300, width=150, height=150)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
