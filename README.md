Medical VR Surgical Simulator GUI
A professional, python-based graphical user interface (GUI) designed for launching Virtual Reality medical training simulations. This application serves as the control center for medical students to access various anatomical modules, including Heart, Knee, Liver, and Dental simulations.
🏥 Project Overview
This GUI is built using Python and PyQt5. It features a modern "medical-grade" aesthetic with a clean blue/teal color palette, rounded cards, and interactive hover animations. It is designed to be:
User-Friendly: Simple point-and-click interface.
Responsive: Automatically adjusts to screen sizes using a grid layout.
Robust: Handles network errors gracefully and uses multi-threading to prevent freezing.
✨ Key Features
6 Anatomical Modules:
🧴 Liver Palpation (Squeeze Simulation)
🦷 Dental Extraction
👃 Nasal Endoscopy
❤️ Heart Simulation (Cardiology)
🦵 Knee Surgery (Orthopedics)
🔪 Abdominal Incision
Dynamic Asset Loading: Fetches medical illustrations from remote URLs (Wikimedia Commons) automatically.
Async Processing: Uses background threads (QThread) to simulate file loading without freezing the main window.
Hidden Asset Management: Securely maps UI cards to hidden server URLs (.scn, .msh, .obj files).
Smart Error Handling: Automatically falls back to text emojis if an image fails to download.
🛠️ Prerequisites
Ensure you have Python installed on your system.
Python 3.8+
PyQt5 Library
📦 Installation
Clone or Download this project folder.
Open your terminal or command prompt.
Install the required dependencies:
pip install PyQt5


🚀 How to Run
Navigate to the project directory in your terminal and run the main script:
python medical_vr_gui_qt.py


⚙️ Configuration
Configuring Hidden URLs
The application connects to a backend server to fetch simulation files. You can configure these URLs in the HIDDEN_URLS dictionary located at the top of the medical_vr_gui_qt.py file:
HIDDEN_URLS = {
    'knee': {'scn': '[http://your-server.com/knee.scn](http://your-server.com/knee.scn)', ...},
    'heart': {'scn': '[http://your-server.com/heart.scn](http://your-server.com/heart.scn)', ...},
    # Add your real server paths here
}


Changing Icons
The code uses stable Wikimedia Commons URLs. If you wish to change an icon, update the url_ variables inside the MainWindow class.
🔧 Troubleshooting
1. Images not loading (403 Forbidden Error):
This happens if the server blocks python requests.
Fix: The code already includes a User-Agent header (Mozilla/5.0) in the ImageLoaderThread to bypass this. Ensure you are connected to the internet.
2. "Attribute Qt::AA_EnableHighDpiScaling must be set..." Error:
Fix: This error occurs in newer versions of PyQt5 where scaling is automatic. The current code has removed the manual setAttribute call to prevent this crash.
3. Window freezes when opening:
Fix: The application uses ImageLoaderThread to download images in the background. If it still freezes, check your internet connection speed.
📝 License
This project is developed for educational purposes (Medical VR Task 4).
