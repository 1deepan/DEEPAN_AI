# Deepan AI (J.A.R.V.I.S) — How to Run

Follow these steps to set up and run your personal AI assistant.

## 1. Prerequisites
- **Python 3.8+**: Ensure you have Python installed.
- **API Keys**: Open the [.env](file:///c:/Users/S.DEEPAN%20KUMAR/OneDrive/Attachments/Desktop/Ironman/.env) file and ensure your `OPENAI_API_KEY` and `GEMINI_API_KEY` are correctly set.

## 2. Installation
Open your terminal (CMD or PowerShell) in the project directory and run:

```bash
pip install -r requirements.txt
```

> [!NOTE]
> If you encounter issues with voice recognition, you may need to install `PyAudio` separately:
> `pip install pyaudio`

## 3. Running the Program
To start the J.A.R.V.I.S server, run:

```bash
python app.py
```

## 4. Accessing the HUD
Once the server is running, you can access the interface in your web browser at:
**[http://localhost:5000](http://localhost:5000)**

---
### Features
- **Voice Commands**: Click the microphone icon or say commands.
- **Task Analysis**: Upload documents for AI-powered tactical briefings.
- **System Monitoring**: Live CPU, RAM, and Battery stats on the dashboard.
