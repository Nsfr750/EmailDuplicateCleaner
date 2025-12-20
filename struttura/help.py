"""
Help Dialog Module for EmailDuplicateCleaner

This module provides a modern, responsive Help dialog with tabbed interface,
dark theme, and improved content display using PySide6.

Features:
- Dark theme with smooth animations and transitions
- Tabbed interface for organized content navigation
- Responsive layout with proper scrolling and content wrapping
- Syntax highlighting for code blocks and markdown support
- Custom animated UI components with visual feedback
- Accessibility features including keyboard navigation
- Support for multiple languages through the language manager

License: GPL v3.0 (see LICENSE)
Copyright © 2024-2025 Nsfr750 - All rights reserved
"""

import sys
import os
import markdown
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any, Union, Callable

# Qt Imports
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTabWidget, QTextBrowser, QPushButton,
    QWidget, QLabel, QHBoxLayout, QScrollArea, QFrame,
    QSizePolicy, QGraphicsDropShadowEffect, QSpacerItem
)

from PySide6.QtCore import (
    Qt, QSize, QUrl, QPropertyAnimation, 
    QEasingCurve, QPoint, QRect, QObject,
    QEvent, QTimer
)

from PySide6.QtGui import (
    QTextCursor, QFont, QDesktopServices, QTextCharFormat,
    QColor, QPainter, QLinearGradient, QBrush, QPalette, 
    QPainterPath, QFontMetrics, QIcon, QPixmap, QKeyEvent,
    QPaintEvent, QMouseEvent, QResizeEvent, QShowEvent, QCloseEvent
)

# Add project root to the Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from lang.lang_manager import get_string

