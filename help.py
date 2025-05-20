def get_help_content():
    """
    Returns the help content as a dictionary containing sections and their content.
    """
    return {
        "overview": {
            "title": "Overview",
            "content": """
            Email Duplicate Cleaner is a powerful tool designed to help you identify and remove duplicate emails from your mailboxes.
            It supports multiple email clients including Thunderbird, Apple Mail, Outlook, and generic mail formats.
            The tool provides a user-friendly web interface to scan, analyze, and clean duplicate emails efficiently.
            """
        },
        "features": {
            "title": "Key Features",
            "content": """
            <ul>
                <li><strong>Multi-Client Support:</strong> Works with Thunderbird, Apple Mail, Outlook, and generic mail formats</li>
                <li><strong>Customizable Detection:</strong> Multiple criteria for identifying duplicates (strict, content, headers, subject+sender)</li>
                <li><strong>Auto-Clean:</strong> Automatic removal of duplicates while keeping the oldest email</li>
                <li><strong>Custom Folders:</strong> Scan custom mail folder locations</li>
                <li><strong>Demo Mode:</strong> Test the tool with sample emails</li>
                <li><strong>History Tracking:</strong> Keep track of all scanning and cleaning operations</li>
            </ul>
            """
        },
        "getting_started": {
            "title": "Getting Started",
            "content": """
            <ol>
                <li>Select your email client or choose "All Clients"</li>
                <li>Choose your duplicate detection criteria</li>
                <li>Click "Find Folders" to locate mail folders</li>
                <li>Select the folders you want to scan</li>
                <li>Click "Scan Selected" to start the scanning process</li>
            </ol>
            """
        },
        "detection_criteria": {
            "title": "Detection Criteria",
            "content": """
            <dl>
                <dt>Strict</dt>
                <dd>Compares all email properties including headers, content, and attachments</dd>
                
                <dt>Content Only</dt>
                <dd>Compares only the email body content</dd>
                
                <dt>Headers</dt>
                <dd>Compares email headers (subject, sender, date, etc.)</dd>
                
                <dt>Subject+Sender</dt>
                <dd>Compares email subject and sender information</dd>
            </dl>
            """
        },
        "cleaning_options": {
            "title": "Cleaning Options",
            "content": """
            <ul>
                <li><strong>Auto-clean:</strong> Automatically removes duplicates while keeping the oldest email</li>
                <li><strong>Manual Selection:</strong> Review duplicates and select which ones to keep/remove</li>
                <li><strong>Batch Operations:</strong> Clean selected or all duplicate groups at once</li>
            </ul>
            """
        },
        "troubleshooting": {
            "title": "Troubleshooting",
            "content": """
            <ul>
                <li><strong>No folders found:</strong> Check if the mail client is properly installed and configured</li>
                <li><strong>Scan takes too long:</strong> Try using more specific detection criteria or scan fewer folders</li>
                <li><strong>Missing emails:</strong> Ensure you have selected all relevant mail folders</li>
                <li><strong>Permission issues:</strong> Run the application with appropriate permissions</li>
            </ul>
            """
        },
        "faq": {
            "title": "Frequently Asked Questions",
            "content": """
            <dl>
                <dt>Is my data safe?</dt>
                <dd>Yes, the tool only removes duplicates while keeping at least one copy of each email.</dd>
                
                <dt>Can I recover deleted emails?</dt>
                <dd>Check your email client's trash folder or backup before using the clean feature.</dd>
                
                <dt>How does it handle attachments?</dt>
                <dd>In strict mode, attachments are considered when detecting duplicates.</dd>
                
                <dt>Can I use it with multiple email clients?</dt>
                <dd>Yes, select "All Clients" to scan across multiple email clients simultaneously.</dd>
            </dl>
            """
        }
    }
