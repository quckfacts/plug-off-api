from flask import Flask, request, jsonify
from tapo import ApiClient
import asyncio
import json

app = Flask(__name__)

@app.route("/turn_off", methods=["POST"])
def turn_off():
    try:
        body = request.get_json()
        email = body.get("email")
        password = body.get("password")
        ip_address = body.get("ip")

        if not (email and password and ip_address):
            return jsonify({"error": "Missing email, password, or ip"}), 400

        async def turn_off_plug():
            client = ApiClient(email, password)
            plug = await client.p110(ip_address)
            await asyncio.sleep(72)  # Delay for 1 min 12 sec
            await plug.off()

        asyncio.run(turn_off_plug())
        return jsonify({"message": "Scheduled plug shutdown after delay"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
