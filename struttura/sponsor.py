"""
Sponsor dialog for the EmailDuplicateCleaner application.
"""
import sys
import os
import qrcode
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Type, Any

# Import LanguageManager with fallback
from PySide6.QtCore import QObject, Signal as QtSignal

class DummyLanguageManager:
    """Dummy LanguageManager for when the real one is not available."""
    def __init__(self):
        class SignalHolder(QObject):
            language_changed = QtSignal(str)
        self._signal_holder = SignalHolder()
        self.language_changed = self._signal_holder.language_changed
    
    def translate(self, key: str, **kwargs: Any) -> str:
        # Return the key as the default translation
        if kwargs:
            try:
                return key.format(**kwargs)
            except (KeyError, IndexError):
                return key
        return key
        
    def get_language(self) -> str:
        return "en"  # Default to English

try:
    from lang.lang_manager import LanguageManager
except ImportError:
    LanguageManager = DummyLanguageManager  # type: ignore

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QWidget, QSizePolicy, QSpacerItem, QSizePolicy as QSP,
    QGraphicsDropShadowEffect, QGridLayout, QTextBrowser
)
from PySide6.QtCore import Qt, QUrl, QSize, QPropertyAnimation, QEasingCurve, QFile, QRect
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QColor, QPainter, QLinearGradient, QBrush, QPalette

# Add project root to the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from lang.lang_manager import get_string as tr
except ImportError:
    # Fallback if lang module is not found
    def tr(key: str, *args, **kwargs) -> str:
        return key  # Return the key as-is if translation is not available
        
