import mimetypes


def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def send_notification(recipient, content, medium=1):
    sender_name = "RealitY"
