import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
    QPushButton, QLabel, QFrame, QMessageBox, QGraphicsDropShadowEffect,
    QScrollArea, QFileDialog, QSizePolicy
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QColor, QCursor 

# ==========================================
# 🔹 INITIAL SIMULATION DATA
# IMPORTANT: This list defines all your simulation modules. 
#            Update the exe_path entries or use the GUI to set them.
# ==========================================
INITIAL_SIMULATIONS = [
    {
        "name": "Heart",
        "icon": "❤️",
        "description": "Cardiac Surgery VR",
        "exe_path": r"C:\Users\HP\Downloads\task4\HEART\UnityCrashHandler64.exe", 
        "color": "#D64545"  # Red
    },
    {
        "name": "Liver",
        "icon": "🟤",
        "description": "Hepatic Procedures VR",
        "exe_path": r"C:\Users\HP\Downloads\task4\liverSqueeze\My project (5).exe",
        "color": "#E85D75"  # Pink/Red
    },
    {
        "name": "Tooth",
        "icon": "🦷",
        "description": "Dental Training VR",
        "exe_path": r"C:\Users\HP\Downloads\task4\teeth\My project (4).exe",
        "color": "#4A90E2"  # Blue
    },
    {
        "name": "Flow", 
        "icon": "💧",
        "description": "Vascular Flow VR",
        "exe_path": r"C:\Users\HP\Downloads\task4\New folder\My project (16).exe",
        "color": "#00BCD4"  # Cyan
    },
    {
        "name": "Nose",
        "icon": "👃",
        "description": "ENT Surgery VR",
        "exe_path": r"C:\Users\HP\Downloads\task4\New folder\My project (16).exe", 
        "color": "#F5A623"  # Orange
    },
    {
        "name": "Abdomen",
        "icon": "🩺",
        "description": "Abdominal Trauma VR",
        "exe_path": r"C:\Users\HP\Downloads\task4\New folder\My project (16).exe",
        "color": "#7B68EE"  # Purple
    }
]

# ==========================================
# 🔹 COLOR PALETTE & STYLESHEET
# ==========================================

MEDICAL_COLORS = {
    "background": "#F0F4F8",
    "card_bg": "#FFFFFF",
    "primary": "#2C5F7C",
    "primary_hover": "#1E4558",
    "secondary": "#4A90E2",
    "accent": "#00A896",
    "text_header": "#1A3A52",
    "text_dark": "#2D3748",
    "text_light": "#718096",
    "success": "#48BB78",
    "error": "#F56565",
}

STYLESHEET = f"""
QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                 stop:0 #E8F4F8, stop:1 #D4E7F0);
}}
QLabel {{
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    color: {MEDICAL_COLORS['text_dark']};
}}
QLabel#MainTitle {{
    font-size: 42px;
    font-weight: 800;
    color: {MEDICAL_COLORS['text_header']};
    margin-bottom: 5px;
    letter-spacing: -1px;
}}
QLabel#SubTitle {{
    font-size: 16px;
    color: {MEDICAL_COLORS['text_light']};
    margin-bottom: 20px;
    font-weight: 500;
}}
QFrame.SimulationCard {{
    background-color: {MEDICAL_COLORS['card_bg']};
    border-radius: 20px;
    border: 2px solid #E2E8F0;
}}
QFrame.SimulationCard:hover {{
    border: 3px solid {MEDICAL_COLORS['secondary']};
}}
QLabel#IconBadge {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                 stop:0 #F7FAFC, stop:1 #EDF2F7);
    border-radius: 60px;
    border: 4px solid #E2E8F0;
}}
QPushButton#LaunchBtn {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                 stop:0 #00A896, stop:1 #008C7A);
    color: white;
    border-radius: 12px;
    padding: 14px 24px;
    font-size: 14px;
    font-weight: bold;
    border: none;
}}
QPushButton#LaunchBtn:hover {{
    background: {MEDICAL_COLORS['accent']};
}}
QPushButton#LaunchBtn:pressed {{
    background: #00695C;
}}
QPushButton#ConfigBtn {{
    background-color: {MEDICAL_COLORS['accent']};
    color: white;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: bold;
    border: none;
}}
QPushButton#ConfigBtn:hover {{
    background-color: #008C7A;
}}
QPushButton#BrowseBtn {{
    background-color: #A0AEC0;
    color: white;
    border-radius: 8px;
    padding: 8px 15px;
    font-size: 12px;
    font-weight: bold;
    border: none;
}}
QPushButton#BrowseBtn:hover {{
    background-color: #718096;
}}
QScrollBar:vertical {{
    border: none;
    background: #EDF2F7;
    width: 12px;
    border-radius: 6px;
}}
QScrollBar::handle:vertical {{
    background: #CBD5E0;
    border-radius: 6px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: #A0AEC0;
}}
"""

