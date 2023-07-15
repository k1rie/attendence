import tempfile

import qrcode


class QRGenerator:

    @staticmethod
    def generate_qr_code(url):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)

        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as img_file:
            img.save(img_file)
            return img_file.name
