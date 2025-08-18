# 📝 TO_DO List

## ✅ Completed in v2.5.2
- [x] Update version information in all relevant files
- [x] Fix version number display in the about dialog
- [x] Update documentation to reflect the latest changes

## ✅ Completed in v2.5.1
- [x] Fix QAction import error in PySide6 GUI
- [x] Add complete English translations
- [x] Add GPL-3.0 license file
- [x] Update version information
- [x] Improve error handling in GUI initialization

## 🔥 High Priority

### 🚀 Features

- [x] Add advanced email analysis options
  - [x] Sender analysis (top senders, domain distribution)
  - [x] Timeline analysis (emails over time, peak hours/days)
  - [x] Attachment analysis (types, sizes, frequency)
  - [x] Thread/conversation analysis
  - [x] Email size distribution
  - [x] Duplicate detection with different matching strategies
- [ ] Implement email recovery feature
- [ ] Add email export functionality (PDF, EML, CSV)
- [x] Improve performance for large email datasets
  - [x] Chunked processing
  - [x] Caching
  - [x] Parallel processing
- [ ] Implement advanced search filters (e.g., by date range, sender, attachment presence)
  - [ ] Date range filtering
  - [ ] Sender/recipient filtering
  - [ ] Attachment type filtering
  - [ ] Full-text search

### 🐛 Fixes

- [ ] Resolve remaining GUI button functionality issues
- [x] Improve error handling in web interface
- [x] Fix any remaining routing issues
- [ ] Fix dark mode inconsistencies in analysis reports

## 🏗️ Medium Priority

### 🛠️ Development

- [x] Refactor menu creation into a separate `struttura/menu.py` module.
- [ ] Add unit tests for email analysis features
- [ ] Implement proper logging for analysis operations
- [ ] Add API documentation for new analysis features

### 🎨 UI/UX

- [ ] Add loading indicators for long operations
- [ ] Add more user-friendly error messages
- [ ] Create visualization dashboard for analysis results
  - [ ] Charts for sender distribution
  - [ ] Timeline visualization
  - [ ] Attachment type pie chart
- [ ] Add export options for analysis reports (PDF, CSV, JSON)

## 📋 Low Priority

### 🛠️ Technical

- [ ] Investigate memory usage optimization
- [ ] Implement caching strategies
- [ ] Add support for encrypted email analysis

### 🌐 Localization

- [ ] Add more language translations
  - [ ] Spanish
  - [ ] French
  - [ ] German
  - [ ] Japanese
  - [ ] Russian
  - [ ] Portuguese
  - [ ] Arabic

## ✅ Done
- ✅ Initial release of all three interfaces (GUI, CLI, Web).
- ✅ Implemented core duplicate detection logic.
- ✅ Added basic logging and error handling.
- ✅ Created initial documentation.
- ✅ Implement multi-selection in GUI lists using `Shift+Arrow Keys` and `Ctrl+Arrow Keys`.
- ✅ Fixed several critical GUI bugs causing crashes and usability issues.
- ✅ Add multi-language support (English and Italian).
- ✅ Create a web interface for remote management.
- ✅ Implement email analysis features
- ✅ Add performance optimizations for large datasets
- ✅ Create analysis report generation
