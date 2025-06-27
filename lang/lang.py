# lang/lang.py

TRANSLATIONS = {
    'en': {
        # ======================================================================
        # General & Common UI Elements
        # ======================================================================
        'app_title': 'Email Duplicate Cleaner',
        'close_button': 'Close',
        'error_title': 'Error',
        'confirm_title': 'Confirm',
        'warning_title': 'Warning',
        'info_title': 'Info',
        'ready_status': 'Ready',

        # ======================================================================
        # Main Menu
        # ======================================================================
        'menu_file': 'File',
        'menu_file_open_folder': 'Open Folder...',
        'menu_file_run_demo': 'Run Demo Mode',
        'menu_file_exit': 'Exit',

        'menu_tools': 'Tools',
        'menu_tools_log_viewer': 'Log Viewer',
        'menu_tools_debug': 'Debug Mode',

        'menu_view': 'View',
        'menu_view_dark_mode': 'Dark Mode',

        'menu_settings': 'Settings',
        'menu_settings_language': 'Language',
        'menu_settings_language_en': 'English',
        'menu_settings_language_it': 'Italian',

        'menu_help': 'Help',
        'menu_help_about': 'About',
        'menu_check_updates': 'Check for Updates',
        'update_available': 'Update Available',
        'update_download': 'Download Now',
        'update_later': 'Remind Me Later',
        'update_error': 'Update Error',
        'update_check_error': 'Failed to check for updates: {error}',
                
        'menu_sponsor': 'Sponsor',
        'menu_sponsor_us': 'Sponsor Us',
        'menu_sponsor_github': 'Sponsor on GitHub',

        # ======================================================================
        # Tabs
        # ======================================================================
        'tab_scan': 'Scan',
        'tab_results': 'Results',
        'tab_analysis': 'Analysis',
        
        # ======================================================================
        # Analysis Tab
        # ======================================================================
        'analysis_run_analysis': 'Run Analysis',
        'analysis_senders': 'Senders',
        'analysis_timeline': 'Timeline',
        'analysis_attachments': 'Attachments',
        'analysis_threads': 'Threads',
        'analysis_duplicates': 'Duplicates',
        'analysis_generate_report': 'Generate Report',
        'analysis_report_format': 'Report Format:',
        'analysis_report_formats': {
            'text': 'Text',
            'html': 'HTML',
            'json': 'JSON'
        },
        'analysis_no_data': 'No analysis data available. Run an analysis first.',
        'analysis_running': 'Analyzing emails...',
        'analysis_complete': 'Analysis complete',
        'analysis_error': 'Error during analysis: {error}',
        'analysis_report_saved': 'Report saved to: {path}',
        'analysis_report_error': 'Error generating report: {error}',
        'analysis_section_senders': 'Top Senders',
        'analysis_section_timeline': 'Email Timeline',
        'analysis_section_attachments': 'Attachment Analysis',
        'analysis_section_threads': 'Conversation Threads',
        'analysis_section_duplicates': 'Duplicate Analysis',

        # ======================================================================
        # Scan Tab
        # ======================================================================
        # --- Labels and Frames ---
        'scan_client_frame': 'Email Client:',
        'scan_criteria_frame': 'Duplicate Detection Criteria:',
        'scan_folder_frame': 'Mail Folders:',

        # --- Radio Buttons ---
        'scan_client_all_radio': 'All Supported',
        'scan_client_thunderbird_radio': 'Thunderbird',
        'scan_client_apple_mail_radio': 'Apple Mail',
        'scan_client_outlook_radio': 'Outlook',
        'scan_client_generic_radio': 'Generic Mbox',

        'scan_criteria_strict_radio': 'Strict (Headers + Content)',
        'scan_criteria_content_radio': 'Content Only',
        'scan_criteria_headers_radio': 'Headers Only',
        'scan_criteria_subject_sender_radio': 'Subject + Sender',
		
        # --- Checkboxes ---
        'scan_autoclean_checkbox': 'Automatically clean duplicates after scan',

        # --- Buttons ---
        'scan_find_folders_button': 'Find Folders',
        'scan_select_all_button': 'Select All',
        'scan_button': 'Scan for Duplicates',

        # ======================================================================
        # Results Tab
        # ======================================================================
        # --- Labels and Frames ---
        'group_management_frame': 'Group Management',
        'email_actions_frame': 'Email Actions',
        'preview_header': 'Select an email to preview its content.',
        'preview_header_group_selected': 'Select an individual email to see a preview.',
        'preview_header_error': 'Error Previewing Email',

        # --- Treeview Headers ---
        'header_group': 'Group',
        'header_date': 'Date',
        'header_from': 'From',
        'header_subject': 'Subject',
        'header_folder': 'Folder',
        'group_text': '{count} emails',
        'original_prefix': 'Original',

        # --- Buttons ---
        'expand_all_button': 'Expand All',
        'collapse_all_button': 'Collapse All',
        'view_email_button': 'View Email',
        'clean_selected_button': 'Clean Selected',
        'clean_all_button': 'Clean All',

        # --- Context Menu ---
        'context_menu_view_email': 'View Email Content',

        # ======================================================================
        # Console
        # ======================================================================
        'console_frame_title': 'Console',

        # ======================================================================
        # Status Bar & Logging Messages
        # ======================================================================
        'status_finding_folders': 'Finding mail folders...',
        'status_found_folders': 'Found {count} mail folders.',
        'status_no_folders_found': 'No mail folders found for the selected client.',
        'status_scanning': 'Scanning {count} folders for duplicates...',
        'status_scan_complete': 'Scan complete. Found {group_count} duplicate groups with {dupe_count} redundant emails.',
        'status_no_duplicates_found': 'Scan complete. No duplicates found.',
        'status_cleaning': 'Cleaning {count} groups...',
        'status_cleaning_all': 'Cleaning all {count} groups...',
        'status_cleaning_complete': 'Cleaning complete. {deleted} emails deleted.',
        'status_cleaning_with_errors': 'Cleaning complete. {deleted} emails deleted with {error_count} errors.',
        'status_debug_enabled': 'Debug mode enabled.',
        'status_debug_disabled': 'Debug mode disabled.',
        'status_groups_expanded': 'All groups expanded.',
        'status_groups_collapsed': 'All groups collapsed.',
        'log_demo_mode_running': 'Running in demo mode with test emails...',
        'log_expanding_groups': 'Expanding all groups...',
        'log_collapsing_groups': 'Collapsing all groups...',
        'log_found_top_level_items': 'Found {count} top-level items',
        'log_error_previewing_email': 'Could not display the email preview.',
        'log_error_cleanup_temp_dir': 'Failed to clean up temp directory: {error}',

        # ======================================================================
        # Dialogs & Message Boxes
        # ======================================================================
        'dialog_select_mail_folder_title': 'Select Mail Folder',
        'dialog_no_folder_selection_title': 'No Folders Selected',
        'dialog_no_folder_selection_message': 'Please select at least one folder to scan.',
        'dialog_no_group_selection_title': 'No Groups Selected',
        'dialog_no_group_selection_message': 'Please select at least one group to clean.',
        'dialog_no_valid_groups_title': 'No Valid Groups',
        'dialog_no_valid_groups_message': 'No valid groups were found in the selection.',
        'dialog_no_duplicates_title': 'No Duplicates',
        'dialog_no_duplicates_message': 'There are no duplicate groups to clean.',
        'dialog_confirm_deletion_title': 'Confirm Deletion',
        'dialog_confirm_deletion_message': 'Are you sure you want to delete the selected duplicate emails? This action cannot be undone.',
        'dialog_confirm_deletion_all_message': 'Are you sure you want to delete all duplicate emails? This action cannot be undone.',
        'dialog_cleaning_errors_title': 'Cleaning Errors',
        'dialog_cleaning_error_message': 'Deleted {deleted} emails, but encountered {error_count} errors.',
        'dialog_errors_label': 'Errors',
        'dialog_cleaning_complete_title': 'Cleaning Complete',
        'dialog_cleaning_success_message': 'Successfully deleted {deleted} duplicate emails.',
        'dialog_demo_mode_title': 'Demo Mode',
        'dialog_demo_mode_confirm_message': 'This will create a temporary mailbox with test emails. Continue?',
        'dialog_demo_mode_info_message': 'Demo mailbox created. Select the folders and click Scan.',
        'dialog_no_email_selection_title': 'No Email Selected',
        'dialog_no_email_selection_message': 'Please select an email to view.',
        'dialog_invalid_selection_title': 'Invalid Selection',
        'dialog_invalid_selection_message': 'Please select an individual email, not a group header.',

        # ======================================================================
        # Error Messages
        # ======================================================================
        'error_finding_folders': 'Error finding mail folders: {error}',
        'error_scanning_folders': 'Error during scanning: {error}',
        'error_cleaning_duplicates': 'Error during cleaning: {error}',
        'error_viewing_email': 'Error viewing email content: {error}',
        'error_demo_mode': 'Error setting up demo mode: {error}',
        'error_expanding_groups': 'Error expanding groups: {error}',
        'error_collapsing_groups': 'Error collapsing groups: {error}',

        # ======================================================================
        # Email Viewer Window
        # ======================================================================
        'email_viewer_title': 'Email Viewer: {subject}',
        'email_headers_frame': 'Email Headers',
        'email_content_frame': 'Email Content',
        'email_header_from': 'From:',
        'email_header_to': 'To:',
        'email_header_to_na': 'N/A',
        'email_header_date': 'Date:',
        'email_header_subject': 'Subject:',
        'email_header_folder': 'Folder:',

        # ======================================================================
        # About Window
        # ======================================================================
        'about_window_title': 'About Email Duplicate Cleaner',
        'version': 'Version:',
        'about': 'About',

        # ======================================================================
        # Sponsor Window
        # ======================================================================
        'sponsor_window_title': 'Sponsor this Project',
        'sponsor_on_github': 'GitHub',
        'join_discord': 'Join Discord',
        'buy_me_a_coffee': 'Buy me a Coffee',
        'join_the_patreon': 'Join Patreon',
        
        # ======================================================================
        # Help Window
        # ======================================================================
        'help_window_title': 'Help',
        'help_title': 'Help',
        'usage_tab': 'Usage',
        'features_tab': 'Features',
        'analysis_tab': 'Analysis',
        'help_usage': (
            '1. Select your email source (IMAP, local file, or directory)\n'
            '2. Choose duplicate detection criteria\n'
            '3. Review the detected duplicates in the results tab\n'
            '4. Use the Analysis tab to gain insights into your email data\n'
            '5. Select actions for each duplicate group (keep, delete, mark, etc.)\n'
            '6. Generate reports of your analysis if needed\n'
            '7. Apply the changes when ready'
        ),
        'help_features': (
            '• Advanced Duplicate Detection: Find and manage duplicate emails with multiple matching criteria\n'
            '• Email Analysis: Comprehensive email analytics including senders, timeline, attachments, and threads\n'
            '• Multi-Platform Support: Works with various email clients and formats\n'
            '• Intuitive Interface: User-friendly GUI with dark/light theme support\n'
            '• Batch Processing: Process multiple email accounts or folders at once\n'
            '• Safe Operations: Preview changes before applying them\n'
            '• Cross-Platform: Works on Windows, macOS, and Linux\n'
            '• Exportable Reports: Generate detailed reports in multiple formats (Text, HTML, JSON)'
        ),
        'help_analysis': (
            'The Analysis tab provides powerful tools to gain insights into your email data:\n'
            '• Sender Analysis: Identify top senders and domains in your inbox\n'
            '• Timeline Visualization: See email patterns and activity over time\n'
            '• Attachment Statistics: Analyze file types, sizes, and frequencies\n'
            '• Thread Analysis: View and manage conversation threads\n'
            '• Duplicate Analysis: Get detailed insights into duplicate patterns\n'
            '• Exportable Reports: Save your analysis in multiple formats for further processing'
        ),
        'close': 'Close',

        # ======================================================================
        # Log Viewer Window
        # ======================================================================
        'log_viewer_title': 'Log Viewer',
        'log_level_label': 'Log Level:',
        'log_timestamp_header': 'Timestamp',
        'log_level_name_header': 'Level',
        'log_message_header': 'Message',
        'clear_log': 'Clear Log',
        'export_log': 'Export Log',

        # ======================================================================
        # Traceback Window
        # ======================================================================
        'traceback_window_title': 'Unhandled Exception',
        'traceback_message': 'An unexpected error occurred. Please see the details below.',
        'traceback_copy_button': 'Copy to Clipboard',
    },
    'it': {
        # ======================================================================
        # General & Common UI Elements
        # ======================================================================
        'app_title': 'Email Duplicate Cleaner',
        'close_button': 'Chiudi',
        'error_title': 'Errore',
        'confirm_title': 'Conferma',
        'warning_title': 'Avviso',
        'info_title': 'Info',
        'ready_status': 'Pronto',

        # ======================================================================
        # Main Menu
        # ======================================================================
        'menu_file': 'File',
        'menu_file_open_folder': 'Apri Cartella...',
        'menu_file_run_demo': 'Esegui Modalità Demo',
        'menu_file_exit': 'Esci',

        'menu_tools': 'Strumenti',
        'menu_tools_log_viewer': 'Visualizzatore Log',
        'menu_tools_debug': 'Modalità Debug',

        'menu_view': 'Visualizza',
        'menu_view_dark_mode': 'Modalità Scura',

        'menu_settings': 'Impostazioni',
        'menu_settings_language': 'Lingua',
        'menu_settings_language_en': 'Inglese',
        'menu_settings_language_it': 'Italiano',

        'menu_help': 'Aiuto',
        'menu_help_about': 'Informazioni',
        'menu_check_updates': 'Controlla aggiornamenti',
        'update_available': 'Aggiornamento disponibile',
        'update_download': 'Scarica ora',
        'update_later': 'Ricordamelo più tardi',
        'update_error': 'Errore aggiornamento',
        'update_check_error': 'Impossibile controllare gli aggiornamenti: {error}',
        'menu_sponsor_us': 'Sponsorizzaci',
        
        # ======================================================================
        # Tabs
        # ======================================================================
        'tab_scan': 'Scansione',
        'tab_results': 'Risultati',
        'tab_analysis': 'Analisi',
        
        # ======================================================================
        # Scheda Analisi
        # ======================================================================
        'analysis_run_analysis': 'Esegui Analisi',
        'analysis_senders': 'Mittenti',
        'analysis_timeline': 'Cronologia',
        'analysis_attachments': 'Allegati',
        'analysis_threads': 'Conversazioni',
        'analysis_duplicates': 'Duplicati',
        'analysis_generate_report': 'Genera Report',
        'analysis_report_format': 'Formato Report:',
        'analysis_report_formats': {
            'text': 'Testo',
            'html': 'HTML',
            'json': 'JSON'
        },
        'analysis_no_data': 'Nessun dato di analisi disponibile. Esegui prima un\'analisi.',
        'analysis_running': 'Analisi email in corso...',
        'analysis_complete': 'Analisi completata',
        'analysis_error': 'Errore durante l\'analisi: {error}',
        'analysis_report_saved': 'Report salvato in: {path}',
        'analysis_report_error': 'Errore durante la generazione del report: {error}',
        'analysis_section_senders': 'Mittenti Principali',
        'analysis_section_timeline': 'Cronologia Email',
        'analysis_section_attachments': 'Analisi Allegati',
        'analysis_section_threads': 'Conversazioni',
        'analysis_section_duplicates': 'Analisi Duplicati',

        # ======================================================================
        # Scan Tab
        # ======================================================================
        # --- Labels and Frames ---
        'scan_client_frame': 'Client Email:',
        'scan_criteria_frame': 'Criteri Rilevamento Duplicati:',
        'scan_folder_frame': 'Cartelle Email:',

        # --- Radio Buttons ---
        'scan_client_all_radio': 'Tutti i Supportati',
        'scan_client_thunderbird_radio': 'Thunderbird',
        'scan_client_apple_mail_radio': 'Apple Mail',
        'scan_client_outlook_radio': 'Outlook',
        'scan_client_generic_radio': 'Mbox Generico',

        'scan_criteria_strict_radio': 'Strict (Intestazioni + Contenuto)',
        'scan_criteria_content_radio': 'Solo Contenuto',
        'scan_criteria_headers_radio': 'Solo Intestazioni',
        'scan_criteria_subject_sender_radio': 'Oggetto + Mittente',
		
        # --- Checkboxes ---
        'scan_autoclean_checkbox': 'Pulisci automaticamente i duplicati dopo la scansione',

        # --- Buttons ---
        'scan_find_folders_button': 'Trova Cartelle',
        'scan_select_all_button': 'Seleziona Tutto',
        'scan_button': 'Scansiona per Duplicati',

        # ======================================================================
        # Results Tab
        # ======================================================================
        # --- Labels and Frames ---
        'group_management_frame': 'Gestione Gruppi',
        'email_actions_frame': 'Azioni Email',
        'preview_header': 'Seleziona un\'email per vederne l\'anteprima.',
        'preview_header_group_selected': 'Seleziona una singola email per vederne l\'anteprima.',
        'preview_header_error': 'Errore Anteprima Email',

        # --- Treeview Headers ---
        'header_group': 'Gruppo',
        'header_date': 'Data',
        'header_from': 'Da',
        'header_subject': 'Oggetto',
        'header_folder': 'Cartella',
        'group_text': '{count} email',
        'original_prefix': 'Originale',

        # --- Buttons ---
        'expand_all_button': 'Espandi Tutto',
        'collapse_all_button': 'Comprimi Tutto',
        'view_email_button': 'Visualizza Email',
        'clean_selected_button': 'Pulisci Selezionati',
        'clean_all_button': 'Pulisci Tutto',

        # --- Context Menu ---
        'context_menu_view_email': 'Visualizza Contenuto Email',

        # ======================================================================
        # Console
        # ======================================================================
        'console_frame_title': 'Console',

        # ======================================================================
        # Status Bar & Logging Messages
        # ======================================================================
        'status_finding_folders': 'Ricerca cartelle email in corso...',
        'status_found_folders': 'Trovate {count} cartelle email.',
        'status_no_folders_found': 'Nessuna cartella email trovata per il client selezionato.',
        'status_scanning': 'Scansione di {count} cartelle per duplicati in corso...',
        'status_scan_complete': 'Scansione completata. Trovati {group_count} gruppi di duplicati con {dupe_count} email ridondanti.',
        'status_no_duplicates_found': 'Scansione completata. Nessun duplicato trovato.',
        'status_cleaning': 'Pulizia di {count} gruppi in corso...',
        'status_cleaning_all': 'Pulizia di tutti i {count} gruppi in corso...',
        'status_cleaning_complete': 'Pulizia completata. {deleted} email eliminate.',
        'status_cleaning_with_errors': 'Pulizia completata. {deleted} email eliminate con {error_count} errori.',
        'status_debug_enabled': 'Modalità debug attivata.',
        'status_debug_disabled': 'Modalità debug disattivata.',
        'status_groups_expanded': 'Tutti i gruppi espansi.',
        'status_groups_collapsed': 'Tutti i gruppi compressi.',
        'log_demo_mode_running': 'Esecuzione in modalità demo con email di prova...',
        'log_expanding_groups': 'Espansione di tutti i gruppi...',
        'log_collapsing_groups': 'Compressione di tutti i gruppi...',
        'log_found_top_level_items': 'Trovati {count} elementi di primo livello',
        'log_error_previewing_email': 'Impossibile visualizzare l\'anteprima dell\'email.',
        'log_error_cleanup_temp_dir': 'Pulizia della directory temporanea fallita: {error}',

        # ======================================================================
        # Dialogs & Message Boxes
        # ======================================================================
        'dialog_select_mail_folder_title': 'Seleziona Cartella Email',
        'dialog_no_folder_selection_title': 'Nessuna Cartella Selezionata',
        'dialog_no_folder_selection_message': 'Seleziona almeno una cartella da scansionare.',
        'dialog_no_group_selection_title': 'Nessun Gruppo Selezionato',
        'dialog_no_group_selection_message': 'Seleziona almeno un gruppo da pulire.',
        'dialog_no_valid_groups_title': 'Nessun Gruppo Valido',
        'dialog_no_valid_groups_message': 'Nessun gruppo valido trovato nella selezione.',
        'dialog_no_duplicates_title': 'Nessun Duplicato',
        'dialog_no_duplicates_message': 'Non ci sono gruppi di duplicati da pulire.',
        'dialog_confirm_deletion_title': 'Conferma Eliminazione',
        'dialog_confirm_deletion_message': 'Sei sicuro di voler eliminare le email duplicate selezionate? Questa azione non può essere annullata.',
        'dialog_confirm_deletion_all_message': 'Sei sicuro di voler eliminare tutte le email duplicate? Questa azione non può essere annullata.',
        'dialog_cleaning_errors_title': 'Errori di Pulizia',
        'dialog_cleaning_error_message': 'Eliminate {deleted} email, ma si sono verificati {error_count} errori.',
        'dialog_errors_label': 'Errori',
        'dialog_cleaning_complete_title': 'Pulizia Completata',
        'dialog_cleaning_success_message': 'Email duplicate eliminate con successo: {deleted}.',
        'dialog_demo_mode_title': 'Modalità Demo',
        'dialog_demo_mode_confirm_message': 'Questo creerà una casella di posta temporanea con email di prova. Continuare?',
        'dialog_demo_mode_info_message': 'Casella di posta demo creata. Seleziona le cartelle e clicca Scansiona.',
        'dialog_no_email_selection_title': 'Nessuna Email Selezionata',
        'dialog_no_email_selection_message': 'Seleziona un\'email da visualizzare.',
        'dialog_invalid_selection_title': 'Selezione non Valida',
        'dialog_invalid_selection_message': 'Seleziona una singola email, non l\'intestazione di un gruppo.',

        # ======================================================================
        # Error Messages
        # ======================================================================
        'error_finding_folders': 'Errore durante la ricerca delle cartelle email: {error}',
        'error_scanning_folders': 'Errore durante la scansione: {error}',
        'error_cleaning_duplicates': 'Errore durante la pulizia: {error}',
        'error_viewing_email': 'Errore durante la visualizzazione del contenuto dell\'email: {error}',
        'error_demo_mode': 'Errore nell\'impostazione della modalità demo: {error}',
        'error_expanding_groups': 'Errore durante l\'espansione dei gruppi: {error}',
        'error_collapsing_groups': 'Errore durante la compressione dei gruppi: {error}',

        # ======================================================================
        # Email Viewer Window
        # ======================================================================
        'email_viewer_title': 'Visualizzatore Email: {subject}',
        'email_headers_frame': 'Intestazioni Email',
        'email_content_frame': 'Contenuto Email',
        'email_header_from': 'Da:',
        'email_header_to': 'A:',
        'email_header_to_na': 'N/D',
        'email_header_date': 'Data:',
        'email_header_subject': 'Oggetto:',
        'email_header_folder': 'Cartella:',

        # ======================================================================
        # About Window
        # ======================================================================
        'about_window_title': 'Informazioni su Email Duplicate Cleaner',
        'version': 'Versione:',
        'about': 'Informazioni',

        # ======================================================================
        # Sponsor Window
        # ======================================================================
        'sponsor_window_title': 'Sponsorizza questo Progetto',
        'sponsor_on_github': 'Sponsorizza su GitHub',
        'join_discord': 'Entra in Discord',
        'buy_me_a_coffee': 'Offrimi un Caffè',
        'join_the_patreon': 'Vieni su Patreon',
        'close': 'Chiudi',

        # ======================================================================
        # Help Window
        # ======================================================================
        'help_window_title': 'Aiuto',
        'help_title': 'Aiuto',
        'usage_tab': 'Utilizzo',
        'features_tab': 'Funzionalità',
        'analysis_tab': 'Analisi',
        'help_usage': (
            '1. Seleziona la sorgente delle email (IMAP, file locale o directory)\n'
            '2. Scegli i criteri di rilevamento dei duplicati\n'
            '3. Rivedi i duplicati rilevati nella scheda dei risultati\n'
            '4. Usa la scheda Analisi per approfondire i tuoi dati email\n'
            '5. Seleziona le azioni per ogni gruppo di duplicati (mantieni, elimina, segna, ecc.)\n'
            '6. Genera report della tua analisi se necessario\n'
            '7. Applica le modifiche quando sei pronto'
        ),
        'help_features': (
            '• Rilevamento Avanzato dei Duplicati: Trova e gestisci email duplicate con criteri di corrispondenza multipli\n'
            '• Analisi Email: Analisi completa inclusi mittenti, cronologia, allegati e thread\n'
            '• Supporto Multi-Piattaforma: Funziona con vari client e formati email\n'
            '• Interfaccia Intuitiva: GUI user-friendly con supporto per temi chiari/scuri\n'
            '• Elaborazione in Batch: Elabora più account o cartelle email contemporaneamente\n'
            '• Operazioni Sicure: Anteprima delle modifiche prima di applicarle\n'
            '• Cross-Platform: Funziona su Windows, macOS e Linux\n'
            '• Report Esportabili: Genera report dettagliati in più formati (Testo, HTML, JSON)'
        ),
        'help_analysis': (
            'La scheda Analisi fornisce strumenti potenti per approfondire i tuoi dati email:\n'
            '• Analisi dei Mittenti: Identifica i mittenti e i domini principali nella tua posta\n'
            '• Visualizzazione della Cronologia: Visualizza modelli e attività email nel tempo\n'
            '• Statistiche sugli Allegati: Analizza tipi, dimensioni e frequenze dei file\n'
            '• Analisi delle Conversazioni: Visualizza e gestisci i thread di discussione\n'
            '• Analisi dei Duplicati: Ottieni approfondimenti dettagliati sui modelli di duplicazione\n'
            '• Report Esportabili: Salva le tue analisi in più formati per ulteriori elaborazioni'
        ),
        'close': 'Chiudi',

        # ======================================================================
        # Log Viewer Window
        # ======================================================================
        'log_viewer_title': 'Visualizzatore Log',
        'log_level_label': 'Livello Log:',
        'log_timestamp_header': 'Timestamp',
        'log_level_name_header': 'Livello',
        'log_message_header': 'Messaggio',
        'clear_log': 'Pulisci Log',
        'export_log': 'Esporta Log',

        # ======================================================================
        # Traceback Window
        # ======================================================================
        'traceback_window_title': 'Eccezione non Gestita',
        'traceback_message': 'Si è verificato un errore imprevisto. Vedi i dettagli di seguito.',
        'traceback_copy_button': 'Copia negli Appunti',
    }
}

class LanguageManager:
    def __init__(self, language='en'):
        self.language = language

    def set_language(self, language):
        if language in TRANSLATIONS:
            self.language = language
        else:
            raise ValueError(f"Unsupported language: {language}")

    def get(self, key, **kwargs):
        return TRANSLATIONS.get(self.language, {}).get(key, key).format(**kwargs)

# Global instance
lang_manager = LanguageManager()

def get_string(key, **kwargs):
    return lang_manager.get(key, **kwargs)
