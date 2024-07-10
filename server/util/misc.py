import mimetypes

from starlette.requests import Request
from user_agents import parse


def get_mime_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)
    return f"{hours}hrs {minutes}m {remaining_seconds}s"


def requestor_metadata(request: Request):
    headers = request.headers
    request_ip = headers.get('x-forwarded-for', 'unknown')
    user_agent_string = headers.get('user-agent', 'unknown')
    user_agent = parse(user_agent_string)
    device_name = user_agent.device.family
    os_name = f"{user_agent.os.family} {user_agent.os.version_string}"
    browser_name = f"{user_agent.browser.family} {user_agent.browser.version_string}"

    return {
        "requestor_ip": request_ip,
        "device_name": device_name,
        "os_name": os_name,
        "browser_name": browser_name
    }
