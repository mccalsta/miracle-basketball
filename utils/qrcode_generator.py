import qrcode
from io import BytesIO
import base64

def generate_qr(data):
    qr = qrcode.QRCode(version=1,box_size=10,border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black',back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
