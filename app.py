from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Global storage for tracking real-time status parameters
latest_status = {
    "vibration": "0.00",
    "motor": "0",
    "health": "Unknown"
}

# Root route to check if the server is alive
@app.route("/", methods=["GET"])
def home():
    return "Vibration Monitoring Chatbot Server is Live!", 200

# Endpoint for ESP8266 to push live state parameters
@app.route("/update", methods=["POST"])
def update_status():
    latest_status["vibration"] = request.form.get("vibration", "0.00")
    latest_status["motor"] = request.form.get("motor", "0")
    latest_status["health"] = request.form.get("health", "Unknown")
    return "Data Updated", 200

# Endpoint tied directly to your Twilio Sandbox WhatsApp Incoming Webhook
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body', '').strip().lower()
    response = MessagingResponse()
    msg = response.message()

    if "status" in incoming_msg:
        # Check if motor variable is active ('1' or 'true')
        is_on = latest_status["motor"] in ["1", "true", "True"]
        motor_state = "🟢 RUNNING" if is_on else "🔴 STOPPED"
        
        reply_text = (
            f"📋 *SYSTEM MONITORING REPORT*\n\n"
            f"🔹 *Motor State:* {motor_state}\n"
            f"🔹 *Live Vibration:* {float(latest_status['vibration']):.2f} m/s²\n"
            f"🔹 *System Health:* ⭐ {latest_status['health']}\n"
        )
        msg.body(reply_text)
    else:
        msg.body("Welcome to the System Bot! Send *'status'* to get live structural updates.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
