import sys
import time
import urllib.request
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
    QPushButton, QLabel, QFrame, QMessageBox, QGraphicsDropShadowEffect,
    QProgressBar, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QCoreApplication
from PyQt5.QtGui import QFont, QColor, QCursor, QPixmap, QPainter, QBrush

# ==========================================
# 🔹 1. CONFIGURATION & STYLES
# ==========================================

COLORS = {
    "background": "#F1F9FF",
    "card_bg":    "#FFFFFF",
    "card_accent": "#CCECEE",
    "button":     "#14967F",
    "button_hover": "#117A65",
    "text_header": "#0E6655",
    "text_dark":  "#2C3E50",
}

# Hidden File Configuration
HIDDEN_URLS = {
    'knee': {'scn': 'http://server/knee.scn', 'msh': 'http://server/knee.msh', 'obj': 'http://server/knee.obj'},
    'heart': {'scn': 'http://server/heart.scn', 'msh': 'http://server/heart.msh', 'obj': 'http://server/heart.obj'},
    'nasal': {'scn': 'http://server/nasal.scn', 'msh': 'http://server/nasal.msh', 'obj': 'http://server/nasal.obj'},
    'dental': {'scn': 'http://server/dental.scn', 'msh': 'http://server/dental.msh', 'obj': 'http://server/dental.obj'},
    'liver': {'scn': 'http://server/liver.scn', 'msh': 'http://server/liver.msh', 'obj': 'http://server/liver.obj'},
    'incision': {'scn': 'http://server/cut.scn', 'msh': 'http://server/cut.msh', 'obj': 'http://server/cut.obj'}
}

STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['background']};
}}
QLabel {{
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    color: {COLORS['text_dark']};
}}
QLabel#MainTitle {{
    font-size: 32px;
    font-weight: 800;
    color: {COLORS['text_header']};
    margin-bottom: 5px;
}}
QLabel#SubTitle {{
    font-size: 14px;
    color: #7F8C8D;
}}
QFrame.OrganCard {{
    background-color: {COLORS['card_bg']};
    border-radius: 15px;
    border: 1px solid #E0F2F1;
}}
QLabel#IconBadge {{
    background-color: {COLORS['card_accent']};
    border-radius: 35px;
    border: 2px solid #B2DFDB;
}}
QPushButton {{
    background-color: {COLORS['button']};
    color: white;
    border-radius: 15px;
    padding: 10px 15px;
    font-size: 12px;
    font-weight: bold;
    border: none;
}}
QPushButton:hover {{
    background-color: {COLORS['button_hover']};
}}
QProgressBar {{
    background-color: #E0E0E0;
    border-radius: 6px;
    height: 10px;
    text-align: center;
}}
QProgressBar::chunk {{
    background-color: {COLORS['button']};
    border-radius: 6px;
}}
"""

# ==========================================
# 🔹 2. WORKER THREADS
# ==========================================

class ImageLoaderThread(QThread):
    image_loaded = pyqtSignal(QPixmap)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            # Use User-Agent to avoid 403 Forbidden errors
            req = urllib.request.Request(
                self.url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            data = urllib.request.urlopen(req, timeout=8).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.image_loaded.emit(pixmap)
        except Exception as e:
            # Silently fail; UI will keep the fallback text/emoji
            pass

class FileLoaderThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str, dict)

    def __init__(self, organ_key, urls):
        super().__init__()
        self.organ_key = organ_key
        self.urls = urls

    def run(self):
        for i in range(1, 101):
            time.sleep(0.01) 
            self.progress_signal.emit(i)
        
        local_files = {
            'scn': f"/local/cache/{self.organ_key}.scn",
            'msh': f"/local/cache/{self.organ_key}.msh",
            'obj': f"/local/cache/{self.organ_key}.obj"
        }
        self.finished_signal.emit(self.organ_key, local_files)

# ==========================================
# 🔹 3. UI COMPONENTS
# ==========================================
class OrganCard(QFrame):
    clicked_signal = pyqtSignal(str, str)

    def __init__(self, title, icon_source, organ_key, button_label="Start", is_image_url=False, fallback_emoji="⚕️"):
        super().__init__()
        self.organ_key = organ_key
        self.title = title
        self.setProperty("class", "OrganCard")
        self.setFixedSize(240, 300) 
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 15))
        self.shadow.setOffset(0, 5)
        self.setGraphicsEffect(self.shadow)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        # Icon Label
        self.icon_label = QLabel()
        self.icon_label.setObjectName("IconBadge")
        self.icon_label.setFixedSize(70, 70)
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)

        # Set default emoji first (so something is always visible)
        self.icon_label.setText(fallback_emoji)
        font = QFont()
        font.setPointSize(28)
        self.icon_label.setFont(font)

        # Start loading image if URL provided
        if is_image_url:
            self.loader = ImageLoaderThread(icon_source)
            self.loader.image_loaded.connect(self.set_rounded_image)
            self.loader.start()

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)

        lbl_desc = QLabel("VR Simulation")
        lbl_desc.setStyleSheet("font-size: 11px; color: #95A5A6;")
        lbl_desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_desc)

        self.btn_load = QPushButton(button_label) 
        self.btn_load.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_load.clicked.connect(self.emit_click)
        layout.addWidget(self.btn_load)

    def set_rounded_image(self, pixmap):
        if pixmap.isNull(): return
        
        # Crop and Scale to Circle
        size = 70
        pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        
        rounded = QPixmap(size, size)
        rounded.fill(Qt.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create circular path
        path = QBrush(pixmap)
        painter.setBrush(path)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)
        painter.end()
        
        self.icon_label.setPixmap(rounded)

    def emit_click(self):
        self.clicked_signal.emit(self.organ_key, self.title)

    def enterEvent(self, event):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(100)
        self.anim.setStartValue(self.geometry())
        rect = self.geometry()
        rect.translate(0, -5)
        self.anim.setEndValue(rect)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(100)
        self.anim.setStartValue(self.geometry())
        rect = self.geometry()
        rect.translate(0, 5)
        self.anim.setEndValue(rect)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        self.anim.start()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.emit_click()

# ==========================================
# 🔹 4. MAIN WINDOW
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical VR Surgical Simulator")
        self.setGeometry(100, 100, 1100, 800)
        self.setStyleSheet(STYLESHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Header
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        title = QLabel("Surgical Simulation Suite")
        title.setObjectName("MainTitle")
        title.setAlignment(Qt.AlignCenter)
        subtitle = QLabel("Select an anatomical module to initialize the VR environment")
        subtitle.setObjectName("SubTitle")
        subtitle.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        main_layout.addSpacing(20)

        # --- Scroll Area for Cards ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("background: transparent;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        
        # Grid Layout (2 Rows x 3 Cols)
        grid_layout = QGridLayout(scroll_content)
        grid_layout.setSpacing(30)
        grid_layout.setAlignment(Qt.AlignCenter)

        # --- NEW STABLE WIKIMEDIA URLS (No more random icon sites) ---
        url_liver = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Gray1086-liver.png/250px-Gray1086-liver.png"
        url_dental = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Tooth_Section.svg/200px-Tooth_Section.svg.png"
        url_nasal = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Blausen_0872_UpperRespiratorySystem.png/250px-Blausen_0872_UpperRespiratorySystem.png"
        url_heart = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Heart_anterior_exterior_view.jpg/200px-Heart_anterior_exterior_view.jpg"
        url_knee = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Knee_diagram.svg/200px-Knee_diagram.svg.png"
        url_cut = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Scalpel_icon.svg/200px-Scalpel_icon.svg.png"

        # Data: (Title, Icon_Source, Key, Button_Label, Is_Image_URL, Fallback_Emoji)
        self.cards_data = [
            ("Liver Palpation", url_liver, "liver", "Start Palpation", True, "🧴"),
            ("Dental Extraction", url_dental, "dental", "Start Extraction", True, "🦷"),
            ("Nasal Endoscopy", url_nasal, "nasal", "Start Endoscopy", True, "👃"),
            ("Heart Simulation", url_heart, "heart", "Launch Cardiology", True, "❤️"),
            ("Knee Surgery", url_knee, "knee", "Launch Orthopedics", True, "🦵"),
            ("Abdominal Incision", url_cut, "incision", "Perform Incision", True, "🔪")
        ]

        row, col = 0, 0
        for title, icon, key, btn_text, is_img, emoji in self.cards_data:
            card = OrganCard(title, icon, key, btn_text, is_image_url=is_img, fallback_emoji=emoji)
            card.clicked_signal.connect(self.start_loading)
            grid_layout.addWidget(card, row, col)
            col += 1
            if col > 2: 
                col = 0
                row += 1

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Footer
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(400)
        self.progress_bar.setVisible(False)
        self.status_label = QLabel("System Ready • Waiting for input")
        self.status_label.setStyleSheet("color: #95A5A6; font-size: 12px;")
        
        footer_layout = QVBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(self.progress_bar)
        footer_layout.addWidget(self.status_label)
        main_layout.addLayout(footer_layout)

    def start_loading(self, organ_key, title):
        urls = HIDDEN_URLS.get(organ_key)
        self.status_label.setText(f"🚀 Initializing {title}...")
        self.status_label.setStyleSheet("color: #14967F; font-weight: bold;")
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.loader_thread = FileLoaderThread(organ_key, urls)
        self.loader_thread.progress_signal.connect(self.progress_bar.setValue)
        self.loader_thread.finished_signal.connect(self.loading_complete)
        self.loader_thread.start()

    def loading_complete(self, organ_key, local_files):
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"✅ {organ_key.capitalize()} assets loaded.")
        msg = QMessageBox()
        msg.setWindowTitle("Ready")
        msg.setText(f"{organ_key.capitalize()} Simulation Loaded Successfully.")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())