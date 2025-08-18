"""
About Dialog for Email Duplicate Cleaner

This module provides a modern, responsive 'About' dialog that displays
application information, version, and copyright details with a sleek dark theme.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List, Tuple

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QWidget, QSizePolicy, QGraphicsDropShadowEffect, QSpacerItem,
    QSizePolicy as QSP, QFrame
)
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import (
    QPixmap, QIcon, QFont, QColor, QPainter, QLinearGradient, QBrush,
    QPalette, QPainterPath, QFontMetrics
)

# Add project root to the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from struttura.version import __version__
from lang.lang_manager import get_string

class AnimatedButton(QPushButton):
    """Custom button with hover and click animations using stylesheet."""
    
    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self._normal_style = """
            QPushButton {
                background-color: #4a5568;
                color: #e2e8f0;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #2d3748;
            }
            QPushButton:pressed {
                background-color: #1a202c;
            }
        """
        self.setStyleSheet(self._normal_style)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    
    def enterEvent(self, event):
        # Hover effect is handled by stylesheet
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        # Hover effect is handled by stylesheet
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        # Pressed effect is handled by stylesheet
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        # Pressed effect is handled by stylesheet
        super().mouseReleaseEvent(event)


class AboutDialog(QDialog):
    """A modern 'About' dialog with dark theme and smooth animations."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the about dialog with modern styling."""
        super().__init__(parent)
        self.setWindowTitle(get_string('about'))
        self.setMinimumSize(500, 450)
        self.setWindowFlags(
            self.windowFlags() & 
            ~Qt.WindowContextHelpButtonHint |
            Qt.WindowSystemMenuHint |
            Qt.WindowCloseButtonHint
        )
        
        # Set window attributes for modern look
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowModality(Qt.ApplicationModal)
        
        self._setup_ui()
        self._setup_styles()
    
    def _setup_ui(self):
        """Set up the user interface with modern design."""
        # Main layout with shadow effect container
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        # Create container widget for the content
        container = QWidget()
        container.setObjectName("aboutContainer")
        container.setStyleSheet("""
            #aboutContainer {
                background-color: #1a202c;
                border-radius: 12px;
                border: 1px solid #2d3748;
            }
        """)
        
        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        container.setGraphicsEffect(shadow)
        
        # Main content layout
        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(30, 30, 30, 25)
        content_layout.setSpacing(20)
        
        # Logo and title section
        logo_title_layout = QVBoxLayout()
        logo_title_layout.setAlignment(Qt.AlignCenter)
        logo_title_layout.setSpacing(15)
        
        # Load and display logo
        logo_path = project_root / "assets" / "email.png"
        if logo_path.exists():
            logo_label = QLabel()
            logo_pixmap = QPixmap(str(logo_path))
            # Scale logo to a reasonable size while maintaining aspect ratio
            logo_pixmap = logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            logo_title_layout.addWidget(logo_label)
        
        # App title and version
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)
        
        self.title_label = QLabel("Email Duplicate Cleaner")
        self.title_label.setStyleSheet("""
            QLabel {
                color: #f7fafc;
                font-size: 24px;
                font-weight: 600;
            }
        """)
        
        self.version_label = QLabel(f"Version {__version__}")
        self.version_label.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 14px;
            }
        """)
        
        title_layout.addWidget(self.title_label, 0, Qt.AlignCenter)
        title_layout.addWidget(self.version_label, 0, Qt.AlignCenter)
        
        logo_title_layout.addLayout(title_layout)
        content_layout.addLayout(logo_title_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            QFrame {
                border: none;
                border-top: 1px solid #2d3748;
                margin: 10px 0;
            }
        """)
        content_layout.addWidget(separator)
        
        # Description
        description = QLabel(
            "A powerful tool to find and remove duplicate emails from your mailbox. "
            "Save space and keep your inbox organized with intelligent duplicate detection."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("""
            QLabel {
                color: #cbd5e0;
                font-size: 14px;
                line-height: 1.5;
                padding: 10px 0;
            }
        """)
        content_layout.addWidget(description)
        
        # Features section
        features_label = QLabel("Key Features:")
        features_label.setStyleSheet("""
            QLabel {
                color: #f7fafc;
                font-size: 16px;
                font-weight: 600;
                margin-top: 10px;
            }
        """)
        content_layout.addWidget(features_label)
        
        features = [
            "• Fast and accurate duplicate detection",
            "• Multiple selection options for precise control",
            "• Preview emails before deletion",
            "• Customizable search criteria",
            "• Batch processing for large email collections"
        ]
        
        for feature in features:
            label = QLabel(feature)
            label.setStyleSheet("""
                QLabel {
                    color: #cbd5e0;
                    font-size: 13px;
                    padding: 4px 0;
                }
            """)
            content_layout.addWidget(label)
        
        # Spacer
        content_layout.addSpacerItem(QSpacerItem(20, 20, QSP.Minimum, QSP.Expanding))
        
        # Copyright and credits
        copyright_label = QLabel(
            f"© 2025 Nsfr750\n"
            f"All rights reserved."
        )
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 12px;
                margin-top: 20px;
                line-height: 1.4;
            }
        """)
        content_layout.addWidget(copyright_label)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.close_button = AnimatedButton("Close")
        self.close_button.setFixedWidth(120)
        self.close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.close_button)
        button_layout.addStretch()
        
        content_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(container)
        
        # Set window size policy
        self.setMinimumSize(500, 600)
        self.setMaximumSize(700, 800)
        self.resize(550, 700)
    
    def _setup_styles(self):
        """Apply modern styling to the dialog."""
        self.setStyleSheet("""
            #container {
                background-color: #1a202c;
                border-radius: 12px;
                border: 1px solid #2d3748;
            }
            
            #logoLabel {
                font-size: 64px;
                margin-bottom: 10px;
            }
            
            #titleLabel {
                color: #f7fafc;
                font-size: 24px;
                font-weight: 600;
                margin-bottom: 5px;
            }
            
            #versionLabel {
                color: #a0aec0;
                font-size: 14px;
                margin-bottom: 15px;
            }
            
            #descriptionLabel {
                color: #a0aec0;
                font-size: 14px;
                line-height: 1.5;
                margin-bottom: 20px;
            }
            
            #featureLabel {
                color: #cbd5e0;
                font-size: 13px;
                padding: 5px 0;
            }
            
            #copyrightLabel {
                color: #718096;
                font-size: 11px;
                margin: 10px 0;
            }
            
            #closeButton {
                text-align: center;
                margin-top: 10px;
                padding: 10px 30px;
                border-radius: 6px;
                font-weight: 500;
            }
        """)
        
        # Add drop shadow effect
        self.setGraphicsEffect(self._create_shadow_effect())
    
    def _create_shadow_effect(self):
        """Create a drop shadow effect for the dialog."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        return shadow
    
    def showEvent(self, event):
        """Handle show event with fade-in animation."""
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()
        super().showEvent(event)
    
    def closeEvent(self, event):
        """Handle close event with fade-out animation."""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(150)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(super().close)
        self.animation.start()
        event.ignore()  # Prevent immediate close

class About:
    """Helper class to show the about dialog."""
    
    @staticmethod
    def show_about(parent: Optional[QWidget] = None):
        """Show the about dialog.
        
        Args:
            parent: The parent widget for the dialog.
        """
        dialog = AboutDialog(parent)
        dialog.exec_()
