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

        'menu_view': 'View',
        'menu_view_dark_mode': 'Dark Mode',
        'menu_view_debug_mode': 'Debug Mode',

        'menu_settings': 'Settings',
        'menu_settings_language': 'Language',
        'menu_settings_language_en': 'English',
        'menu_settings_language_it': 'Italiano',

        'menu_help': 'Help',
        'menu_help_about': 'About',
        'menu_help_report_bug': 'Report Bug',
        'menu_help_content': 'Help Content',

        'menu_sponsor': 'Sponsor',
        'menu_sponsor_us': 'Sponsor Us',

        # ======================================================================
        # Tabs
        # ======================================================================
        'tab_scan': 'Scan',
        'tab_results': 'Results',

        # ======================================================================
        # Scan Tab
        # ======================================================================
        # --- Labels and Frames ---
        'scan_client_label': 'Email Client:',
        'scan_criteria_label': 'Duplicate Detection Criteria:',
        'scan_folders_label': 'Mail Folders:',

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
        'results_group_management_frame': 'Group Management',
        'results_email_actions_frame': 'Email Actions',
        'results_preview_header_default': 'Select an email to preview its content.',
        'results_preview_header_group_selected': 'Select an individual email to see a preview.',
        'results_preview_header_error': 'Error Previewing Email',

        # --- Treeview Headers ---
        'results_header_group': 'Group',
        'results_header_date': 'Date',
        'results_header_from': 'From',
        'results_header_subject': 'Subject',
        'results_header_folder': 'Folder',
        'results_group_text': '{count} emails',
        'results_original_prefix': 'Original',

        # --- Buttons ---
        'results_expand_all_button': 'Expand All',
        'results_collapse_all_button': 'Collapse All',
        'results_view_email_button': 'View Email',
        'results_clean_selected_button': 'Clean Selected',
        'results_clean_all_button': 'Clean All',

        # --- Context Menu ---
        'results_context_menu_view_email': 'View Email Content',

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
        'about_version_label': 'Version:',
        'about_author_label': 'Author:',
        'about_email_label': 'Email:',
        'about_github_label': 'GitHub:',
        'about_license_label': 'License:',

        # ======================================================================
        # Sponsor Window
        # ======================================================================
        'sponsor_window_title': 'Sponsor this Project',
        'sponsor_paypal_button': 'PayPal',
        'sponsor_patreon_button': 'Patreon',

        # ======================================================================
        # Help Window
        # ======================================================================
        'help_window_title': 'Help',

        # ======================================================================
        # Log Viewer Window
        # ======================================================================
        'log_viewer_title': 'Log Viewer',
        'log_level_label': 'Log Level:',
        'log_timestamp_header': 'Timestamp',
        'log_level_name_header': 'Level',
        'log_message_header': 'Message',
        'log_clear_button': 'Clear Log',
        'log_export_button': 'Export Log',

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

        'menu_view': 'Visualizza',
        'menu_view_dark_mode': 'Modalità Scura',
        'menu_view_debug_mode': 'Modalità Debug',

        'menu_settings': 'Impostazioni',
        'menu_settings_language': 'Lingua',
        'menu_settings_language_en': 'English',
        'menu_settings_language_it': 'Italiano',

        'menu_help': 'Aiuto',
        'menu_help_about': 'Informazioni',
        'menu_help_report_bug': 'Report Bug',
        'menu_help_content': 'Contenuto Aiuto',

        'menu_sponsor': 'Sponsor',
        'menu_sponsor_us': 'Sponsorizzaci',

        # ======================================================================
        # Tabs
        # ======================================================================
        'tab_scan': 'Scansione',
        'tab_results': 'Risultati',

        # ======================================================================
        # Scan Tab
        # ======================================================================
        # --- Labels and Frames ---
        'scan_client_label': 'Client Email:',
        'scan_criteria_label': 'Criteri Rilevamento Duplicati:',
        'scan_folders_label': 'Cartelle Email:',

        # --- Radio Buttons ---
        'scan_client_all_radio': 'Tutti i Supportati',
        'scan_client_thunderbird_radio': 'Thunderbird',
        'scan_client_apple_mail_radio': 'Apple Mail',
        'scan_client_outlook_radio': 'Outlook',
        'scan_client_generic_radio': 'Mbox Generico',

        'scan_criteria_strict_radio': 'Stretto (Intestazioni + Contenuto)',
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
        'results_group_management_frame': 'Gestione Gruppi',
        'results_email_actions_frame': 'Azioni Email',
        'results_preview_header_default': 'Seleziona un\'email per vederne l\'anteprima.',
        'results_preview_header_group_selected': 'Seleziona una singola email per vederne l\'anteprima.',
        'results_preview_header_error': 'Errore Anteprima Email',

        # --- Treeview Headers ---
        'results_header_group': 'Gruppo',
        'results_header_date': 'Data',
        'results_header_from': 'Da',
        'results_header_subject': 'Oggetto',
        'results_header_folder': 'Cartella',
        'results_group_text': '{count} email',
        'results_original_prefix': 'Originale',

        # --- Buttons ---
        'results_expand_all_button': 'Espandi Tutto',
        'results_collapse_all_button': 'Comprimi Tutto',
        'results_view_email_button': 'Visualizza Email',
        'results_clean_selected_button': 'Pulisci Selezionati',
        'results_clean_all_button': 'Pulisci Tutto',

        # --- Context Menu ---
        'results_context_menu_view_email': 'Visualizza Contenuto Email',

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
        'about_window_title': 'Informazioni su Pulitore Duplicati Email',
        'about_version_label': 'Versione:',
        'about_author_label': 'Autore:',
        'about_email_label': 'Email:',
        'about_github_label': 'GitHub:',
        'about_license_label': 'Licenza:',

        # ======================================================================
        # Sponsor Window
        # ======================================================================
        'sponsor_window_title': 'Sponsorizza questo Progetto',
        'sponsor_paypal_button': 'PayPal',
        'sponsor_patreon_button': 'Patreon',

        # ======================================================================
        # Help Window
        # ======================================================================
        'help_window_title': 'Aiuto',

        # ======================================================================
        # Log Viewer Window
        # ======================================================================
        'log_viewer_title': 'Visualizzatore Log',
        'log_level_label': 'Livello Log:',
        'log_timestamp_header': 'Timestamp',
        'log_level_name_header': 'Livello',
        'log_message_header': 'Messaggio',
        'log_clear_button': 'Pulisci Log',
        'log_export_button': 'Esporta Log',

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
