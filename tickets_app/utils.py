import base64
from io import BytesIO

import qrcode
from django.urls import reverse

from django.urls import reverse
from django.http import HttpRequest


def generate_qr_code(request: HttpRequest, relative: str, uuid: str):
    absolute_url = request.build_absolute_uri(reverse(relative, kwargs={'ticket_id': uuid}))

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(absolute_url)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    qr_image.save(buffered)  # Specify the format as "PNG"
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return qr_code_base64




