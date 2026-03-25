"""Deepan AI — Personal AI Assistant
Flask application entry point.
"""
import logging
import os
import threading
import sys
import webbrowser
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

from assistant.commands import process_command, get_command_list
from assistant.voice import speak, listen
from assistant.llm import llm_service
from assistant.file_parser import extract_text_from_file
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ===========================
# FLASK ROUTES
# ===========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"reply": "Invalid request."}), 400
    text = data["text"].strip()
    if not text:
        return jsonify({"reply": "Please enter a command."})
    logger.info(f"Command: {text}")
    
    response = process_command(text)
    speak(response["reply"])
    return jsonify(response)


@app.route("/voice", methods=["GET"])
def voice():
    text = listen()
    if not text:
        return jsonify({
            "reply": "I didn't catch that, sir. Please try again.", 
            "heard": "",
            "action": None
        })
    logger.info(f"Voice: {text}")
    
    response = process_command(text)
    speak(response["reply"])
    response["heard"] = text
    return jsonify(response)


@app.route("/commands", methods=["GET"])
def commands_list():
    return jsonify({"commands": get_command_list()})


@app.route("/stats", methods=["GET"])
def stats():
    result = {"cpu": 0, "ram": 0, "battery": 0, "disk": 0}
    try:
        import psutil
        result["cpu"] = psutil.cpu_percent(interval=0.1)
        result["ram"] = psutil.virtual_memory().percent
        bat = psutil.sensors_battery()
        result["battery"] = bat.percent if bat else 100
        result["disk"] = psutil.disk_usage('/').percent
    except:
        pass
    return jsonify(result)


@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"reply": "No file part, sir."}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"reply": "No selected file, sir."}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        notes = ""
        extracted_text = extract_text_from_file(file_path)
        if extracted_text:
            prompt = f"Analyze document: {extracted_text[:4000]}"
            notes = llm_service.generate_response(prompt)
            if notes:
                speak("Sir, I have analyzed the document.")
                return jsonify({
                    "reply": f"File '{filename}' analyzed.",
                    "notes": notes
                })

        return jsonify({"reply": f"File '{filename}' stored."})


# ===========================
# SYSTEM TRAY LOGIC
# ===========================

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def create_tray_icon():
    try:
        import pystray
        from pystray import MenuItem as item
        from PIL import Image, ImageDraw

        def on_open_hud(icon, item):
            webbrowser.open("http://localhost:5000")

        def on_quit(icon, item):
            icon.stop()
            os._exit(0)

        # Create a simple JARVIS-style icon (blue circle)
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), (10, 10, 10))
        dc = ImageDraw.Draw(image)
        dc.ellipse((8, 8, 56, 56), fill=(0, 200, 255), outline=(255, 255, 255))
        dc.ellipse((20, 20, 44, 44), fill=(10, 10, 10), outline=(0, 200, 255))

        menu = (
            item('Open JARVIS HUD', on_open_hud),
            item('Restart Full Systems', on_open_hud),
            item('Exit JARVIS', on_quit),
        )

        icon = pystray.Icon("Ironman", image, "J.A.R.V.I.S (Active)", menu)
        icon.run()
    except Exception as e:
        logger.error(f"Tray Icon Error: {e}")
        # If tray fails, just run flask in main thread (fallback)
        run_flask()

if __name__ == "__main__":
    print("\n[*] J.A.R.V.I.S — Background Initialization...")
    
    # Start Flask in a background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    print("[*] Access the HUD at http://localhost:5000")
    print("[*] Use the System Tray icon to manage JARVIS.\n")
    
    # Run Tray Icon in main thread
    create_tray_icon()