class AnimatedButton(QPushButton):
    """
    A modern, animated button with hover and click effects.
    
    Features:
    - Smooth color transitions on hover and click
    - Rounded corners with subtle shadows
    - Customizable colors and animations
    - Accessibility support
    """
    
    # Class constants for default styling
    NORMAL_COLOR = QColor("#4a5568")
    HOVER_COLOR = QColor("#2d3748")
    PRESSED_COLOR = QColor("#1a202c")
    TEXT_COLOR = QColor("#e2e8f0")
    ANIMATION_DURATION = 200
    BORDER_RADIUS = 6
    MIN_HEIGHT = 40
    
    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        """
        Initialize the animated button.
        
        Args:
            text: Button text
            parent: Parent widget
        """
        super().__init__(text, parent)
        
        # Animation setup
        self._animation = QPropertyAnimation(self, b"color")
        self._animation.setDuration(self.ANIMATION_DURATION)
        
        # Color states
        self._normal_color = self.NORMAL_COLOR
        self._hover_color = self.HOVER_COLOR
        self._pressed_color = self.PRESSED_COLOR
        self._current_color = self._normal_color
        self._text_color = self.TEXT_COLOR
        
        # UI Configuration
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(self.MIN_HEIGHT)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Accessibility
        self.setAccessibleName(text)
        self.setAccessibleDescription(f"Button: {text}")
    
    # Event Handlers
    def enterEvent(self, event: QEvent) -> None:
        """Handle mouse enter event with hover animation."""
        self._animate_color(self._hover_color)
        super().enterEvent(event)
    
    def leaveEvent(self, event: QEvent) -> None:
        """Handle mouse leave event with return animation."""
        self._animate_color(self._normal_color)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press with visual feedback."""
        if event.button() == Qt.LeftButton:
            self._animate_color(self._pressed_color, 100)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Handle mouse release with visual feedback."""
        if event.button() == Qt.LeftButton:
            self._animate_color(self._hover_color, 100)
        super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle keyboard interaction (Enter/Space for click)."""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space):
            self.animateClick()
        super().keyPressEvent(event)
    
    # Animation Methods
    def _animate_color(self, target_color: QColor, duration: int = None) -> None:
        """
        Animate the button's color transition.
        
        Args:
            target_color: The target color to animate to
            duration: Animation duration in milliseconds
        """
        if duration is None:
            duration = self.ANIMATION_DURATION
            
        self._animation.stop()
        self._animation.setDuration(duration)
        self._animation.setStartValue(self._current_color)
        self._animation.setEndValue(target_color)
        self._animation.valueChanged.connect(self._update_color)
        self._animation.start(QPropertyAnimation.DeleteWhenStopped)
    
    def _update_color(self, color: QColor) -> None:
        """Update the button's current color and trigger a repaint."""
        self._current_color = color
        self.update()
    
    # Rendering
    def paintEvent(self, event: QPaintEvent) -> None:
        """Render the button with custom styling and animations."""
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.Antialiasing | 
            QPainter.TextAntialiasing |
            QPainter.SmoothPixmapTransform
        )
        
        # Draw background with rounded corners
        path = QPainterPath()
        path.addRoundedRect(
            self.rect().adjusted(0.5, 0.5, -0.5, -0.5),  # Slight adjustment for crisp edges
            self.BORDER_RADIUS,
            self.BORDER_RADIUS
        )
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._current_color)
        painter.drawPath(path)
        
        # Draw text with proper alignment and padding
        text_rect = self.rect().adjusted(10, 0, -10, 0)  # Horizontal padding
        painter.setPen(self._text_color)
        
        # Configure font
        font = self.font()
        font.setBold(True)
        font.setPixelSize(14)  # Slightly larger, more readable text
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class HelpContentWidget(QWidget):
    """A scrollable widget for displaying help content with proper formatting and dark theme."""
    
    def __init__(self, content: str, parent: Optional[QWidget] = None):
        """Initialize the help content widget.
        
        Args:
            content: The help text content to display
            parent: The parent widget
        """
        super().__init__(parent)
        self._setup_ui(content)
        self._setup_styles()
    
    def _setup_ui(self, content: str):
        """Set up the user interface with modern design."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 10, 5, 10)  # Add some padding around the content
        layout.setSpacing(5)  # Spacing between elements
        
        # Create a text browser for the content
        self.text_browser = QTextBrowser()
        self.text_browser.setObjectName("helpContent")
        self.text_browser.setReadOnly(True)
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setHtml(self._format_content(content))
        self.text_browser.setFrameShape(QTextBrowser.NoFrame)
        self.text_browser.viewport().setAutoFillBackground(False)
        
        # Add to layout
        layout.addWidget(self.text_browser)
        layout.addStretch()
    
    def _format_content(self, content: str) -> str:
        """Format the help content as HTML with dark theme styling."""
        # Convert markdown to HTML if markdown is installed
        try:
            # Try to convert markdown to HTML
            html_content = markdown.markdown(
                content,
                extensions=[
                    'fenced_code',
                    'tables',
                    'toc',
                    'sane_lists',
                    'nl2br',
                    'mdx_breakless_lists'
                ]
            )
        except:
            # Fallback to simple conversion if markdown is not available
            html_content = content.replace('\n', '<br>')
        
        # Dark theme CSS
        css = """
        <style>
            body {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 15px;  /* Slightly larger base font size */
                line-height: 1.8;  /* Increased line height for better readability */
                color: #e2e8f0;
                background-color: transparent;
                padding: 0;
                margin: 0 0 0 5px;  /* Small left margin for text alignment */
                max-width: 900px;  /* Limit line length for better readability */
                margin: 0 auto;  /* Center content */
            }
            h1 {
                color: #f7fafc;
                font-size: 28px;  /* Larger heading */
                font-weight: 600;
                margin: 0 0 25px 0;  /* More bottom margin */
                padding: 10px 0 15px 0;  /* More vertical padding */
                border-bottom: 1px solid #3a4556;  /* Slightly lighter border */
                line-height: 1.3;  /* Tighter line height for headings */
            }
            h2 {
                color: #90cdf4;
                font-size: 22px;  /* Slightly larger */
                font-weight: 600;
                margin: 1.8em 0 1em 0;  /* More vertical spacing */
                padding-top: 10px;  /* Extra space above */
                line-height: 1.3;
            }
            h3 {
                color: #a0aec0;
                font-size: 18px;  /* Slightly larger */
                font-weight: 600;
                margin: 1.6em 0 0.9em 0;  /* More vertical spacing */
                padding-top: 8px;  /* Extra space above */
                line-height: 1.35;
            }
            p {
                margin: 1.2em 0;  /* More vertical space between paragraphs */
                line-height: 1.8;  /* Increased line height */
                padding: 0 5px;  /* Small horizontal padding */
            }
            code {
                font-family: 'Cascadia Code', 'Consolas', 'Monaco', monospace;
                background-color: #2d3748;
                color: #f6ad55;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 0.9em;
                border: 1px solid #4a5568;
            }
            pre {
                background-color: #1a202c;
                border: 1px solid #2d3748;
                border-radius: 8px;  /* Slightly rounder corners */
                padding: 16px 18px;  /* More padding */
                margin: 1.5em 0;  /* More vertical space */
                overflow-x: auto;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);  /* Deeper shadow */
            }
            pre code {
                background-color: transparent;
                border: none;
                padding: 0;
                color: #e2e8f0;
                font-size: 0.9em;
                line-height: 1.6;
            }
            blockquote {
                margin: 1.8em 0;  /* More vertical space */
                padding: 1.2em 1.5em;  /* More padding */
                border-left: 5px solid #4a5568;  /* Thicker border */
                color: #a0aec0;
                background-color: rgba(74, 85, 104, 0.12);  /* Slightly more visible */
                border-radius: 0 6px 6px 0;  /* Slightly rounder corners */
                font-style: italic;
                line-height: 1.7;  /* Better line height */
            }
            a {
                color: #63b3ed;
                text-decoration: none;
                font-weight: 500;
                transition: color 0.2s;
            }
            a:hover {
                color: #90cdf4;
                text-decoration: underline;
            }
            .note, .tip, .warning, .danger {
                padding: 18px 22px;  /* More padding */
                margin: 2em 0;  /* More vertical space */
                border-radius: 0 6px 6px 0;  /* Slightly rounder corners */
                line-height: 1.8;  /* Better line height */
            }
            
            .note, .tip {
                background-color: rgba(66, 153, 225, 0.12);  /* Slightly more visible */
                border-left: 5px solid #4299e1;  /* Thicker border */
            }
            .warning {
                background-color: rgba(237, 137, 54, 0.12);  /* Slightly more visible */
                border-left: 5px solid #ed8936;  /* Thicker border */
            }
            .danger {
                background-color: rgba(229, 62, 62, 0.12);  /* Slightly more visible */
                border-left: 5px solid #e53e3e;  /* Thicker border */
                background-color: rgba(229, 62, 62, 0.1);
                border-left: 4px solid #e53e3e;
                padding: 14px;
                margin: 1.5em 0;
                border-radius: 0 4px 4px 0;
            }
            ul, ol {
                margin: 1.2em 0 1.2em 1em;  /* More vertical space */
                padding-left: 2.2em;  /* Slightly more indentation */
            }
            
            li {
                margin: 0.6em 0;  /* More space between list items */
                line-height: 1.7;  /* Better line height for list items */
                padding: 0 5px;  /* Small horizontal padding */
            }
            
            /* Better spacing for nested lists */
            li ul, li ol {
                margin: 0.6em 0 0.6em 1em;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 1.5em 0;
                background-color: #1a202c;
                border: 1px solid #2d3748;
                border-radius: 6px;
                overflow: hidden;
            }
            th, td {
                border: 1px solid #2d3748;
                padding: 10px 12px;
                text-align: left;
            }
            th {
                background-color: #2d3748;
                color: #f7fafc;
                font-weight: 600;
            }
            tr:nth-child(even) {
                background-color: rgba(255, 255, 255, 0.02);
            }
            img {
                max-width: 100%;
                height: auto;
                border-radius: 4px;
                margin: 1em 0;
            }
            hr {
                border: none;
                height: 1px;
                background-color: #2d3748;
                margin: 2em 0;
            }
        </style>
        """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            {css}
        </head>
        <body>
            <div class="markdown-body">
                {html_content}
            </div>
        </body>
        </html>
        """
    
    def _setup_styles(self):
        """Set up the widget styles with modern dark theme."""
        self.setStyleSheet("""
            #contentContainer {
                background-color: transparent;
            }
            #helpContent {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #1a202c;
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #4a5568;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #718096;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical {
                height: 0;
                background: none;
            }""")


