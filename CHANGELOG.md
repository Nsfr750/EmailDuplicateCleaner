# 📋 Changelog

All notable changes to Email Duplicate Cleaner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 🚀 [2.5.0] - 2025-06-27

### 🆕 Added

- ✨ **Email Analysis Features**:
  - Added comprehensive email analysis capabilities
  - New Analysis tab in the UI with multiple analysis types:
    - Sender analysis (top senders and domains)
    - Timeline analysis (email patterns over time)
    - Attachment analysis (file types, sizes, frequencies)
    - Thread analysis (conversation threads)
    - Duplicate analysis (detailed insights)
  - Export analysis reports in multiple formats (Text, HTML, JSON)
  - Support for both English and Italian languages

### 🔧 Changed

- ⬆️ Updated version to 2.5.0
- 🌐 Added new UI strings for the analysis features
- 📊 Enhanced README with new analysis capabilities

## 🚀 [2.4.0] - 2025-06-18

### 🐛 Fixed

- 🌐 Web Interface:
  - Resolved critical routing errors by adding missing `@app.route` decorators to all API endpoints
  - Corrected a JavaScript typo (`hystoryTab` -> `historyTab`) that prevented the history tab from functioning
  - Improved template handling to prevent unnecessary file operations
  - Strengthened error handling within API endpoints to provide clearer feedback
  - Ensured proper database session management to prevent resource leaks

## 🚀 [2.3.0] - 2025-05-20 (Stable)

### 🆕 Added

- 🌐 Modern Web Interface:
  - Fully responsive web interface built with Flask
  - Dark/light mode toggle
  - Real-time updates and interactive previews
- 📚 Comprehensive Help System:
  - Dynamic help content with multiple sections
  - Integrated into GUI menu
  - Detailed documentation for all features
- 🛠️ Development Tools:
  - Enhanced testing framework
  - Improved code formatting tools
  - Better type checking

### 🔧 Changed

- 🏗️ Architecture:
  - Complete rewrite of web interface
  - Improved database management with SQLAlchemy
  - Enhanced error handling throughout the application
- 📦 Dependencies:
  - Updated Flask and related packages
  - Added new development tools
  - Improved package management

### 🐛 Fixed

- 🔍 Web Interface:
  - Resolved routing issues
  - Fixed template rendering problems
  - Improved state management
- 🖥️ UI/UX:
  - Enhanced dark mode implementation
  - Fixed layout inconsistencies
  - Improved form handling

### 🔬 Technical Enhancements

- Performance improvements
- Better memory management
- Enhanced logging system
- Improved test coverage

## 🚀 [2.2.4] - 2025-05-15 (Beta)

### 🆕 Added

- 📄 Separate modular components:
  - `about.py`: Dedicated About dialog module
  - `sponsor.py`: Comprehensive sponsor information module
  - `version.py`: Advanced version management system
- 🌐 Enhanced documentation
  - Improved README with detailed project information
  - Added badges and shields

### 🔧 Changed

- 🏗️ Architectural Improvements:
  - Refactored GUI code for better modularity
  - Improved code organization
  - Enhanced separation of concerns
- 📊 Version management:
  - Updated to version 2.2.4
  - Implemented more robust version compatibility checks

### 🐛 Fixed

- 🔍 Version Management:
  - Resolved syntax errors in version compatibility functions
  - Improved error handling mechanisms
- 🖥️ UI Stability:
  - Minor bug fixes in GUI components
  - Enhanced error reporting

### 🔬 Technical Enhancements
- Improved type hinting
- Enhanced logging capabilities
- Optimized import structures

## 🌟 [2.2.3] - 2025-05-10

### 🆕 Added
- 🚀 Initial release of Email Duplicate Cleaner
- 📧 Core Functionality:
  - Email scanning engine
  - Duplicate removal capabilities
- 🌐 Multi-client Support:
  - Thunderbird
  - Apple Mail
  - Microsoft Outlook
  - Generic mbox/maildir formats

## 🔧 [2.2.2] - 2025-05-05

### 🆕 Added
- 🌓 Dark mode support
- 🐞 Enhanced debugging capabilities
- 🚀 Performance optimizations

### 🔧 Changed
- 🎨 Improved user interface
- 📊 Refined duplicate detection algorithms

## 🐞 [2.2.1] - 2025-04-25

### 🔧 Fixed
- 🐛 Minor bug fixes
- 🚀 Performance improvements
- 🔍 Stability enhancements

## 🎉 [2.2.0] - 2025-04-15

### 🆕 Added
- 🚀 Initial beta release
- 🔍 Core duplicate detection functionality
- 🌐 Basic multi-interface support

### 🔬 Notes
- 🧪 Experimental features
- 🚧 Ongoing development

---

🔍 **Legend**:
- 🆕 Added
- 🔧 Changed
- 🐛 Fixed
- 🚀 New Feature
- 🌐 Improvement

## [1.2.0-rc] - 2025-06-19

### Added
- **GUI**: Added multi-selection of mailboxes and folders using `Shift+Arrow Keys` and `Ctrl+Arrow Keys` for a more efficient workflow.

### Fixed
- **GUI**: Fixed a `_tkinter.TclError` crash caused by mixing `pack` and `grid` geometry managers within the same frame.
- **GUI**: Fixed an `AttributeError` on startup by ensuring event bindings are set only after the corresponding widgets have been created.
- **GUI**: Restored automatic scrolling to ensure the active item is always visible when navigating lists with the keyboard.
- **GUI**: Corrected an `IndentationError` that prevented the application from starting.

## [Unreleased]

### Added
- New `AppMenu` class in `struttura/menu.py` to handle menu creation and management.
- Dynamic language switching for all menu and UI elements.

### Changed
- **Refactored** GUI menu creation by detaching it from `email_cleaner_gui.py` and moving it to `struttura/menu.py`.
- Updated all auxiliary windows (`About`, `Help`, `Sponsor`) to be Toplevel subclasses with static `show` methods.
- Replaced local frames with `LabelFrame` widgets in the Scan tab for better UI organization.

### Fixed
- `NameError` in `struttura/menu.py` caused by incorrect variable scope.
- `AttributeError` in `email_cleaner_gui.py` during language switching due to typos and incorrect widget references.
- `TabError` in `struttura/menu.py` due to inconsistent indentation.
- `SyntaxError` in `struttura/about.py`.
- Missing and incorrect translation keys in `lang/lang.py`.

## [2.2.1] - 2025-04-25

### Fixed
- Minor bug fixes
- Performance improvements

## [2.2.0] - 2025-04-15

### Added
- Initial beta release
- Core email duplicate detection functionality
