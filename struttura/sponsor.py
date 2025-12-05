from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                           QHBoxLayout, QTextBrowser, QApplication, QWidget,
                           QGridLayout, QSizePolicy)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import Qt, QUrl, QSize, QBuffer, QTimer
from PySide6.QtGui import QPixmap, QImage, QIcon
import webbrowser
import os
import io
import logging

# Try to import qrcode for QR code generation
try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    qrcode = None
    HAS_QRCODE = False
    logging.debug("qrcode not available - QR code generation will be disabled")

try:
    from wand.image import Image as WandImage
    from wand.drawing import Drawing
    from wand.color import Color
    HAS_WAND = True
except ImportError:
    WandImage = None
    Drawing = None
    Color = None
    HAS_WAND = False
    logging.debug("wand not available - QR code generation will be disabled")

logger = logging.getLogger(__name__)

class SponsorDialog(QDialog):
    def __init__(self, parent=None, language_manager=None):
        super().__init__(parent)
        self.setWindowTitle("Support")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Support OpenPGP")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Message
        message = QLabel("This application is developed and maintained by a single developer.\nIf you find this application useful, please consider supporting its development.\nYour support helps keep the project alive, allows for new features and improvements and encourages further development.\n\n")
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)
        
        # Create a grid layout for donation methods
        grid = QGridLayout()
        
        # GitHub button
        github_button = QPushButton("GitHub Sponsors")
        github_button.setStyleSheet("""
            QPushButton {
                background-color: #2ea44f;
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2c974b;
            }
        """)
        github_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/sponsors/Nsfr750")))

        # PayPal button
        paypal_button = QPushButton("PayPal Donation")
        paypal_button.setStyleSheet("""
            QPushButton {
                background-color: #0070ba;
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0062a3;
            }
        """)
        paypal_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://paypal.me/3dmega")))
        
        # Monero
        monero_address = "47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF"
        monero_display = "XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR XMR "
        monero_label = QLabel("Monero:")
        monero_xmr = monero_address
        monero_address_label = QLabel(monero_display)
        monero_address_label.setStyleSheet("""
            QLabel {
                font-family: monospace;
                background-color: #f0f0f0;
                color: #000;
                padding: 5px;
                border-radius: 3px;
                border: 1px solid #ddd;
            }
        """)
        
        # Generate QR Code (only if dependencies are available)
        if HAS_QRCODE and HAS_WAND and WandImage and Drawing and Color:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f'monero:{monero_address}')
            qr.make(fit=True)
            
            # Draw QR code with Wand
            matrix = qr.get_matrix()
            box_size = 10
            border = 4
            width = (len(matrix[0]) + border * 2) * box_size
            height = (len(matrix) + border * 2) * box_size

            with WandImage(width=width, height=height, background=Color('white')) as img:
                with Drawing() as draw:
                    draw.fill_color = Color('black')
                    # Draw black squares where matrix cell is True
                    for r, row in enumerate(matrix):
                        for c, cell in enumerate(row):
                            if cell:
                                x0 = (c + border) * box_size
                                y0 = (r + border) * box_size
                                x1 = x0 + box_size - 1
                                y1 = y0 + box_size - 1
                                draw.rectangle(left=x0, top=y0, right=x1, bottom=y1)
                    draw(img)
                img.format = 'png'
                buffer = io.BytesIO()
                img.save(file=buffer)
                data = buffer.getvalue()

            # Load into QPixmap
            pixmap = QPixmap()
            pixmap.loadFromData(data, "PNG")
            
            # Scale the pixmap to a reasonable size
            pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, 
                                 Qt.TransformationMode.SmoothTransformation)
            
            # Create a label to display the QR code
            qr_label = QLabel()
            qr_label.setPixmap(pixmap)
            qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qr_label.setToolTip("Scan to donate XMR")
            
            # Add widgets to grid
            grid.addWidget(QLabel("<h3>>Ways to Support:</h3>"), 0, 0, 1, 2)
            grid.addWidget(github_button, 1, 0, 1, 2)
            grid.addWidget(paypal_button, 2, 0, 1, 2)
            grid.addWidget(monero_label, 3, 0, 1, 2)
            grid.addWidget(monero_address_label, 4, 0, 1, 2)
            grid.addWidget(qr_label, 1, 2, 4, 1)  # Span 4 rows
        else:
            # QR code not available, adjust layout
            grid.addWidget(QLabel("<h3>>Ways to Support:</h3>"), 0, 0, 1, 2)
            grid.addWidget(github_label, 1, 0, 1, 2)
            grid.addWidget(paypal_label, 2, 0, 1, 2)
            grid.addWidget(monero_label, 3, 0, 1, 2)
            grid.addWidget(monero_address_label, 4, 0, 1, 2)
            
            # Add a placeholder for QR code
            qr_placeholder = QLabel("QR Code not available\n(requires qrcode and wand libraries)")
            qr_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qr_placeholder.setStyleSheet("color: #666; font-size: 12px; padding: 20px;")
            grid.addWidget(qr_placeholder, 1, 2, 4, 1)  # Span 4 rows
        
        # Add some spacing
        grid.setSpacing(10)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        
        # Add grid to layout
        layout.addLayout(grid)
        
        # Other ways to help
        other_help = QTextBrowser()
        other_help.setOpenExternalLinks(True)
        other_help.setHtml("""
        <h3>Other Ways to Help:</h3>
        <ul>
            <li>Star the project on <a href="https://github.com/Nsfr750/EmailDuplicateCleaner">GitHub</a></li>
            <li>Report bugs and suggest features</li>
            <li>Share with others who might find it useful</li>
        </ul>
        """)    
        other_help.setMaximumHeight(150)
        layout.addWidget(other_help)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: orange;
            }
        """)
        
        # Donate button
        donate_btn = QPushButton("Donate with PayPal")
        donate_btn.setStyleSheet("""
            QPushButton {
                background-color: #0079C1;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0062A3;
            }
        """)
        donate_btn.clicked.connect(self.open_paypal_link)
        
        # Copy Monero address button
        self.copy_monero_btn = QPushButton("Copy Monero Address")
        self.copy_monero_btn.setStyleSheet("""
            QPushButton {
                background-color: #F26822;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #D45B1D;
            }
        """)
        self.copy_monero_btn.clicked.connect(lambda: self.copy_to_clipboard(monero_address))
        
        button_layout.addWidget(close_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.copy_monero_btn)
        button_layout.addWidget(donate_btn)
        
        layout.addLayout(button_layout)
    
    def open_donation_link(self):
        """Open donation link in default web browser."""
        QDesktopServices.openUrl(QUrl("https://github.com/sponsors/Nsfr750"))
    
    def open_paypal_link(self):
        """Open PayPal link in default web browser."""
        QDesktopServices.openUrl(QUrl("https://paypal.me/3dmega"))
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard and show a tooltip."""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        
        # Change button text temporarily
        original_text = self.copy_monero_btn.text()
        self.copy_monero_btn.setText("Copied!")
        
        # Reset button text after 2 seconds
        QTimer.singleShot(2000, self.reset_monero_button)
    
    def reset_monero_button(self):
        """Reset the Monero button text and style."""
        self.copy_monero_btn.setText("Copy Monero Address")
        