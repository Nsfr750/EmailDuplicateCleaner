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
        'error': 'Error',
        'error_demo_mode': 'Error in demo mode: {error}',
        'error_scanning_folders': 'Error scanning folders: {error}',
        'status_scanning_folders': 'Scanning {count} folders...',
        'status_no_duplicates_found': 'No duplicate emails found.',
        'status_found_duplicates': 'Found {group_count} groups with a total of {dupe_count} duplicate emails.',

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

        'menu_sponsor_us': 'Sponsor',
        'menu_sponsor_message': 'Support Development',
        'menu_sponsor_dialog': 'Thank you for considering to support our development!',

        # ======================================================================
        # Scan Tab
        # ======================================================================
        'tab_scan': 'Scansione',
        'tab_results': 'Risultati',
        'tab_analysis': 'Analisi',
        
        # Frame Titles
        'frame_client_selection': 'Selezione Client Email',
        'frame_scan_criteria': 'Criteri di Scansione',
        'frame_folders': 'Cartelle',
        'frame_actions': 'Azioni',
        'frame_preview': 'Anteprima Email',
        'frame_results': 'Gruppi di Duplicati',
        'frame_analysis': 'Analisi Email',
        'frame_analysis_summary': 'Riepilogo',
        'frame_analysis_senders': 'Mittenti Principali',
        'frame_analysis_subjects': 'Oggetti Comuni',
        'frame_analysis_dates': 'Distribuzione Email',
        
        # Help Panel
        'help_title': 'Guida e Documentazione',
        'help_content': """# Guida di Email Duplicate Cleaner
        
## Panoramica
Questo strumento ti aiuta a trovare e rimuovere le email duplicate da vari client di posta.

## Come Usare
1. Seleziona il tuo client email
2. Scegli le cartelle da scansionare
3. Imposta i criteri di scansione
4. Clicca 'Cerca Duplicati'
5. Rivedi e pulisci i duplicati

## Supporto
Per assistenza, visita il nostro [repository GitHub](https://github.com/your-repo)""",
        'help_button': 'Mostra Guida',
        
        # Update Panel
        'update_title': 'Controlla Aggiornamenti',
        'update_button': 'Controlla Ora',
        'update_available': 'Nuova versione disponibile: {version}',
        'update_uptodate': 'Hai l\'ultima versione installata',
        'update_checking': 'Controllo aggiornamenti in corso...',
        'update_error': 'Errore nel controllo aggiornamenti',
        'update_download': 'Scarica Aggiornamento',
        'update_install': 'Installa Aggiornamento',
        'update_later': 'Ricordamelo Più Tardi',
        
        # Sponsor Panel
        'sponsor_title': 'Supporta lo Sviluppo',
        'sponsor_message': 'Se trovi utile questo strumento, valuta di supportarne lo sviluppo.',
        'sponsor_button': 'Diventa uno Sponsor',
        'sponsor_thanks': 'Grazie per il tuo supporto!',
        
        # About Panel
        'about_title': 'Informazioni su Email Duplicate Cleaner',
        'about_version': 'Versione: {version}',
        'about_author': 'Autore: Il Tuo Nome',
        'about_license': 'Licenza: MIT',
        'about_website': 'Sito Web: https://your-website.com',
        'about_github': 'GitHub: https://github.com/your-repo',
        
        # Analysis Section
        'analysis_run_button': 'Esegui Analisi',
        'analysis_export_button': 'Esporta Report',
        'analysis_summary_title': 'Riepilogo Email',
        'analysis_total_emails': 'Email Totali',
        'analysis_duplicate_emails': 'Email Duplicate',
        'analysis_unique_emails': 'Email Uniche',
        'analysis_space_saved': 'Spazio da Risparmiare',
        'analysis_top_senders': 'Top 10 Mittenti',
        'analysis_common_subjects': 'Oggetti Più Comuni',
        'analysis_email_distribution': 'Distribuzione Email per Data',
        'analysis_no_data': 'Nessun dato disponibile. Esegui prima l\'analisi.',
        'analysis_generating': 'Generazione analisi in corso...',
        'analysis_complete': 'Analisi completata',
        'analysis_error': 'Errore durante la generazione dell\'analisi',
        'analysis_export_success': 'Report esportato con successo',
        'analysis_export_error': 'Errore durante l\'esportazione del report',
        
        # Analysis Chart Labels
        'chart_senders': 'Mittenti',
        'chart_emails': 'Email',
        'chart_dates': 'Date',
        'chart_count': 'Conteggio',
        'chart_subject': 'Oggetto',
        'chart_frequency': 'Frequenza',
        
        # --- Client Selection ---
        'scan_client_all_radio': 'All Clients',
        'scan_client_thunderbird_radio': 'Mozilla Thunderbird',
        'scan_client_apple_mail_radio': 'Apple Mail',
        'scan_client_outlook_radio': 'Microsoft Outlook',
        'scan_client_generic_radio': 'Generic (MBOX/EML)',
        
        # --- Scan Criteria ---
        'scan_criteria_strict_radio': 'Strict (all headers and content must match)',
        'scan_criteria_content_radio': 'Content Only (ignore headers)',
        'scan_criteria_headers_radio': 'Headers Only (ignore content)',
        'scan_criteria_subject_sender_radio': 'Subject and Sender Only',

        'scan_email_client_label': 'Email Client:',
        'scan_find_folders_button': 'Find Folders',
        'scan_folders_label': 'Folders:',
        'scan_select_all_button': 'Select All',
        'scan_button': 'Find Duplicates',

        # --- Status Messages ---
        'status_scanning_folders': 'Scanning {count} folders for duplicates...',
        'status_no_duplicates_found': 'No duplicate emails found.',
        'status_found_duplicates': 'Found {group_count} groups with {dupe_count} duplicate emails.',
        'status_cleaning': 'Cleaning duplicates...',
        'status_cleaning_complete': 'Cleaning complete. Removed {count} duplicate(s).',
        'status_cleaning_error': 'Error during cleaning: {error}',

        # --- Error Messages ---
        'error_no_client_selected': 'Please select an email client',
        'error_no_folders_found': 'No mail folders found',
        'error_no_folders_selected': 'Please select at least one folder',
        'error_scanning_folders': 'Error scanning folders: {error}',
        'error_loading_emails': 'Error loading emails: {error}',
        'error_cleaning_duplicates': 'Error cleaning duplicates: {error}',
        'error_no_duplicates_selected': 'Please select at least one duplicate group to clean',

        # --- Success Messages ---
        'success_folders_found': 'Found {count} folders',
        'success_duplicates_found': 'Found {count} duplicate emails in {time:.2f} seconds',

        # --- Other ---
        'group_prefix': 'Group {index}',
        'original_prefix': 'Original',
        'emails_label': 'emails',

        # ======================================================================
        # Results Tab
        # ======================================================================
        # --- Treeview Headers ---
        'header_group': 'Group',
        'header_date': 'Date',
        'header_from': 'From',
        'header_subject': 'Subject',
        'header_folder': 'Folder',

        # --- Buttons ---
        'clean_selected_button': 'Clean Selected',
        'clean_all_button': 'Clean All',
        'expand_all_button': 'Expand All',
        'collapse_all_button': 'Collapse All',
        'export_button': 'Export Results',

        # --- Context Menu ---
        'context_view': 'View Email',
        'context_open_folder': 'Open Containing Folder',
        'context_copy': 'Copy to Clipboard',

        # --- Messages ---
        'confirm_clean_selected': 'Are you sure you want to clean the selected {count} duplicate(s)?',
        'confirm_clean_all': 'Are you sure you want to clean all {count} duplicates?',
        'no_duplicates_selected': 'No duplicates selected',

        # ======================================================================
        # Analysis Tab
        # ======================================================================
        'analysis_run_button': 'Run Analysis',
        'analysis_export_button': 'Export Report',
        'analysis_section_summary': 'Summary',
        'analysis_section_senders': 'Top Senders',
        'analysis_section_subjects': 'Common Subjects',
        'analysis_section_dates': 'Email Distribution',
        'analysis_total_emails': 'Total Emails',
        'analysis_duplicate_emails': 'Duplicate Emails',
        'analysis_unique_emails': 'Unique Emails',
        'analysis_space_saved': 'Space to Save',
        'analysis_top_senders': 'Top 10 Senders',
        'analysis_common_subjects': 'Common Subjects',
        'analysis_email_distribution': 'Email Distribution by Date',
        'analysis_no_data': 'No data available. Run the analysis first.',

        # ======================================================================
        # Log Viewer
        # ======================================================================
        'log_viewer_title': 'Log Viewer',
        'log_level_label': 'Log Level:',
        'log_timestamp_header': 'Timestamp',
        'log_level_name_header': 'Level',
        'log_message_header': 'Message',
        'clear_log': 'Clear Log',
        'copy_log': 'Copy to Clipboard',
        'save_log': 'Save Log As...',
        'log_save_success': 'Log saved successfully',
        'log_save_error': 'Error saving log: {error}',

        # ======================================================================
        # Demo Mode
        # ======================================================================
        'demo_mode_title': 'Demo Mode',
        'demo_mode_message': 'Running in demo mode with sample data.',

        # ======================================================================
        # Traceback Window
        # ======================================================================
        'traceback_window_title': 'Unhandled Exception',
        'traceback_message': 'An unexpected error occurred. Please see the details below.',
        'traceback_copy_button': 'Copy to Clipboard',
        'traceback_continue_button': 'Continue',
        'traceback_quit_button': 'Quit',
        'error': 'Error',
        'error_demo_mode': 'Error in demo mode: {error}'
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
        'info_title': 'Informazioni',
        'ready_status': 'Pronto',
        'error': 'Errore',
        'error_demo_mode': 'Errore nella modalità demo: {error}',
        'error_scanning_folders': 'Errore durante la scansione delle cartelle: {error}',
        'status_scanning_folders': 'Scansione di {count} cartelle in corso...',
        'status_no_duplicates_found': 'Nessuna email duplicata trovata.',
        'status_found_duplicates': 'Trovati {group_count} gruppi con un totale di {dupe_count} email duplicate.',

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
        'menu_check_updates': 'Controlla Aggiornamenti',
        'update_available': 'Aggiornamento Disponibile',
        'update_download': 'Scarica Ora',
        'update_later': 'Ricordamelo Più Tardi',
        'update_error': 'Errore Aggiornamento',
        'update_check_error': 'Impossibile controllare gli aggiornamenti: {error}',

        'menu_sponsor_us': 'Supportaci',
        'sponsor':'Sponsorizzaci',
        'support_on_github': 'Sponsoraci su GitHub', 
        'join_discord':'Unisciti a Discord',
        'buy_me_a_coffee':'Offrimi un Caffè',
        'join_the_patreon':'Unisciti a Patreon',
        'close':'Chiudi',

        # ======================================================================
        # Frames
        # ======================================================================
        'scan_folder_frame':'Cartelle da Scansionare',
        'scan_autoclean_checkbox': 'Pulisci automaticamente i duplicati',
        'scan_criteria_frame':'Criteri di Scansione',
        'scan_button_frame':'Pulsanti di Scansione',
        'console_frame_title':'Console',
        'results_frame_title':'Risultati',
        'analysis_frame_title':'Analisi',
        'preview_header':'Anteprima',
        'email_action_frame':'Azioni Email',
        'group_management_frame': 'Gestione Gruppi',
        'view_email_button':'Anteprima Email',

        # ======================================================================
        # Scan Tab
        # ======================================================================
        'tab_scan': 'Scansione',
        'tab_results': 'Risultati',
        'tab_analysis': 'Analisi',
        
        # --- Client Selection ---
        'scan_client_all_radio': 'Tutti i Client',
        'scan_client_thunderbird_radio': 'Mozilla Thunderbird',
        'scan_client_apple_mail_radio': 'Apple Mail',
        'scan_client_outlook_radio': 'Microsoft Outlook',
        'scan_client_generic_radio': 'Generico (MBOX/EML)',
        
        # --- Scan Criteria ---
        'scan_criteria_strict_radio': 'Rigido (tutti gli header e il contenuto devono corrispondere)',
        'scan_criteria_content_radio': 'Solo Contenuto (ignora gli header)',
        'scan_criteria_headers_radio': 'Solo Header (ignora il contenuto)',
        'scan_criteria_subject_sender_radio': 'Solo Oggetto e Mittente',

        'scan_email_client_label': 'Client Email:',
        'scan_find_folders_button': 'Trova Cartelle',
        'scan_folders_label': 'Cartelle:',
        'scan_select_all_button': 'Seleziona Tutto',
        'scan_button': 'Cerca Duplicati',

        # --- Status Messages ---
        'status_scanning_folders': 'Scansione di {count} cartelle alla ricerca di duplicati...',
        'status_cleaning': 'Pulizia duplicati in corso...',
        'status_cleaning_complete': 'Pulizia completata. Rimossi {count} duplicato/i.',
        'status_cleaning_error': 'Errore durante la pulizia: {error}',

        # --- Error Messages ---
        'error_no_client_selected': 'Seleziona un client email',
        'error_no_folders_found': 'Nessuna cartella email trovata',
        'error_no_folders_selected': 'Seleziona almeno una cartella',
        'error_loading_emails': 'Errore nel caricamento delle email: {error}',
        'error_cleaning_duplicates': 'Errore durante la pulizia dei duplicati: {error}',
        'error_no_duplicates_selected': 'Seleziona almeno un gruppo di duplicati da pulire',

        # --- Success Messages ---
        'success_folders_found': 'Trovate {count} cartelle',
        'success_duplicates_found': 'Trovate {count} email duplicate in {time:.2f} secondi',

        # --- Other ---
        'group_prefix': 'Gruppo {index}',
        'original_prefix': 'Originale',
        'emails_label': 'email',

        # ======================================================================
        # Results Tab
        # ======================================================================
        # --- Treeview Headers ---
        'header_group': 'Gruppo',
        'header_date': 'Data',
        'header_from': 'Da',
        'header_subject': 'Oggetto',
        'header_folder': 'Cartella',

        # --- Buttons ---
        'clean_selected_button': 'Elimina Selezionati',
        'clean_all_button': 'Elimina Tutti',
        'expand_all_button': 'Espandi Tutto',
        'collapse_all_button': 'Comprimi Tutto',
        'export_button': 'Esporta Risultati',

        # --- Context Menu ---
        'context_view': 'Visualizza Email',
        'context_open_folder': 'Apri Cartella',
        'context_copy': 'Copia negli Appunti',

        # --- Messages ---
        'confirm_clean_selected': 'Sei sicuro di voler eliminare {count} duplicato/i selezionato/i?',
        'confirm_clean_all': 'Sei sicuro di voler eliminare tutti i {count} duplicati?',
        'no_duplicates_selected': 'Nessun duplicato selezionato',

        # ======================================================================
        # Analysis Tab
        # ======================================================================
        'analysis_run_button': 'Esegui Analisi',
        'analysis_export_button': 'Esporta Report',
        'analysis_section_summary': 'Riepilogo',
        'analysis_section_senders': 'Mittenti Principali',
        'analysis_section_subjects': 'Oggetti Comuni',
        'analysis_section_dates': 'Distribuzione Email',
        'analysis_total_emails': 'Email Totali',
        'analysis_duplicate_emails': 'Email Duplicate',
        'analysis_unique_emails': 'Email Uniche',
        'analysis_space_saved': 'Spazio da Risparmiare',
        'analysis_top_senders': 'Top 10 Mittenti',
        'analysis_common_subjects': 'Oggetti Più Comuni',
        'analysis_email_distribution': 'Distribuzione Email per Data',
        'analysis_no_data': 'Nessun dato disponibile. Eseguire prima l\'analisi.',
        'analysis_control': 'Controllo',
        'analysis_run_analysis': 'Esegui Analisi',
        'analysis_report_format': 'Formato Report',
        'analysis_generate_report': 'Genera Report',
        'analysis_sender': 'Mittenti',
        'analysis_timeline': 'Timeline',
        'analysis_attachments': 'Allegati',
        'analysis_thread': 'Thread',
        'analysis_duplicates': 'Duplicati',
       
        # ======================================================================
        # Log Viewer
        # ======================================================================
        'log_viewer_title': 'Visualizzatore Log',
        'log_level_label': 'Livello Log:',
        'log_timestamp_header': 'Data/Ora',
        'log_level_name_header': 'Livello',
        'log_message_header': 'Messaggio',
        'clear_log': 'Pulisci Log',
        'copy_log': 'Copia negli Appunti',
        'save_log': 'Salva Log Come...',
        'log_save_success': 'Log salvato con successo',
        'log_save_error': 'Errore nel salvataggio del log: {error}',

        # ======================================================================
        # Demo Mode
        # ======================================================================
        'demo_mode_title': 'Modalità Demo',
        'demo_mode_message': 'Esecuzione in modalità demo con dati di esempio.',

        # ======================================================================
        # Traceback Window
        # ======================================================================
        'traceback_window_title': 'Eccezione non Gestita',
        'traceback_message': 'Si è verificato un errore imprevisto. Vedi i dettagli di seguito.',
        'traceback_copy_button': 'Copia negli Appunti',
        'traceback_continue_button': 'Continua',
        'traceback_quit_button': 'Esci',
        'error': 'Errore',
        'error_demo_mode': 'Errore nella modalità demo: {error}'
    }
}

class LanguageManager:
    def __init__(self, language='en'):
        self.language = language
    
    def set_language(self, language):
        if language in TRANSLATIONS:
            self.language = language
    
    def get(self, key, **kwargs):
        return TRANSLATIONS.get(self.language, {}).get(key, key).format(**kwargs)

# Global instance
lang_manager = LanguageManager()

def get_string(key, **kwargs):
    return lang_manager.get(key, **kwargs)
