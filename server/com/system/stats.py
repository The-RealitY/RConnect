import time

from server import app, SERVER_UPTIME
from server.com.ext.helper import send_response
from server.util.misc import format_time


@app.route('/api/v1', methods=['GET'])
async def server_state(_):
    return send_response(
        {
            "data": [{
                'upTime': format_time(time.time() - SERVER_UPTIME)
            }],
            'message': "Server API was up and running!"

        },
        200
    )