# ==========================================
# 🔹 SIMULATION CARD
# ==========================================
class SimulationCard(QFrame):
    def __init__(self, index, simulation_data, parent_window):
        super().__init__()
        self.index = index
        self.simulation = simulation_data
        self.parent_window = parent_window
        
        self.setProperty("class", "SimulationCard")
        self.setFixedSize(250, 350)
        self.setCursor(Qt.PointingHandCursor)

        # Shadow effect
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setColor(QColor(0, 0, 0, 30)) 
        self.shadow.setBlurRadius(25)
        self.shadow.setOffset(0, 8)
        self.setGraphicsEffect(self.shadow)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 25)

        # Status indicator
        status_container = QWidget()
        status_layout = QVBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        
        self.status_label = QLabel() 
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)
        layout.addWidget(status_container)

        # Icon with colored background
        icon_label = QLabel(simulation_data["icon"])
        icon_label.setObjectName("IconBadge")
        icon_label.setFixedSize(100, 100)
        icon_label.setAlignment(Qt.AlignCenter)
        font = self.parent_window.font()
        font.setPointSize(40)
        icon_label.setFont(font)
        
        # Add colored border matching simulation type
        icon_label.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                         stop:0 #FFFFFF, stop:1 {simulation_data['color']}20);
            border-radius: 50px;
            border: 4px solid {simulation_data['color']};
        """)
        layout.addWidget(icon_label)

        layout.addSpacing(5)

        # Simulation Name
        lbl_name = QLabel(simulation_data["name"])
        lbl_name.setStyleSheet(f"""
            font-size: 18px; 
            font-weight: bold; 
            color: {MEDICAL_COLORS['text_header']};
        """)
        lbl_name.setAlignment(Qt.AlignCenter)
        lbl_name.setWordWrap(True)
        layout.addWidget(lbl_name)

        # Description
        lbl_desc = QLabel(simulation_data["description"])
        lbl_desc.setStyleSheet(f"font-size: 12px; color: {MEDICAL_COLORS['text_light']};")
        lbl_desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_desc)

        layout.addSpacing(10)

        # Launch Button
        self.btn_launch = QPushButton("🚀 LAUNCH")
        self.btn_launch.setObjectName("LaunchBtn")
        self.btn_launch.setCursor(Qt.PointingHandCursor)
        self.btn_launch.clicked.connect(self.launch_simulation)
        
        # Customize button color based on the simulation
        launch_style = f"""
            QPushButton#LaunchBtn {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                             stop:0 {simulation_data['color']}, 
                                             stop:1 {self.darken_color(simulation_data['color'])});
                color: white;
                border-radius: 12px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }}
            QPushButton#LaunchBtn:hover {{
                background: {simulation_data['color']};
            }}
        """
        self.btn_launch.setStyleSheet(launch_style)
        layout.addWidget(self.btn_launch)
        
        self.update_status_indicator()

    def update_status_indicator(self):
        """Update the 'Ready/Not Found' label based on the current exe_path"""
        exe_path = self.parent_window.SIMULATIONS[self.index]["exe_path"]
        exists = os.path.exists(exe_path)
        
        status_text = "✅ Ready" if exists else "⚠️ Not Found"
        status_color = MEDICAL_COLORS['success'] if exists else MEDICAL_COLORS['error']
        
        self.status_label.setText(status_text)
        self.status_label.setStyleSheet(f"font-size: 11px; color: {status_color}; font-weight: bold;")
        self.btn_launch.setEnabled(exists)

    def darken_color(self, hex_color):
        """Darken a hex color by 20%"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * 0.7), int(g * 0.7), int(b * 0.7)
        return f'#{r:02x}{g:02x}{b:02x}'

    def launch_simulation(self):
        """
        Launch the Unity executable.
        Uses cwd=os.path.dirname(exe_path) to ensure the executable finds its data files.
        """
        exe_path = self.parent_window.SIMULATIONS[self.index]["exe_path"]
        
        if not os.path.exists(exe_path):
            QMessageBox.warning(self, "Launch Failed", "File not found. Please use 'Configure Paths' to set the correct location.")
            self.parent_window.update_status(f"❌ '{self.simulation['name']}' not found", MEDICAL_COLORS['error'])
            return
        
        try:
            # 1. Define the launch command (just the executable path)
            launch_command = [exe_path]
            
            # 2. CRITICAL STEP: Get the directory where the .exe file resides
            # This is the directory that must contain the *_Data folder.
            cwd_path = os.path.dirname(exe_path)
            
            # 3. Launch the process, setting the CWD
            process = subprocess.Popen(launch_command, cwd=cwd_path)
            
            print(f"Launching: {exe_path} (PID: {process.pid})")
            
            self.parent_window.update_status(
                f"✅ Launching '{self.simulation['name']}'...", 
                MEDICAL_COLORS['success']
            )
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Launch Error", 
                f"Failed to launch simulation (Error):\n\n{str(e)}"
            )
            self.parent_window.update_status(
                f"❌ Failed to launch '{self.simulation['name']}'", 
                MEDICAL_COLORS['error']
            )
    
    # --- Hover/Animation methods ---
    def enterEvent(self, event):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(250)
        self.anim.setStartValue(self.geometry())
        rect = self.geometry()
        rect.translate(0, -10)
        self.anim.setEndValue(rect)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()
        self.shadow.setBlurRadius(35)
        self.shadow.setOffset(0, 12)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(250)
        self.anim.setStartValue(self.geometry())
        rect = self.geometry()
        rect.translate(0, 10)
        self.anim.setEndValue(rect)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()
        self.shadow.setBlurRadius(25)
        self.shadow.setOffset(0, 8)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.launch_simulation()


