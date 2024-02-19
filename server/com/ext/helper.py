from starlette.responses import JSONResponse, FileResponse


def send_response(content: dict, status: int = 200):
    payload = {
        "data": content.get('data', []),
        "message": content.get('message', 'N/A')
    }
    return JSONResponse(
        status_code=status,
        content=payload,
    )


def send_file(file_path, download_name=None, as_attachment=True):
    return FileResponse(file_path, filename=download_name,
                        content_disposition_type="inline" if not as_attachment else "attachment")

