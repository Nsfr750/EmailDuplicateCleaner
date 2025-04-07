#!/usr/bin/env python3
"""
Email Duplicate Cleaner - Web Interface

A web-based interface for the Email Duplicate Cleaner tool.
This interface provides easy access to the functionality for scanning and removing
duplicate emails from various email clients.

©2025 by Nsfr750
"""

import os
import sys
import json
import threading
import tempfile
import shutil
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import logging
from io import StringIO

# Import the core functionality from the CLI version
from email_duplicate_cleaner import (
    EmailClientManager, DuplicateEmailFinder, create_test_mailbox,
    BaseEmailClientHandler, ThunderbirdMailHandler, AppleMailHandler,
    OutlookHandler, GenericMailHandler
)

# Import database functions
from db_init import (
    create_app, init_db, add_scan_history, add_clean_record, 
    get_user_settings, update_user_settings, get_scan_history
)
from flask import redirect, url_for
from models import ScanHistory, EmailCleanRecord, UserSettings

# Create Flask app
app = create_app()  # Use the app from db_init that has database setup

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
global_state = {
    'client_manager': EmailClientManager(),
    'duplicate_finder': DuplicateEmailFinder(),
    'mail_folders': [],
    'selected_folders': [],
    'duplicate_groups': [],
    'scan_thread': None,
    'clean_thread': None,
    'temp_dir': None,
    'log_buffer': StringIO(),
    'scanning': False,
    'cleaning': False,
    'scan_complete': False
}

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# Create static directory if it doesn't exist
os.makedirs('static', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# Initialize database
with app.app_context():
    init_db()

# Create HTML templates
with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Duplicate Cleaner</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
            <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
                <span class="fs-4">Email Duplicate Cleaner</span>
            </a>
            <ul class="nav nav-pills">
                <li class="nav-item"><a href="#" class="nav-link active" id="scan-tab">Scan</a></li>
                <li class="nav-item"><a href="#" class="nav-link" id="results-tab">Results</a></li>
                <li class="nav-item"><a href="#" class="nav-link" id="history-tab">History</a></li>
                <li class="nav-item"><a href="#" class="nav-link" id="settings-tab">Settings</a></li>
                <li class="nav-item"><a href="#" class="nav-link" id="help-tab">Help</a></li>
            </ul>
        </header>

        <main>
            <div class="tab-content">
                <!-- Scan Tab -->
                <div class="tab-pane active" id="scan-content">
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <h5>Email Client Selection</h5>
                                </div>
                                <div class="card-body">
                                    <form id="scan-form">
                                        <div class="mb-3">
                                            <label class="form-label">Email Client:</label>
                                            <div class="btn-group" role="group">
                                                <input type="radio" class="btn-check" name="client" id="all" value="all" checked>
                                                <label class="btn btn-outline-primary" for="all">All Clients</label>

                                                <input type="radio" class="btn-check" name="client" id="thunderbird" value="thunderbird">
                                                <label class="btn btn-outline-primary" for="thunderbird">Thunderbird</label>

                                                <input type="radio" class="btn-check" name="client" id="apple_mail" value="apple_mail">
                                                <label class="btn btn-outline-primary" for="apple_mail">Apple Mail</label>

                                                <input type="radio" class="btn-check" name="client" id="outlook" value="outlook">
                                                <label class="btn btn-outline-primary" for="outlook">Outlook</label>

                                                <input type="radio" class="btn-check" name="client" id="generic" value="generic">
                                                <label class="btn btn-outline-primary" for="generic">Generic</label>
                                            </div>
                                        </div>

                                        <div class="mb-3">
                                            <label class="form-label">Detection Criteria:</label>
                                            <div class="btn-group" role="group">
                                                <input type="radio" class="btn-check" name="criteria" id="strict" value="strict" checked>
                                                <label class="btn btn-outline-primary" for="strict">Strict</label>

                                                <input type="radio" class="btn-check" name="criteria" id="content" value="content">
                                                <label class="btn btn-outline-primary" for="content">Content Only</label>

                                                <input type="radio" class="btn-check" name="criteria" id="headers" value="headers">
                                                <label class="btn btn-outline-primary" for="headers">Headers</label>

                                                <input type="radio" class="btn-check" name="criteria" id="subject-sender" value="subject-sender">
                                                <label class="btn btn-outline-primary" for="subject-sender">Subject+Sender</label>
                                            </div>
                                        </div>

                                        <div class="mb-3">
                                            <div class="form-check">
                                                <input class="form-check-input" type="checkbox" id="auto-clean" name="auto-clean">
                                                <label class="form-check-label" for="auto-clean">
                                                    Auto-clean (keep oldest emails)
                                                </label>
                                            </div>
                                        </div>

                                        <div class="d-flex justify-content-between">
                                            <button type="button" id="find-folders-btn" class="btn btn-primary">Find Folders</button>
                                            <button type="button" id="custom-folder-btn" class="btn btn-secondary">Custom Folder</button>
                                            <button type="button" id="demo-btn" class="btn btn-info">Run Demo</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row mb-3">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header d-flex justify-content-between align-items-center">
                                    <h5>Mail Folders</h5>
                                    <div>
                                        <button type="button" id="select-all-btn" class="btn btn-sm btn-outline-secondary">Select All</button>
                                        <button type="button" id="scan-selected-btn" class="btn btn-sm btn-success">Scan Selected</button>
                                    </div>
                                </div>
                                <div class="card-body">
                                    <div class="folder-list" id="folder-list">
                                        <div class="alert alert-info">Click "Find Folders" to search for mail folders.</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="row">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <h5>Console Output</h5>
                                </div>
                                <div class="card-body">
                                    <pre id="console-output" class="console-output bg-dark text-light p-3 rounded"></pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Results Tab -->
                <div class="tab-pane" id="results-content">
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header d-flex justify-content-between align-items-center">
                                    <h5>Duplicate Groups</h5>
                                    <div>
                                        <button type="button" id="clean-selected-btn" class="btn btn-sm btn-warning">Clean Selected</button>
                                        <button type="button" id="clean-all-btn" class="btn btn-sm btn-danger">Clean All</button>
                                    </div>
                                </div>
                                <div class="card-body" id="results-container">
                                    <div class="alert alert-info">Scan mail folders to find duplicates.</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Help Tab -->
                <div class="tab-pane" id="help-content">
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <h5>Help & Documentation</h5>
                                </div>
                                <div class="card-body">
                                    <h4>Email Duplicate Cleaner</h4>
                                    <p>This tool helps you find and remove duplicate emails from various email clients.</p>

                                    <h5>Using the Web Interface</h5>
                                    <ol>
                                        <li>Select an email client or "All Clients"</li>
                                        <li>Choose duplicate detection criteria</li>
                                        <li>Click "Find Folders" to locate mail folders</li>
                                        <li>Select folders you want to scan</li>
                                        <li>Click "Scan Selected" to find duplicates</li>
                                        <li>Review duplicate groups in the Results tab</li>
                                        <li>Select groups and click "Clean Selected" or "Clean All" to remove duplicates</li>
                                    </ol>

                                    <h5>Detection Criteria</h5>
                                    <ul>
                                        <li><strong>Strict:</strong> Uses Message-ID, Date, From, Subject, and content</li>
                                        <li><strong>Content Only:</strong> Only compares message content</li>
                                        <li><strong>Headers:</strong> Uses Message-ID, Date, From, and Subject</li>
                                        <li><strong>Subject+Sender:</strong> Only compares Subject and From fields</li>
                                    </ul>

                                    <div class="alert alert-warning">
                                        <strong>Note:</strong> The tool always keeps at least one copy of each email.
                                        Always backup your email client's data files before using this tool on real emails.
                                    </div>

                                    <h5>Demo Mode</h5>
                                    <p>Click "Run Demo" to create a temporary mailbox with sample emails containing duplicates for testing.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
            <div class="col-md-6 d-flex align-items-center">
                <span class="text-muted">Email Duplicate Cleaner v2.0.1 &copy; 2025 by Nsfr750 </span>
                <span class="text-muted"> - <a href="https://patreon.com/Nsfr750?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink
" target="_blank">Patreon</a> - <a href="https://github.com/Nsfr750" target="_blank">GitHub</a></span>
            </div>
            <div class="col-md-6 d-flex justify-content-end">
                <span class="text-muted" id="status-text">Ready</span>
            </div>
        </footer>
    </div>

    <!-- Modals -->
    <div class="modal fade" id="customFolderModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Enter Custom Folder Path</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="custom-folder-form">
                        <div class="mb-3">
                            <label for="folder-path" class="form-label">Mail Folder Path:</label>
                            <input type="text" class="form-control" id="folder-path" required>
                            <div class="form-text">Enter the absolute path to your mail folder.</div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" id="submit-custom-folder">Search</button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="confirmModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Confirm Action</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="confirm-message">
                    Are you sure you want to continue?
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" id="confirm-action">Continue</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
''')

with open('static/css/style.css', 'w') as f:
    f.write('''
.console-output {
    max-height: 200px;
    overflow-y: scroll;
    font-family: monospace;
}

.folder-list {
    max-height: 300px;
    overflow-y: auto;
}

.duplicate-group {
    margin-bottom: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
    overflow: hidden;
}

.group-header {
    background-color: #f8f9fa;
    padding: 10px 15px;
    border-bottom: 1px solid #ddd;
}

.email-item {
    padding: 10px 15px;
    border-bottom: 1px solid #eee;
}

.email-item:hover {
    background-color: #f5f5f5;
}

.email-item.original {
    background-color: #e7f7e7;
}

.email-item:last-child {
    border-bottom: none;
}

.email-meta {
    font-size: 0.85rem;
    color: #666;
}

.email-subject {
    font-weight: bold;
}

.check-column {
    width: 40px;
}
''')

with open('static/js/script.js', 'w') as f:
    f.write('''
document.addEventListener('DOMContentLoaded', function() {
    // Tab navigation
    const scanTab = document.getElementById('scan-tab');
    const resultsTab = document.getElementById('results-tab');
    const helpTab = document.getElementById('help-tab');

    const scanContent = document.getElementById('scan-content');
    const resultsContent = document.getElementById('results-content');
	const helpContent = document.getElementById('help-content');

    // Buttons
    const findFoldersBtn = document.getElementById('find-folders-btn');
    const customFolderBtn = document.getElementById('custom-folder-btn');
    const demoBtn = document.getElementById('demo-btn');
    const selectAllBtn = document.getElementById('select-all-btn');
    const scanSelectedBtn = document.getElementById('scan-selected-btn');
    const cleanSelectedBtn = document.getElementById('clean-selected-btn');
    const cleanAllBtn = document.getElementById('clean-all-btn');
    const submitCustomFolderBtn = document.getElementById('submit-custom-folder');

    // Console output
    const consoleOutput = document.getElementById('console-output');
    const statusText = document.getElementById('status-text');

    // Bootstrap modals
    const customFolderModal = new bootstrap.Modal(document.getElementById('customFolderModal'));
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    const confirmMessage = document.getElementById('confirm-message');
    const confirmAction = document.getElementById('confirm-action');

    // Tab switching
    scanTab.addEventListener('click', function(e) {
        e.preventDefault();
        setActiveTab('scan');
    });

    resultsTab.addEventListener('click', function(e) {
        e.preventDefault();
        setActiveTab('results');
    });

    helpTab.addEventListener('click', function(e) {
        e.preventDefault();
        setActiveTab('help');
    });

    function setActiveTab(tabName) {
        // Reset all tabs
        scanTab.classList.remove('active');
        resultsTab.classList.remove('active');
        helpTab.classList.remove('active');

        scanContent.classList.remove('active');
        resultsContent.classList.remove('active');
        helpContent.classList.remove('active');

        // Set active class
        document.getElementById(tabName + '-tab').classList.add('active');
        document.getElementById(tabName + '-content').classList.add('active');
    }

    // Console polling
    function pollConsole() {
        fetch('/api/get_logs')
            .then(response => response.json())
            .then(data => {
                if (data.logs) {
                    consoleOutput.textContent = data.logs;
                    consoleOutput.scrollTop = consoleOutput.scrollHeight;
                }
                if (data.status) {
                    statusText.textContent = data.status;
                }

                // Check if scanning is complete to switch to results tab
                if (data.scan_complete) {
                    resultsTab.click();
                    updateResults();
                }
            })
            .catch(error => console.error('Error polling console:', error));
    }

    // Start console polling
    setInterval(pollConsole, 1000);

    // Find folders
    findFoldersBtn.addEventListener('click', function() {
        const client = document.querySelector('input[name="client"]:checked').value;
        setStatus('Searching for mail folders...');

        fetch('/api/find_folders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ client: client }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateFolderList(data.folders);
                setStatus(`Found ${data.folders.length} mail folders`);
            } else {
                setStatus(data.message || 'Error finding folders');
            }
        })
        .catch(error => {
            console.error('Error finding folders:', error);
            setStatus('Error: Could not find mail folders');
        });
    });

    // Custom folder modal
    customFolderBtn.addEventListener('click', function() {
        customFolderModal.show();
    });

    // Submit custom folder
    submitCustomFolderBtn.addEventListener('click', function() {
        const folderPath = document.getElementById('folder-path').value;
        if (!folderPath) {
            return;
        }

        customFolderModal.hide();

        fetch('/api/scan_custom_folder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ folder_path: folderPath }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateFolderList(data.folders);
                setStatus(`Found ${data.folders.length} mail folders in ${folderPath}`);
            } else {
                setStatus(data.message || 'Error scanning custom folder');
            }
        })
        .catch(error => {
            console.error('Error scanning custom folder:', error);
            setStatus('Error: Could not scan custom folder');
        });
    });

    // Run demo
    demoBtn.addEventListener('click', function() {
        confirmMessage.textContent = 'This will create a temporary mailbox with sample emails for demonstration. Continue?';
        confirmAction.onclick = function() {
            confirmModal.hide();

            fetch('/api/run_demo')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        updateFolderList(data.folders);
                        setStatus('Demo mode active');
                    } else {
                        setStatus(data.message || 'Error starting demo');
                    }
                })
                .catch(error => {
                    console.error('Error running demo:', error);
                    setStatus('Error: Could not start demo mode');
                });
        };
        confirmModal.show();
    });

    // Select all folders
    selectAllBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.folder-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = true;
        });
    });

    // Scan selected folders
    scanSelectedBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.folder-checkbox:checked');
        if (checkboxes.length === 0) {
            alert('Please select at least one folder to scan');
            return;
        }

        const folderIndices = Array.from(checkboxes).map(checkbox => parseInt(checkbox.value));
        const criteria = document.querySelector('input[name="criteria"]:checked').value;
        const autoClean = document.getElementById('auto-clean').checked;

        setStatus(`Scanning ${folderIndices.length} folders...`);

        fetch('/api/scan_folders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                folder_indices: folderIndices,
                criteria: criteria,
                auto_clean: autoClean
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                setStatus('Scanning in progress...');
            } else {
                setStatus(data.message || 'Error starting scan');
            }
        })
        .catch(error => {
            console.error('Error scanning folders:', error);
            setStatus('Error: Could not scan folders');
        });
    });

    // Update results
    function updateResults() {
        fetch('/api/get_results')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const resultsContainer = document.getElementById('results-container');
                    if (data.groups.length === 0) {
                        resultsContainer.innerHTML = '<div class="alert alert-info">No duplicate emails found.</div>';
                        return;
                    }

                    let html = '';
                    data.groups.forEach((group, groupIndex) => {
                        html += `
                            <div class="duplicate-group shadow-sm" data-group-index="${groupIndex}">
                                <div class="group-header d-flex justify-content-between align-items-center bg-light">
                                    <div class="d-flex align-items-center">
                                        <input type="checkbox" class="form-check-input group-checkbox ms-2" value="${groupIndex}">
                                        <span class="ms-3 fw-bold">Group ${groupIndex + 1}</span>
                                        <span class="ms-2 badge bg-primary">${group.emails.length} emails</span>
                                    </div>
                                    <button class="btn btn-sm btn-warning clean-group-btn me-2" data-group-index="${groupIndex}">
                                        <i class="fas fa-broom"></i> Clean Group
                                    </button>
                                </div>
                                <div class="email-list">`;

                        group.emails.forEach((email, emailIndex) => {
                            const isOriginal = emailIndex === 0;
                            html += `
                                <div class="email-item p-3 border-bottom ${isOriginal ? 'original bg-light' : ''} hover-highlight">
                                    <div class="d-flex">
                                        <div class="email-meta me-3 text-center">
                                            <span class="badge ${isOriginal ? 'bg-success' : 'bg-secondary'}">${emailIndex + 1}</span>
                                            ${isOriginal ? '<br><small class="text-success">Original</small>' : ''}
                                        </div>
                                        <div class="flex-grow-1">
                                            <div class="email-subject h6 mb-2">${email.subject}</div>
                                            <div class="d-flex justify-content-between align-items-center mb-2">
                                                <div class="email-meta text-muted">
                                                    <i class="fas fa-user me-1"></i> ${email.from}
                                                </div>
                                                <div class="email-meta text-muted">
                                                    <i class="fas fa-calendar me-1"></i> ${email.date}
                                                </div>
                                            </div>
                                            <div class="email-meta text-muted">
                                                <i class="fas fa-folder me-1"></i> ${email.folder_path}
                                            </div>
                                        </div>
                                    </div>
                                </div>`;
                        });

                        html += `
                                </div>
                            </div>`;
                    });

                    resultsContainer.innerHTML = html;

                    // Add listeners for individual group clean buttons
                    document.querySelectorAll('.clean-group-btn').forEach(button => {
                        button.addEventListener('click', function() {
                            const groupIndex = parseInt(button.getAttribute('data-group-index'));
                            cleanGroups([groupIndex]);
                        });
                    });

                    setStatus(`Found ${data.groups.length} duplicate groups`);
                } else {
                    setStatus(data.message || 'Error getting results');
                }
            })
            .catch(error => {
                console.error('Error getting results:', error);
                setStatus('Error: Could not load results');
            });
    }

    // Clean selected groups
    cleanSelectedBtn.addEventListener('click', function() {
        const checkboxes = document.querySelectorAll('.group-checkbox:checked');
        if (checkboxes.length === 0) {
            alert('Please select at least one group to clean');
            return;
        }

        const groupIndices = Array.from(checkboxes).map(checkbox => parseInt(checkbox.value));

        confirmMessage.textContent = `This will delete duplicates from ${groupIndices.length} selected groups, keeping the oldest email in each group. Continue?`;
        confirmAction.onclick = function() {
            confirmModal.hide();
            cleanGroups(groupIndices);
        };
        confirmModal.show();
    });

    // Clean all groups
    cleanAllBtn.addEventListener('click', function() {
        confirmMessage.textContent = 'This will delete duplicates from ALL groups, keeping the oldest email in each group. Continue?';
        confirmAction.onclick = function() {
            confirmModal.hide();

            fetch('/api/clean_all_groups')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        setStatus('Cleaning in progress...');
                    } else {
                        setStatus(data.message || 'Error cleaning groups');
                    }
                })
                .catch(error => {
                    console.error('Error cleaning all groups:', error);
                    setStatus('Error: Could not clean groups');
                });
        };
        confirmModal.show();
    });

    // Clean groups helper function
    function cleanGroups(groupIndices) {
        setStatus(`Cleaning ${groupIndices.length} groups...`);

        fetch('/api/clean_groups', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ group_indices: groupIndices }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                setStatus('Cleaning in progress...');
            } else {
                setStatus(data.message || 'Error cleaning groups');
            }
        })
        .catch(error => {
            console.error('Error cleaning groups:', error);
            setStatus('Error: Could not clean groups');
        });
    }

    // Update folder list helper function
    function updateFolderList(folders) {
        const folderList = document.getElementById('folder-list');
        if (folders.length === 0) {
            folderList.innerHTML = '<div class="alert alert-warning">No mail folders found.</div>';
            return;
        }

        let html = '<div class="list-group">';
        folders.forEach((folder, index) => {
            html += `
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="form-check">
                            <input class="form-check-input folder-checkbox" type="checkbox" value="${index}" id="folder-${index}">
                            <label class="form-check-label" for="folder-${index}">
                                ${folder.display_name}
                            </label>
                        </div>
                    </div>
                </div>`;
        });
        html += '</div>';

        folderList.innerHTML = html;
    }

    // Set status helper function
    function setStatus(message) {
        statusText.textContent = message;
    }
});
''')

# Custom stream handler to capture console output
class WebConsoleHandler:
    """Custom handler to capture console output for web display"""

    def __init__(self):
        self.buffer = StringIO()

    def write(self, message):
        if isinstance(message, bytes):
            message = message.decode('utf-8')

        if message and message.strip():  # Skip empty lines
            self.buffer.write(message)

    def flush(self):
        pass

    def get_logs(self):
        return self.buffer.getvalue()

    def clear(self):
        self.buffer = StringIO()

# Initialize console handler
console_handler = WebConsoleHandler()

# Redirect stdout for capturing application logs
original_stdout = sys.stdout
sys.stdout = console_handler

@app.route('/')
def index():
    """Render the main application page"""
    # Load user settings for default values
    with app.app_context():
        settings = get_user_settings()

    return render_template('index.html', settings=settings)

@app.route('/api/find_folders', methods=['POST'])
def api_find_folders():
    """Find mail folders for the selected email client"""
    client = request.json.get('client', 'all')

    try:
        if client == 'all':
            global_state['mail_folders'] = global_state['client_manager'].get_all_mail_folders()
        else:
            global_state['mail_folders'] = global_state['client_manager'].get_client_folders(client)

        return jsonify({
            'success': True,
            'folders': [{'display_name': folder['display_name']} for folder in global_state['mail_folders']]
        })
    except Exception as e:
        logger.error(f"Error finding folders: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error finding folders: {str(e)}"
        })

@app.route('/api/scan_custom_folder', methods=['POST'])
def api_scan_custom_folder():
    """Scan a custom folder path for mail folders"""
    folder_path = request.json.get('folder_path')

    if not folder_path or '..' in folder_path or not os.path.isabs(folder_path):
        return jsonify({
            'success': False,
            'message': 'Invalid folder path provided'
        })

    try:
        # Create a generic mail handler for this path
        custom_handler = GenericMailHandler()
        custom_handler.profile_paths = [folder_path]

        global_state['mail_folders'] = custom_handler.find_mail_folders()

        return jsonify({
            'success': True,
            'folders': [{'display_name': folder['display_name']} for folder in global_state['mail_folders']]
        })
    except Exception as e:
        logger.error(f"Error scanning custom folder: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error scanning custom folder: {str(e)}"
        })

@app.route('/api/run_demo')
def api_run_demo():
    """Run the application in demo mode with test emails"""
    try:
        print("Running in demo mode with test emails...")

        # Create test mailbox
        global_state['temp_dir'], profile_path = create_test_mailbox()

        # Set up a generic mail handler for this path
        custom_handler = GenericMailHandler()
        custom_handler.profile_paths = [profile_path]

        # Find mail folders
        global_state['mail_folders'] = custom_handler.find_mail_folders()

        return jsonify({
            'success': True,
            'folders': [{'display_name': folder['display_name']} for folder in global_state['mail_folders']]
        })
    except Exception as e:
        logger.error(f"Error setting up demo mode: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error setting up demo mode: {str(e)}"
        })

@app.route('/api/scan_folders', methods=['POST'])
def api_scan_folders():
    """Scan selected folders for duplicate emails"""
    folder_indices = request.json.get('folder_indices', [])
    criteria = request.json.get('criteria', 'strict')
    auto_clean = request.json.get('auto_clean', False)

    if not folder_indices:
        return jsonify({
            'success': False,
            'message': 'No folders selected'
        })

    try:
        # Get selected folders
        global_state['selected_folders'] = [global_state['mail_folders'][i] for i in folder_indices]

        # Reset scan state
        global_state['duplicate_groups'] = []
        global_state['scanning'] = True
        global_state['scan_complete'] = False

        # Start scanning thread
        def scan_folders_thread():
            try:
                print(f"Scanning {len(global_state['selected_folders'])} folders...")
                print(f"Using criteria: {criteria}")

                for folder in global_state['selected_folders']:
                    print(f"Scanning folder: {folder['display_name']}")
                    groups = global_state['duplicate_finder'].scan_folder(folder, criteria)

                    if groups:
                        for group in groups:
                            global_state['duplicate_groups'].append(group)

                total_dupes = sum(group['count'] - 1 for group in global_state['duplicate_groups'])
                groups_count = len(global_state['duplicate_groups'])

                print(f"Found {groups_count} duplicate groups with {total_dupes} duplicate emails")

                # Add scan to database history
                client_type = request.json.get('client', 'all')
                total_emails = sum(len(group['messages']) for group in global_state['duplicate_groups'])
                folder_paths = ', '.join([f['display_name'] for f in global_state['selected_folders']])

                # Add record to scan history
                with app.app_context():
                    scan_id = add_scan_history(
                        client_type=client_type,
                        folder_path=folder_paths,
                        criteria=criteria,
                        total_emails=total_emails,
                        duplicate_groups=groups_count,
                        duplicate_emails=total_dupes
                    )

                # Auto-clean if requested
                if auto_clean and global_state['duplicate_groups']:
                    print("Auto-cleaning duplicates...")
                    deleted, errors = global_state['duplicate_finder'].delete_duplicates(
                        list(range(len(global_state['duplicate_groups']))), selection_method='keep-first'
                    )
                    print(f"Deleted {deleted} duplicate emails")

                    if errors:
                        print("Some errors occurred during deletion:")
                        for error in errors[:5]:
                            print(f"  - {error}")
                        if len(errors) > 5:
                            print(f"  ... and {len(errors) - 5} more errors")

                    # Add cleaning record to database
                    with app.app_context():
                        add_clean_record(
                            scan_id=scan_id,
                            cleaned_count=deleted,
                            error_count=len(errors),
                            selection_method='keep-first'
                        )

                global_state['scanning'] = False
                global_state['scan_complete'] = True
            except Exception as e:
                print(f"Error scanning folders: {str(e)}")
                global_state['scanning'] = False

        global_state['scan_thread'] = threading.Thread(target=scan_folders_thread)
        global_state['scan_thread'].daemon = True
        global_state['scan_thread'].start()

        return jsonify({
            'success': True
        })
    except Exception as e:
        logger.error(f"Error starting scan: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error starting scan: {str(e)}"
        })

@app.route('/api/get_results')
def api_get_results():
    """Get scanning results"""
    try:
        groups_data = []

        for group in global_state['duplicate_groups']:
            emails_data = []

            for email in group['messages']:  # Changed from 'emails' to 'messages'
                emails_data.append({
                    'date': email.get('date', ''),
                    'from': email.get('from', ''),
                    'subject': email.get('subject', ''),
                    'folder_path': email.get('folder', '')  # Changed from folder_path to folder
                })

            groups_data.append({
                'count': len(group['messages']),  # Calculate count from messages length
                'emails': emails_data
            })

        return jsonify({
            'success': True,
            'groups': groups_data
        })
    except Exception as e:
        logger.error(f"Error getting results: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error getting results: {str(e)}"
        })

@app.route('/api/view_email/<int:group_index>/<int:email_index>', methods=['GET'])
def api_view_email(group_index, email_index):
    """Get full content of a specific email"""
    try:
        if not global_state['duplicate_groups']:
            return jsonify({
                'success': False,
                'message': 'No duplicate groups available'
            })

        if group_index < 0 or group_index >= len(global_state['duplicate_groups']):
            return jsonify({
                'success': False,
                'message': f'Invalid group index: {group_index}'
            })

        group = global_state['duplicate_groups'][group_index]

        if email_index < 0 or email_index >= group['count']:
            return jsonify({
                'success': False,
                'message': f'Invalid email index: {email_index}'
            })

        # Get the email content using DuplicateEmailFinder's method
        msg_info = group['messages'][email_index]
        message = msg_info.get('message')
        if not message:
            return {"error": "Message content not available"}

        return jsonify({
            'success': True,
            'email': message
        })
    except Exception as e:
        logger.error(f"Error viewing email: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error viewing email: {str(e)}"
        })

@app.route('/api/clean_groups', methods=['POST'])
def api_clean_groups():
    """Clean duplicates from selected groups"""
    group_indices = request.json.get('group_indices', [])

    if not group_indices:
        return jsonify({
            'success': False,
            'message': 'No groups selected'
        })

    try:
        # Start cleaning thread
        global_state['cleaning'] = True

        def clean_groups_thread():
            try:
                print(f"Cleaning {len(group_indices)} groups...")

                deleted, errors = global_state['duplicate_finder'].delete_duplicates(
                    group_indices, selection_method='keep-first'
                )

                print(f"Deleted {deleted} duplicate emails")

                if errors:
                    print("Some errors occurred during deletion:")
                    for error in errors[:5]:
                        print(f"  - {error}")
                    if len(errors) > 5:
                        print(f"  ... and {len(errors) - 5} more errors")

                # Record cleaning operation in database
                with app.app_context():
                    # Get the latest scan history record to associate with this cleaning operation
                    scan_history = get_scan_history(limit=1)
                    if scan_history:
                        scan_id = scan_history[0].id
                        add_clean_record(
                            scan_id=scan_id,
                            cleaned_count=deleted,
                            error_count=len(errors),
                            selection_method='keep-first'
                        )

                # Refresh duplicate groups
                global_state['duplicate_groups'] = []
                print("Rescanning folders after cleaning...")

                for folder in global_state['selected_folders']:
                    groups = global_state['duplicate_finder'].scan_folder(folder, 'strict')

                    if groups:
                        for group in groups:
                            global_state['duplicate_groups'].append(group)

                global_state['cleaning'] = False
            except Exception as e:
                print(f"Error cleaning groups: {str(e)}")
                global_state['cleaning'] = False

        global_state['clean_thread'] = threading.Thread(target=clean_groups_thread)
        global_state['clean_thread'].daemon = True
        global_state['clean_thread'].start()

        return jsonify({
            'success': True
        })
    except Exception as e:
        logger.error(f"Error starting cleaning: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error starting cleaning: {str(e)}"
        })

@app.route('/api/clean_all_groups')
def api_clean_all_groups():
    """Clean duplicates from all groups"""
    if not global_state['duplicate_groups']:
        return jsonify({
            'success': False,
            'message': 'No duplicate groups to clean'
        })

    try:
        all_indices = list(range(len(global_state['duplicate_groups'])))
        return api_clean_groups()
    except Exception as e:
        logger.error(f"Error cleaning all groups: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error cleaning all groups: {str(e)}"
        })

@app.route('/api/get_logs')
def api_get_logs():
    """Get console output logs"""
    status = "Ready"

    if global_state['scanning']:
        status = "Scanning in progress..."
    elif global_state['cleaning']:
        status = "Cleaning in progress..."
    elif global_state['scan_complete']:
        total_dupes = sum(group['count'] - 1 for group in global_state['duplicate_groups']) if global_state['duplicate_groups'] else 0
        status = f"Found {len(global_state['duplicate_groups'])} duplicate groups with {total_dupes} duplicate emails"

    return jsonify({
        'logs': console_handler.get_logs(),
        'status': status,
        'scan_complete': global_state['scan_complete'] and not global_state['cleaning']
    })

# Database-related routes
@app.route('/history')
def history():
    """Show scan history page"""
    with app.app_context():
        scan_history = get_scan_history(limit=50)  # Get more history entries
    return render_template('history.html', scan_history=scan_history)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Show settings page"""
    save_success = False

    if request.method == 'POST':
        # Save settings to database
        settings_dict = {
            'default_client': request.form.get('default_client', 'all'),
            'default_criteria': request.form.get('default_criteria', 'strict'),
            'auto_clean': request.form.get('auto_clean') == 'on',
            'last_custom_folder': request.form.get('last_custom_folder', '')
        }
        with app.app_context():
            update_user_settings(settings_dict)
        save_success = True

    with app.app_context():
        settings = get_user_settings()

    return render_template('settings.html', settings=settings, save_success=save_success)

@app.route('/help')
def help():
    """Show help page"""
    return render_template('help.html')

@app.route('/api/save_settings', methods=['POST'])
def api_save_settings():
    """Save user settings API endpoint"""
    settings_dict = {
        'default_client': request.form.get('default_client', 'all'),
        'default_criteria': request.form.get('default_criteria', 'strict'),
        'auto_clean': request.form.get('auto_clean') == 'on',
        'last_custom_folder': request.form.get('last_custom_folder', '')
    }

    with app.app_context():
        update_user_settings(settings_dict)

    return redirect(url_for('settings', save_success=True))

@app.teardown_appcontext
def cleanup(exception=None):
    """Clean up resources when shutting down"""
    # Remove temp directory if in demo mode
    if global_state['temp_dir'] and os.path.exists(global_state['temp_dir']):
        try:
            shutil.rmtree(global_state['temp_dir'])
            print("Cleaned up demo environment")
        except Exception as e:
            print(f"Could not clean up demo directory: {str(e)}")

    # Restore original stdout
    sys.stdout = original_stdout

def main():
    """Main function to run the web application"""
    port = 5000
    print(f"Starting Email Duplicate Cleaner Web Interface on port {port}")
    print(f"Open http://localhost:{port} in your browser")
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == "__main__":
    main()