class SponsorDialog(QDialog):
    """Dialog for displaying sponsorship options and donation information."""
    
    def __init__(self, parent=None, language_manager: Optional[LanguageManager] = None):
        try:
            print("Initializing SponsorDialog...")
            super().__init__(parent)
            print("Parent initialized")

            # Store reference to parent for language changes
            self._parent = parent
            
            # Initialize language manager
            self.lang_manager = language_manager or (getattr(parent, 'lang_manager', None) if parent else None) or LanguageManager()
            print(f"Language manager initialized: {type(self.lang_manager).__name__}")
            
            # If we're using a DummyLanguageManager, we'll handle language changes locally
            if not hasattr(self.lang_manager, 'language_changed'):
                print("Using local language change handling")
                self._local_language_changed = True
            else:
                self._local_language_changed = False
                print("Connecting to language manager's language_changed signal")
                self.lang_manager.language_changed.connect(self.on_language_changed)
                
            # Set up local signal for language changes if needed
            if self._local_language_changed:
                from PySide6.QtCore import Signal, QObject
                class SignalHolder(QObject):
                    language_changed = Signal(str)
                self._signal_holder = SignalHolder()
                self._signal_holder.language_changed.connect(self.on_language_changed)

            print("Setting window properties...")
            self.setMinimumSize(500, 400)
            self.setWindowModality(Qt.WindowModality.ApplicationModal)
            
            # Store QR code data
            self.qr_code_data = "47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF"
            self.qr_code_image = None

            # Initialize UI
            print("Setting up UI...")
            self.setup_ui()
            print("UI setup complete")

            # Set initial translations
            print("Setting initial translations...")
            self.retranslate_ui()
            
            # Generate QR code
            print("Generating QR code...")
            self.generate_qr_code()
            print("SponsorDialog initialization complete")
            
        except Exception as e:
            print(f"Error initializing SponsorDialog: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

    def translate(self, key: str, **kwargs) -> str:
        """Helper method to get translated text."""
        if hasattr(self, "lang_manager") and self.lang_manager:
            # Use get() method which is the correct method in LanguageManager
            return self.lang_manager.get(key, **kwargs)
        return key  # Fallback to key if no translation available

    def on_language_changed(self, lang_code: str) -> None:
        """Handle language change."""
        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        """Retranslate the UI elements."""
        self.setWindowTitle(self.translate("support_development"))

        if hasattr(self, "title_label"):
            self.title_label.setText(self.translate("support_app_name"))

        if hasattr(self, "message_label"):
            self.message_label.setText(self.translate("support_project_description"))

        if hasattr(self, "github_btn"):
            self.github_btn.setText(self.translate("github_sponsors"))
            self.github_btn.clicked.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl("https://github.com/sponsors/Nsfr750")
                )
            )

        if hasattr(self, "monero_label"):
            self.monero_label.setText(f"{self.translate('monero')}:")

        if hasattr(self, "close_btn"):
            self.close_btn.setText(self.translate("close"))

        if hasattr(self, "donate_btn"):
            self.donate_btn.setText(self.translate("donate_with_paypal"))

        if hasattr(self, "copy_monero_btn"):
            self.copy_monero_btn.setText(self.translate("copy_monero_address"))

    def generate_qr_code(self) -> None:
        """Generate QR code for the Monero address using Wand."""
        try:
            from wand.image import Image
            from wand.drawing import Drawing
            from wand.color import Color
            import io
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.qr_code_data)
            qr.make(fit=True)
            
            # Create a temporary buffer for the QR code
            buffer = io.BytesIO()
            
            # Generate QR code image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Create a Wand image from the buffer
            with Image(blob=buffer) as img:
                # Resize if needed
                img.resize(200, 200)
                
                # Convert to QPixmap
                img_buffer = io.BytesIO()
                img.save(img_buffer)
                pixmap = QPixmap()
                pixmap.loadFromData(img_buffer.getvalue())
                
                # Set the pixmap to the label
                self.qr_code_label.setPixmap(pixmap)
                self.qr_code_label.setAlignment(Qt.AlignCenter)
                self.qr_code_image = pixmap
                
        except ImportError:
            # Fallback to PIL if Wand is not available
            try:
                import PIL
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(self.qr_code_data)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")
                buffer = io.BytesIO()
                qr_img.save(buffer, format="PNG")
                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue(), "PNG")
                self.qr_code_label.setPixmap(pixmap.scaled(
                    200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.qr_code_image = pixmap
            except Exception as e:
                print(f"Error generating QR code with PIL: {str(e)}")
                if hasattr(self, 'qr_code_label'):
                    self.qr_code_label.setText("QR Code Unavailable")
                    
        except Exception as e:
            print(f"Error generating QR code with Wand: {str(e)}")
            import traceback
            traceback.print_exc()
            if hasattr(self, 'qr_code_label'):
                self.qr_code_label.setText("QR Code Generation Failed")

    def setup_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
            """
        )
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Message
        self.message_label = QLabel()
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label)

        # Create a container widget for the grid layout
        grid_container = QWidget()
        grid = QGridLayout(grid_container)

        # GitHub button
        self.github_btn = QPushButton()
        self.github_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.github_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """
        )

        # PayPal
        self.paypal_label = QLabel()
        self.paypal_label.setOpenExternalLinks(True)
        self.paypal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Monero
        monero_address = "47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF"
        self.monero_label = QLabel()
        monero_address_label = QLabel(monero_address)
        monero_address_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        monero_address_label.setStyleSheet(
            """
            QLabel {
                font-family: monospace;
                background-color: #2a2a2a;
                padding: 5px;
                border-radius: 3px;
                border: 1px solid #444;
                color: #f0f0f0;
            }
        """
        )

        # QR Code display
        self.qr_code_label = QLabel()
        self.qr_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_code_label.setToolTip(self.translate("scan_to_donate_xmr"))
        self.qr_code_label.setStyleSheet(
            """
            QLabel {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
            }
        """
        )

        # Add widgets to grid
        grid.addWidget(
            QLabel(f"<h3>{self.translate('ways_to_support')}</h3>"), 0, 0, 1, 2
        )
        grid.addWidget(self.github_btn, 1, 0, 1, 2)
        grid.addWidget(self.paypal_label, 2, 0, 1, 2)
        grid.addWidget(self.monero_label, 3, 0, 1, 2)
        grid.addWidget(monero_address_label, 4, 0, 1, 2)

        # Add QR code to the grid if it was created
        if hasattr(self, "qr_code_label") and self.qr_code_label is not None:
            # Create a container widget for the QR code with proper alignment
            qr_container = QWidget()
            qr_layout = QVBoxLayout(qr_container)
            qr_layout.addWidget(self.qr_code_label, 0, Qt.AlignmentFlag.AlignCenter)
            qr_layout.setContentsMargins(10, 10, 10, 10)

            # Add the container to the grid, spanning 5 rows (from 0 to 4)
            grid.addWidget(qr_container, 0, 2, 5, 1)

        # Add some spacing
        grid.setSpacing(10)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        # Add grid container to layout
        layout.addWidget(grid_container)

        # Other ways to help
        other_help = QTextBrowser()
        other_help.setOpenExternalLinks(True)
        other_help.setHtml(
            f"<h3>{self.translate('other_ways_to_help')}</h3>"
            f"<ul>"
            f"<li>{self.translate('star_on_github')} <a href=\"https://github.com/Nsfr750/EmailDuplicateCleaner\">GitHub</a></li>"
            f"<li>{self.translate('report_bugs')}</li>"
            f"<li>{self.translate('share_with_others')}</li>"
            f"</ul>"
        )
        other_help.setMaximumHeight(150)
        other_help.setStyleSheet(
            """
            QTextBrowser {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 4px;
                color: #f0f0f0;
            }
            a { color: #4a9cff; }
        """
        )
        layout.addWidget(other_help)

        # Button layout
        button_layout = QHBoxLayout()

        # Close button
        self.close_btn = QPushButton()
        self.close_btn.clicked.connect(self.accept)

        # Donate button
        self.donate_btn = QPushButton()
        self.donate_btn.setStyleSheet(
            """
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
        """
        )
        self.donate_btn.clicked.connect(self.open_paypal_link)

        # Copy Monero address button
        self.copy_monero_btn = QPushButton()
        self.copy_monero_btn.setStyleSheet(
            """
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
        """
        )
        self.copy_monero_btn.clicked.connect(
            lambda: self.copy_to_clipboard(monero_address)
        )

        button_layout.addWidget(self.close_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.copy_monero_btn)
        button_layout.addWidget(self.donate_btn)

        layout.addLayout(button_layout)

        # Apply dark theme
        self.apply_dark_theme()

    def apply_dark_theme(self):
        """Apply dark theme to the dialog."""
        # Set style sheet
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                padding: 5px;
            }
            QPushButton {
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 120px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
            QPushButton:disabled {
                background-color: #2a2a2a;
                color: #666;
            }
            QTextEdit, QTextBrowser {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 10px;
            }
            QScrollBar:vertical {
                border: 1px solid #555;
                background: #2b2b2b;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 0px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Set palette
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(43, 43, 43))
        palette.setColor(QPalette.WindowText, QColor(224, 224, 224))
        palette.setColor(QPalette.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipText, QColor(224, 224, 224))
        palette.setColor(QPalette.Text, QColor(224, 224, 224))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(224, 224, 224))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218).lighter())
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.LinkVisited, QColor(42, 130, 218).darker())
        self.setPalette(palette)
        
        # Set window icon if available
        try:
            from scripts.resources import resources
            self.setWindowIcon(QIcon(":/icons/app_icon.png"))
        except ImportError:
            pass

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

        # Show a temporary tooltip
        button = self.sender()
        if button:
            original_text = button.text()
            button.setText(self.translate("copied"))
            button.setStyleSheet(button.styleSheet() + "background-color: #4CAF50;")

            # Reset button text after 2 seconds
            QTimer.singleShot(2000, lambda: self.reset_button(button, original_text))

    def reset_button(self, button, text):
        """Reset button text and style."""
        button.setText(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                font-weight: bold;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #D45B1D;
            }
        """
        )
