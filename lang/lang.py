# lang/lang.py

TRANSLATIONS = {
    'en': {
        # General
        'app_title': 'Email Duplicate Cleaner',
        'ready': 'Ready',
        'error': 'Error',
        'success': 'Success',
        'info': 'Info',
        'warning': 'Warning',
        'confirm': 'Confirm',
        'cancel': 'Cancel',
        'close': 'Close',
        'yes': 'Yes',
        'no': 'No',

        # Menu
        'file': 'File',
        'exit': 'Exit',
        'tools': 'Tools',
        'view': 'View',
        'demo_mode': 'Demo Mode',
        'settings': 'Settings',
        'dark_mode': 'Dark Mode',
        'debug_mode': 'Debug Mode',
        'help': 'Help',
        'about': 'About',
        'sponsor': 'Sponsor',
        'sponsor_us': 'Sponsor Us',
        'language': 'Language',

        # Tabs
        'scan_tab': 'Scan',
        'results_tab': 'Results',

        # Scan Tab
        'email_client': 'Email Client:',
        'select_client': 'Select Client',
        'thunderbird': 'Thunderbird',
        'outlook': 'Outlook',
        'apple_mail': 'Apple Mail',
        'custom_folder': 'Custom Folder',
        'find_folders': 'Find Folders',
        'mail_folders': 'Mail Folders:',
        'select_all': 'Select All',
        'scan': 'Scan',

        # Results Tab
        'duplicate_groups': 'Duplicate Groups',
        'group': 'Group',
        'subject': 'Subject',
        'count': 'Count',
        'clean_selected': 'Clean Selected',
        'clean_all': 'Clean All',
        'email_preview': 'Email Preview',
        'headers': 'Email Headers',
        'from': 'From:',
        'to': 'To:',
        'date': 'Date:',
        'folder': 'Folder:',
        'content': 'Email Content',

        # Console
        'console': 'Console',
        'console_frame_title': "Console",
        'status_debug_enabled': "Debug mode enabled.",
        'status_debug_disabled': "Debug mode disabled.",
        'error_prefix': "Error",
        'lang_english': "English",
        'lang_italian': "Italiano",
        'demo_mode_running': "Running in demo mode with test emails...",
        'expanding_all_groups': "Expanding all groups...",
        'collapsing_all_groups': "Collapsing all groups...",
        'found_top_level_items': "Found {count} top-level items",
        'preview_header_group_selected': "Select an individual email to see a preview.",
        'preview_header_error': "Error Previewing Email",
        'error_previewing_email': "Could not display the email preview.",
        'error_cleanup_temp_dir': "Failed to clean up temp directory: {error}",

        # Status Messages
        'finding_folders': 'Finding mail folders...',
        'folders_found': 'Found {count} mail folders.',
        'no_folders_found': 'No mail folders found for the selected client.',
        'scanning_folders': 'Scanning selected folders...',
        'scan_complete': 'Scan complete. Found {count} duplicate groups.',
        'no_duplicates_found': 'No duplicates found.',
        'cleaning_selected': 'Cleaning selected duplicate groups...',
        'cleaning_all': 'Cleaning all duplicate groups...',
        'cleaning_complete': 'Cleaning complete. Deleted {deleted_count} emails. Encountered {error_count} errors.',
        'select_folders_to_scan': 'Please select at least one folder to scan.',
        'select_groups_to_clean': 'Please select at least one group to clean.',
        'no_groups_to_clean': 'No duplicate groups to clean.',
        'demo_mode_running': 'Running in Demo Mode. A temporary mailbox has been created.',
        'error_finding_folders': 'Error finding mail folders: {error}',
        'error_scanning': 'Error during scanning: {error}',
        'error_cleaning': 'Error during cleaning: {error}',
        'error_viewing_email': 'Error viewing email content: {error}',

        # About Window
        'about_title': "About Email Duplicate Cleaner",
        'version': 'Version',
        'author': 'Author',
        'email': 'Email',
        'github': 'GitHub',
        'license': 'License',
        'version_label': "Version:",

        # Sponsor Window
        'sponsor_title': 'Sponsor this Project',

        # Logger
        'log_viewer_title': 'Log Viewer',
        'log_level': 'Log Level:',
        'log_timestamp': 'Timestamp',
        'log_level_name': 'Level',
        'log_message': 'Message',
        'clear_log': 'Clear Log',
        'export_log': 'Export Log',

        # Traceback
        'traceback_title': 'Unhandled Exception',
        'traceback_message': 'An unexpected error occurred. Please see the details below.',
        'copy_to_clipboard': 'Copy to Clipboard',
    },
    'it': {
        # General
        'app_title': 'Email Duplicate Cleaner',
        'ready': 'Pronto',
        'error': 'Errore',
        'success': 'Successo',
        'info': 'Info',
        'warning': 'Avviso',
        'confirm': 'Conferma',
        'cancel': 'Annulla',
        'close': 'Chiudi',
        'yes': 'Sì',
        'no': 'No',

        # Menu
        'file': 'File',
        'exit': 'Esci',
        'tools': 'Strumenti',
        'view': 'Visualizza',
        'demo_mode': 'Modalità Demo',
        'settings': 'Impostazioni',
        'dark_mode': 'Modalità Scura',
        'debug_mode': 'Modalità Debug',
        'help': 'Aiuto',
        'about': 'Informazioni',
        'sponsor': 'Sponsor',
        'sponsor_us': 'Sponsorizzaci',
        'language': 'Lingua',

        # Tabs
        'scan_tab': 'Scansione',
        'results_tab': 'Risultati',

        # Scan Tab
        'email_client': 'Client Email:',
        'select_client': 'Seleziona Client',
        'thunderbird': 'Thunderbird',
        'outlook': 'Outlook',
        'apple_mail': 'Apple Mail',
        'custom_folder': 'Cartella Personalizzata',
        'find_folders': 'Trova Cartelle',
        'mail_folders': 'Cartelle Email:',
        'select_all': 'Seleziona Tutto',
        'scan': 'Scansiona',

        # Results Tab
        'duplicate_groups': 'Gruppi Duplicati',
        'group': 'Gruppo',
        'subject': 'Oggetto',
        'count': 'Numero',
        'clean_selected': 'Pulisci Selezionati',
        'clean_all': 'Pulisci Tutto',
        'email_preview': 'Anteprima Email',
        'headers': 'Intestazioni Email',
        'from': 'Da:',
        'to': 'A:',
        'date': 'Data:',
        'folder': 'Cartella:',
        'content': 'Contenuto Email',

        # Console
        'console': 'Console',
        'console_frame_title': "Console",
        'status_debug_enabled': "Modalità debug attivata.",
        'status_debug_disabled': "Modalità debug disattivata.",
        'error_prefix': "Errore",
        'lang_english': "English",
        'lang_italian': "Italiano",
        'demo_mode_running': "Esecuzione in modalità demo con email di prova...",
        'expanding_all_groups': "Espansione di tutti i gruppi...",
        'collapsing_all_groups': "Compressione di tutti i gruppi...",
        'found_top_level_items': "Trovati {count} elementi di primo livello",
        'preview_header_group_selected': "Seleziona una singola email per vederne l'anteprima.",
        'preview_header_error': "Errore Anteprima Email",
        'error_previewing_email': "Impossibile visualizzare l'anteprima dell'email.",
        'error_cleanup_temp_dir': "Pulizia della directory temporanea fallita: {error}",

        # Status Messages
        'finding_folders': 'Ricerca cartelle email in corso...',
        'folders_found': 'Trovate {count} cartelle email.',
        'no_folders_found': 'Nessuna cartella email trovata per il client selezionato.',
        'scanning_folders': 'Scansione delle cartelle selezionate in corso...',
        'scan_complete': 'Scansione completata. Trovati {count} gruppi di duplicati.',
        'no_duplicates_found': 'Nessun duplicato trovato.',
        'cleaning_selected': 'Pulizia dei gruppi di duplicati selezionati in corso...',
        'cleaning_all': 'Pulizia di tutti i gruppi di duplicati in corso...',
        'cleaning_complete': 'Pulizia completata. Eliminate {deleted_count} email. Riscontrati {error_count} errori.',
        'select_folders_to_scan': 'Seleziona almeno una cartella da scansionare.',
        'select_groups_to_clean': 'Seleziona almeno un gruppo da pulire.',
        'no_groups_to_clean': 'Nessun gruppo di duplicati da pulire.',
        'demo_mode_running': "Esecuzione in modalità demo con email di prova...",
        'error_finding_folders': 'Errore durante la ricerca delle cartelle email: {error}',
        'error_scanning': 'Errore durante la scansione: {error}',
        'error_cleaning': 'Errore during la pulizia: {error}',
        'error_viewing_email': "Errore durante la visualizzazione del contenuto dell'email: {error}",

        # About Window
        'about_title': "Informazioni su Email Duplicate Cleaner",
        'version': 'Versione',
        'author': 'Autore',
        'email': 'Email',
        'github': 'GitHub',
        'license': 'Licenza',
        'version_label': "Versione:",

        # Sponsor Window
        'sponsor_title': 'Sponsorizza questo Progetto',

        # Logger
        'log_viewer_title': 'Visualizzatore Log',
        'log_level': 'Livello Log:',
        'log_timestamp': 'Timestamp',
        'log_level_name': 'Livello',
        'log_message': 'Messaggio',
        'clear_log': 'Pulisci Log',
        'export_log': 'Esporta Log',

        # Traceback
        'traceback_title': 'Eccezione non gestita',
        'traceback_message': 'Si è verificato un errore imprevisto. Vedi i dettagli di seguito.',
        'copy_to_clipboard': 'Copia negli Appunti',
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
