
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
                            <div class="duplicate-group" data-group-index="${groupIndex}">
                                <div class="group-header d-flex justify-content-between align-items-center">
                                    <div>
                                        <input type="checkbox" class="form-check-input group-checkbox" value="${groupIndex}">
                                        <span class="ms-2">Group ${groupIndex + 1} (${group.emails.length} emails)</span>
                                    </div>
                                    <button class="btn btn-sm btn-outline-warning clean-group-btn" data-group-index="${groupIndex}">
                                        Clean Group
                                    </button>
                                </div>
                                <div class="email-list">`;

                        group.emails.forEach((email, emailIndex) => {
                            const isOriginal = emailIndex === 0;
                            html += `
                                <div class="email-item ${isOriginal ? 'original' : ''}">
                                    <div class="d-flex">
                                        <div class="email-meta me-3">
                                            ${emailIndex + 1}${isOriginal ? ' (orig)' : ''}
                                        </div>
                                        <div class="flex-grow-1">
                                            <div class="email-subject">${email.subject}</div>
                                            <div class="d-flex justify-content-between mt-1">
                                                <div class="email-meta">
                                                    <strong>From:</strong> ${email.from}
                                                </div>
                                                <div class="email-meta">
                                                    <strong>Date:</strong> ${email.date}
                                                </div>
                                            </div>
                                            <div class="email-meta mt-1">
                                                <strong>Folder:</strong> ${email.folder_path}
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
