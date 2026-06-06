# Industrial IoT (IIoT) Structural Health Monitoring & Predictive Maintenance System

An automated, end-to-end Industrial IoT (IIoT) and digital twin solution designed for real-time asset evaluation, structural vibration telemetry, and remote edge control. This system bridges local physical sensor networks with cloud architectures and conversational instant messaging layers to provide instant system visibility and critical fault protection.

---

## 🚀 Key Features

* **Dual-Layer Visibility:** Features a high-speed local web dashboard for on-site monitoring alongside a secure cloud-connected cloud server.
* **Conversational Chatbot Interface:** Built-in integration with **Twilio and WhatsApp** to request live structural updates via text command metrics.
* **Intelligent Timing Latch Engine:** Incorporates a cloud-side 3-second alert latch algorithm to catch and lock high-vibration transients ($\ge 7.0\text{ m/s}^2$), preventing quick spikes from masking prolonged mechanical wear.
* **Bi-Directional Edge Control:** Built-in architecture to dispatch remote relay signaling commands ("Turn On/Off Motor") over WhatsApp down to the physical hardware actuator.
* **Professional Analytical Dashboard:** Includes rolling historical ledgers, maximum peak memory indicators, and visual reference thresholds matching modern Supervisory Control and Data Acquisition (SCADA) systems.

---

## 📊 System Architecture & Data Flow

The project layout decouples raw edge collection from intensive cloud notification processes:

1. **Hardware Edge:** The **ESP8266** samples mechanical force attributes from an **ADXL345** accelerometer via the $I^2C$ protocol, calculates mathematical vector magnitudes, and hosts an asynchronous local web server for instantaneous data polling.
2. **Secure Sync Ingestion:** Every 5 seconds, the microcontroller handles a secure `WiFiClientSecure` HTTPS POST handshake to dispatch formatted raw string parameters up to the cloud.
3. **Cloud Processing Hub:** A web app hosted on **Render** serves as the central data master. It parses incoming telemetry and exposes dedicated webhooks for webhook endpoints.
4. **Instant Notification Layer:** The cloud app formats real-time status data cards and responds immediately to automated network inquiries parsed from the WhatsApp client ecosystem.

---

## 🛠️ Hardware Circuit Setup

The hardware utilizes an isolated dual-power design to separate sensitive logic processing from high-current motor inductive loads:

* **Logic Core Power:** The ESP8266 is safely powered via a laptop USB connection or standard 5V wall-charging grid adapter.
* **Motor Driving Power:** The DC motor runs independently on its own dedicated external power loop.
* **Relay Isolation Logic:**
    * **VCC** $\rightarrow$ ESP8266 **VIN** (5V USB rail)
    * **GND** $\rightarrow$ ESP8266 **GND** (Common reference ground shared with external negative supply rail)
    * **IN (Signal)** $\rightarrow$ ESP8266 **D5 (GPIO14)**
    * **External Load Switching:** External Positive (+) Line wired through Relay **COM** (Common) and **NO** (Normally Open) terminals. **NC** (Normally Closed) is left intentionally empty for default-off safety configuration.

---

## 📂 Repository Structure

```text
├── app.py                # Python/Flask Backend Web Server (Handles Twilio & Latching Engine)
├── esp8266_sketch.ino    # ESP8266 Arduino Sketch (Local Web Server & ADXL345 Ingestion)
└── README.md             # Project documentation and presentation manual
