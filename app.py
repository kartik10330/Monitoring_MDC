from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Configurable threshold for evaluation
VIBRATION_THRESHOLD = 7.0

# Global storage for tracking real-time status parameters from the ESP8266
latest_status = {
    "vibration": "0.00",
    "motor": "0",
    "health": "Unknown"
}

# Root route to quickly verify in your browser if Render is up and running
@app.route("/", methods=["GET"])
def home():
    return f"Vibration Monitoring Chatbot Server is Live! (Threshold Set to: {VIBRATION_THRESHOLD} m/s²)", 200

# Endpoint for ESP8266 to push live state parameters over HTTP POST
@app.route("/update", methods=["POST"])
def update_status():
    latest_status["vibration"] = request.form.get("vibration", "0.00")
    latest_status["motor"] = request.form.get("motor", "0")
    latest_status["health"] = request.form.get("health", "Unknown")
    return "Data Updated Successfully", 200

# Endpoint tied directly to your Twilio Sandbox WhatsApp Incoming Webhook
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    # Capture what the user typed in WhatsApp (converted to lowercase)
    incoming_msg = request.form.get('Body', '').strip().lower()
    
    response = MessagingResponse()
    msg = response.message()

    if "status" in incoming_msg:
        # 1. Parse current metrics
        try:
            vib_val = float(latest_status["vibration"])
        except ValueError:
            vib_val = 0.00

        is_on = latest_status["motor"] in ["1", "true", "True"]
        
        # 2. Determine Motor State String
        motor_state = "🟢 RUNNING" if is_on else "🔴 STOPPED"
        
        # 3. Apply the 7.0 m/s² Threshold Overrides for Chatbot Reporting
        if not is_on:
            calculated_health = "OFFLINE"
        elif vib_val > VIBRATION_THRESHOLD:
            calculated_health = "🚨 CRITICAL (Exceeds 7.0 m/s²)"
        else:
            calculated_health = "✅ HEALTHY"

        # 4. Construct the WhatsApp Message Card
        reply_text = (
            f"📋 *SYSTEM MONITORING REPORT*\n\n"
            f"🔹 *Motor State:* {motor_state}\n"
            f"🔹 *Live Vibration:* {vib_val:.2f} m/s²\n"
            f"🔹 *System Health:* {calculated_health}\n\n"
            f"_Threshold Limit: {VIBRATION_THRESHOLD} m/s²_"
        )
        msg.body(reply_text)
        
    else:
        # Default response if someone texts anything other than "status"
        msg.body("Welcome to the System Bot! Send *'status'* to get live structural updates.")

    return str(response)

if __name__ == "__main__":
    # Bound to 0.0.0.0 so Render can map it to its public routing system
    app.run(host="0.0.0.0", port=5000)
