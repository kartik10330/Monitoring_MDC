from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import time

app = Flask(__name__)

# System Configurations
VIBRATION_THRESHOLD = 7.0
LATCH_DURATION = 3.0  # Latch window in seconds

# Global storage for tracking real-time data attributes
latest_status = {
    "vibration": 0.0,
    "motor": 1  # FORCED ALWAYS ON (1) FOR PRESENTATION STABILITY
}

# Tracking states for the 3-second alert latch
poor_status_active = False
poor_status_start_time = 0.0

@app.route("/", methods=["GET"])
def home():
    return f"Vibration Monitoring Chatbot Master Server is Active! (Threshold: {VIBRATION_THRESHOLD} m/s²)", 200

# Endpoint for ESP8266 to push raw data packets
@app.route("/update", methods=["POST"])
def update_status():
    global poor_status_active, poor_status_start_time
    
    try:
        current_vib = float(request.form.get("vibration", 0.0))
    except ValueError:
        current_vib = 0.0
        
    latest_status["vibration"] = current_vib
    # We ignore request.form.get("motor") here to keep it hardcoded to active status

    # Latching Logic Engine: Check if vibration crosses the threshold limit
    if current_vib > VIBRATION_THRESHOLD:
        poor_status_active = True
        poor_status_start_time = time.time()  # Reset the countdown anchor
        
    return "Data Logged Successfully", 200

# Endpoint tied directly to your Twilio Sandbox Webhook
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    global poor_status_active
    
    incoming_msg = request.form.get('Body', '').strip().lower()
    response = MessagingResponse()
    msg = response.message()

    if "status" in incoming_msg:
        vib_val = latest_status["vibration"]
        is_on = latest_status["motor"] == 1 # This will evaluate to True
        
        # Format running profile string
        motor_state = "🟢 RUNNING" if is_on else "🔴 STOPPED"
        
        # Check if the 3-second latch timer has expired yet
        if poor_status_active:
            elapsed_time = time.time() - poor_status_start_time
            if elapsed_time < LATCH_DURATION:
                calculated_health = "⚠️ POOR (Threshold Exceeded)"
            else:
                if vib_val > VIBRATION_THRESHOLD:
                    calculated_health = "⚠️ POOR (Threshold Exceeded)"
                else:
                    poor_status_active = False  # Reset latch safely
                    calculated_health = "✅ HEALTHY"
        else:
            calculated_health = "✅ HEALTHY"

        # Construct the WhatsApp Message Layout
        reply_text = (
            f"📋 *SYSTEM MONITORING REPORT*\n\n"
            f"🔹 *Motor State:* {motor_state}\n"
            f"🔹 *Live Vibration:* {vib_val:.2f} m/s²\n"
            f"🔹 *System Health:* {calculated_health}\n\n"
            f"_Threshold Limit: {VIBRATION_THRESHOLD} m/s²_"
        )
        msg.body(reply_text)
    else:
        msg.body("Welcome to the System Bot! Send *'status'* to get live structural updates.")

    return str(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
