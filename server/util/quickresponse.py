import json
import os

import qrcode
from uvicorn.config import logger

from server.util.misc import get_mime_type


class GenerateQRC:
    def __init__(self, root_path):
        self.qrc_abspath = os.path.join(os.getcwd(), root_path)
        self.extension = ".jpg"
        self._image_name = f"QuickResponseCode"
        self._qr = qrcode.main.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )

    def generate_qrc(self, data, uuid):
        self._qr.add_data(data)
        self._qr.make(fit=True)
        img = self._qr.make_image(fill_color="black", back_color="white")
        image_folder = os.path.join(self.qrc_abspath, uuid)
        os.makedirs(image_folder, exist_ok=True)
        img_path = os.path.join(image_folder, f"{self._image_name}_{uuid}{self.extension}")
        with open(img_path, 'wb') as img_file:
            img.save(img_file)
        qrc_md = {
            "file_name": f"{self._image_name}_{uuid}{self.extension}",
            "legacy_name": self._image_name + self.extension,
            "file_type": get_mime_type(img_path),
            "extension": self.extension,
            "uuid": uuid
        }
        return json.dumps(qrc_md)