class HelpDialog(QDialog):
    """A modern help dialog with tabbed interface and dark theme."""
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the help dialog with modern styling.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        self.setWindowTitle(get_string('help_title'))
        self.setMinimumSize(900, 650)
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
        
        # Container widget for the content
        container = QWidget()
        container.setObjectName("container")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Create header with title and close button
        header = QWidget()
        header.setObjectName("header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 15, 15)
        
        # Title
        title_label = QLabel(get_string('help_title'))
        title_label.setObjectName("titleLabel")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setObjectName("closeButton")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        
        # Add to header
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("tabWidget")
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(False)
        
        # Add tabs with sample content
        self._add_tab('getting_started', '🚀 Getting Started', """
        # Getting Started with Email Duplicate Cleaner

        Welcome to Email Duplicate Cleaner! This guide will help you get started with the application.

        ## First Steps
        1. **Choose a mode**: GUI, Web, or CLI
        2. **Scan** for duplicate emails using your preferred criteria
        3. **Review** the results and previews
        4. **Remove** unwanted duplicates safely

        ## Features
        - Fast duplicate detection using advanced algorithms
        - Multiple selection options for precise control
        - Preview emails before deletion
        - Customizable search criteria (strict, content, headers, subject-sender)
        - Batch processing for large email collections

        > **Note:** Always back up your emails before performing any cleanup operations.
        """)
        
        self._add_tab('faq', '❓ FAQ', """
        # Frequently Asked Questions
        
        ## General
        
        ### How do I import my emails?
        You can import emails by going to `File > Import` and selecting your email file or connecting to your email account.
        
        ### Is my data secure?
        Yes, your data is processed locally and never sent to any external servers. We take your privacy seriously.
        
        ## Troubleshooting
        
        ### The application is running slowly
        Try these optimizations:
        - Reduce the number of emails you're scanning at once
        - Adjust the search criteria to be more specific
        - Close other memory-intensive applications
        - Allocate more memory to the application in settings
        
        ### I can't find my emails
        Make sure you've:
        1. Selected the correct file format
        2. Checked that the file isn't corrupted
        3. Verified file permissions
        4. Confirmed the file contains valid email data
        
        ## Performance Tips
        
        - Use the preview feature before running full scans
        - Schedule large operations during off-hours
        - Regularly clean up temporary files
        - Keep your application updated to the latest version
        """)
        
        self._add_tab('contact', '📞 Contact & Support', """
        # Contact & Support

        If you need further assistance with Email Duplicate Cleaner, please use the channels below.

        ## Email Support
        [Support](mailto:info@tuxxle.org)

        ## Documentation
        Visit the project documentation and README on GitHub:
        - [Project README](https://github.com/Nsfr750/EmailDuplicateCleaner#readme)
        - [Docs folder](https://github.com/Nsfr750/EmailDuplicateCleaner/tree/master/docs)

        ## Community & Issues
        - [GitHub Issues](https://github.com/Nsfr750/EmailDuplicateCleaner/issues)
        - [GitHub Sponsors](https://github.com/sponsors/Nsfr750)

        ## Notes
        - Please include details about your OS, Python version and application version (2.5.2) when reporting issues.
        """)
        
        # Add tab widget to layout
        container_layout.addWidget(header)
        container_layout.addWidget(self.tab_widget)
        
        # Add container to main layout
        main_layout.addWidget(container)
    
    def _add_tab(self, tab_id: str, title: str, content: str):
        """Add a tab to the help dialog with the specified content.
        
        Args:
            tab_id: Unique identifier for the tab
            title: Display title of the tab
            content: Markdown formatted content
        """
        # Create the help content widget with dark theme
        help_content = HelpContentWidget(content)
        
        # Add the tab with the help content
        self.tab_widget.addTab(help_content, title)
    
    def _setup_styles(self):
        """Set up the dialog styles with modern dark theme."""
        self.setStyleSheet("""
            #container {
                background-color: #1a202c;
                border-radius: 12px;
                border: 1px solid #2d3748;
            }
            #header {
                border-bottom: 1px solid #2d3748;
            }
            #titleLabel {
                color: #f7fafc;
                font-size: 16px;
                font-weight: 600;
            }
            #closeButton {
                background-color: transparent;
                color: #a0aec0;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                padding: 4px 8px;
            }
            #closeButton:hover {
                background-color: rgba(255, 255, 255, 0.05);
                color: #e2e8f0;
            }
            #closeButton:pressed {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QTabWidget::pane {
                border: none;
                background: transparent;
                margin: 0;
                padding: 0;
            }
            QTabBar::tab {
                background-color: #2d3748;
                color: #a0aec0;
                border: none;
                border-bottom: 2px solid transparent;
                padding: 10px 16px;
                margin-right: 4px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #2d3748;
                color: #f7fafc;
                border-bottom: 2px solid #4299e1;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
                background-color: #1a202c;
            }
            QTabBar::tab:hover:!selected {
                background-color: #2d3748;
                color: #e2e8f0;
            }
            QTabBar::tab:first-child {
                margin-left: 20px;
            }
            QTabBar::tab:last-child {
                margin-right: 0;
            }
            QTabBar::tab-bar {
                left: 0;
                background-color: #1a202c;
                border-bottom: 1px solid #2d3748;
            }
            QTabBar QToolButton {
                background-color: #2d3748;
                color: #a0aec0;
                border: none;
                border-radius: 4px;
                margin: 4px 2px;
                padding: 4px 8px;
            }
            QTabBar QToolButton:hover {
                background-color: #4a5568;
                color: #e2e8f0;
            }
            QTabBar QToolButton::right-arrow {
                image: url(:/qss_icons/rc/right_arrow.png);
            }
            QTabBar QToolButton::left-arrow {
                image: url(:/qss_icons/rc/left_arrow.png);
            }""")
        
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


class Help:
    """Helper class to show the help dialog."""
    
    @staticmethod
    def show_help(parent: Optional[QWidget] = None):
        """Show the help dialog.
        
        Args:
            parent: The parent widget for the dialog.
        """
        dialog = HelpDialog(parent)
        dialog.exec_()
