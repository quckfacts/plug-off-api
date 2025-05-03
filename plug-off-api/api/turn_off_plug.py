# api/turn_off_plug.py
from tapo import ApiClient
import asyncio
import json

def handler(request):
    try:
        if request.method != 'POST':
            return (405, {}, "Only POST requests allowed")

        body = request.body.decode("utf-8")
        data = json.loads(body)

        email = data.get("email")
        password = data.get("password")
        ip_address = data.get("ip")

        if not (email and password and ip_address):
            return (400, {}, "Missing email, password, or ip in request body")

        async def turn_off():
            client = ApiClient(email, password)
            plug = await client.p110(ip_address)
            await asyncio.sleep(72)  # 1 min 12 sec delay
            await plug.off()

        asyncio.run(turn_off())
        return (200, {}, "Scheduled plug shutdown after delay")

    except Exception as e:
        return (500, {}, f"Error: {str(e)}")