# ==========================================
# 🔹 MAIN WINDOW (Suite Launcher)
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.SIMULATIONS = INITIAL_SIMULATIONS
        self.simulation_cards = []
        
        self.setWindowTitle("Surgical Simulation Suite")
        self.setGeometry(100, 50, 1600, 900)
        self.setStyleSheet(STYLESHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(50, 45, 50, 35)
        main_layout.setSpacing(25)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("🏥 Surgical Simulation Suite")
        title.setObjectName("MainTitle")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Select an anatomical module to initialize the VR environment")
        subtitle.setObjectName("SubTitle")
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        main_layout.addSpacing(10)

        # Configuration Button (Uses the dynamic path method)
        config_layout = QVBoxLayout()
        config_layout.setAlignment(Qt.AlignCenter)
        
        btn_config = QPushButton("⚙️ Configure Simulation Paths")
        btn_config.setObjectName("ConfigBtn")
        btn_config.setCursor(Qt.PointingHandCursor)
        btn_config.clicked.connect(self.show_config_dialog) 
        btn_config.setFixedWidth(300)
        config_layout.addWidget(btn_config)
        
        main_layout.addLayout(config_layout)
        main_layout.addSpacing(20)

        # Scroll Area for Cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(35)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.create_simulation_cards()
        
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # Status Bar
        status_container = QFrame()
        status_container.setStyleSheet(f"""
            background-color: {MEDICAL_COLORS['card_bg']};
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #E2E8F0;
        """)
        status_layout = QVBoxLayout(status_container)
        
        self.status_label = QLabel("🟢 System Ready • Waiting for input")
        self.status_label.setStyleSheet(f"color: {MEDICAL_COLORS['text_light']}; font-size: 13px; font-weight: 500;")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        main_layout.addWidget(status_container)

    def create_simulation_cards(self):
        """Create and display all simulation cards"""
        row, col = 0, 0
        max_cols = 6 
        
        for index, simulation in enumerate(self.SIMULATIONS):
            card = SimulationCard(index, simulation, self) 
            self.simulation_cards.append(card)
            self.grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def update_status(self, message, color=None):
        """Update status bar message"""
        if color is None:
            color = MEDICAL_COLORS['text_light']
        
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: 500;")

    def update_simulation_card(self, index):
        """Called after a path is set to refresh the status indicator"""
        self.simulation_cards[index].update_status_indicator()

    # ===============================================
    # 🔹 CONFIGURATION DIALOG METHODS
    # ===============================================
    def show_config_dialog(self):
        """Display a dialog for the user to configure all simulation paths."""
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Configure Simulation Paths")
        dialog.setIcon(QMessageBox.Information)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        info_label = QLabel("Click 'Browse' to set the full path for any Unity executable (.exe).")
        info_label.setStyleSheet(f"color: {MEDICAL_COLORS['primary']}; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(info_label)

        config_list_widget = QWidget()
        config_layout = QVBoxLayout(config_list_widget)
        config_layout.setSpacing(10)

        for index, sim in enumerate(self.SIMULATIONS):
            sim_widget = QWidget()
            sim_layout = QGridLayout(sim_widget)
            sim_layout.setContentsMargins(0, 5, 0, 5)

            # Status and Name Label (Column 0)
            exists = os.path.exists(sim["exe_path"])
            status_color = MEDICAL_COLORS['success'] if exists else MEDICAL_COLORS['error']
            
            status_label = QLabel(f"<span style='color:{status_color}; font-weight: bold;'>{sim['name']}</span>")
            status_label.setFixedWidth(150)
            sim_layout.addWidget(status_label, 0, 0)

            # Path Label (Column 1)
            path_label = QLabel(sim["exe_path"])
            path_label.setTextElideMode(Qt.ElideLeft)
            path_label.setStyleSheet(f"color: {MEDICAL_COLORS['text_light']}; font-size: 12px;")
            sim_layout.addWidget(path_label, 0, 1)

            # Browse Button (Column 2)
            browse_btn = QPushButton("Browse")
            browse_btn.setObjectName("BrowseBtn")
            browse_btn.setFixedWidth(100)
            
            # Use a lambda function to pass the index to the handler
            browse_btn.clicked.connect(lambda checked, idx=index: self.browse_for_exe(idx, dialog)) 
            sim_layout.addWidget(browse_btn, 0, 2)
            
            config_layout.addWidget(sim_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setWidget(config_list_widget)
        main_layout.addWidget(scroll_area)
        
        dialog.layout().addWidget(main_widget)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.exec_()


    def browse_for_exe(self, index, dialog_parent):
        """Browse for the correct executable file and update the configuration."""
        
        dialog_parent.close() 

        # Open file dialog
        current_path = os.path.dirname(self.SIMULATIONS[index]['exe_path']) or os.getcwd()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Locate {self.SIMULATIONS[index]['name']} Unity Executable",
            current_path, 
            "Unity Executable (*.exe);;All Files (*.*)"
        )
        
        if file_path:
            # Update the SIMULATIONS list in memory
            self.SIMULATIONS[index]["exe_path"] = file_path
            
            # Refresh the card status indicator
            self.update_simulation_card(index) 

            # Display success message
            QMessageBox.information(
                self, 
                "Path Updated", 
                f"✅ Path for '{self.SIMULATIONS[index]['name']}' updated to:\n{file_path}\n\n"
                "The changes are active for this session. Click 'Launch' to test."
            )

        self.show_config_dialog() 


# ==========================================
# 🔹 RUN APPLICATION
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())