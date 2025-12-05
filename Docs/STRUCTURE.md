# 🧱 Email Duplicate Cleaner – Project Structure (v2.5.2)

Questa pagina descrive la struttura del progetto alla **versione 2.5.2** e il ruolo delle principali directory e file.

## 📁 Panoramica delle directory principali

- `email_duplicate_cleaner.py`  
  Core logica di scansione/rimozione duplicati + entry point **CLI**.

- `email_cleaner_gui.py`  
  Entry point per la **GUI desktop** (PySide6).

- `email_cleaner_web.py`  
  Entry point per l’interfaccia **Web** (Flask).

- `struttura/`  
  Moduli di supporto condivisi dalla GUI (e in parte dal resto dell’app):
  - `version.py` – gestione versione centralizzata (major/minor/patch, `get_version()`, dialog versione).
  - `menu.py` – menu applicazione.
  - `about.py` – finestra "About".
  - `help.py` – finestra di aiuto.
  - `sponsor.py` – dialog sponsor.
  - `logger.py` – sistema di logging centralizzato.
  - `updates.py` – logica aggiornamenti.
  - `view_log.py` – visualizzazione log.
  - `traceback.py` / `traceback_handler.py` – gestione errori e tracebacks.

- `lang/`  
  Gestione lingue e traduzioni:
  - `language_manager.py` – sistema lingua.
  - `translations.py` – stringhe tradotte (no JSON, solo Python).

- `assets/`  
  Risorse statiche (icone, immagini, ecc.):
  - `icon.ico` – icona principale dell’app (usata per GUI/installer).
  - `email.png` – risorse grafiche aggiuntive per UI.

- `docs/`  
  Documentazione del progetto:
  - `README.md` – documentazione generale.
  - `USER_GUIDE.md` – guida utente.
  - `API_REFERENCE.md` – riferimento API/logica.
  - `SECURITY.md` – policy di sicurezza (serie 2.5.x supportata).
  - `TROUBLESHOOTING.md` – guida alla risoluzione problemi.
  - `PREREQUISITES.md` – prerequisiti e dipendenze.
  - `ROADMAP.md` – roadmap del progetto (questo file viene tenuto allineato alla 2.5.2).
  - `STRUCTURE.md` – (questo file) struttura del progetto.

- `setup/`  
  Script di build e packaging:
  - `comp.py` – build **GUI** con Nuitka.
  - `comp-CLI.py` – build **CLI** con Nuitka.
  - `comp-web.py` – build **Web** con Nuitka.
  - `installer.nsi` – script NSIS per installer Windows.
  - `version_info.txt` – metadati versione per installer.
  - (eventuali script ausiliari di build/pre-build).

- `tests/`  
  Test automatizzati (Pytest) per le varie componenti.

- Altri file di root importanti:
  - `version.py` (se presente) – versione distribuita o legacy.
  - `requirements.txt` – dipendenze Python.
  - `LICENSE` – licenza (GPLv3).
  - `README.md` – README principale del repository.

## 🔌 Interfacce principali

- **CLI** – `email_duplicate_cleaner.py`
  - Opzioni per scan, demo, scelta criteri, ecc.
- **GUI** – `email_cleaner_gui.py`
  - Usa `struttura/*` per menu, about, help, sponsor, logger, version.
- **Web** – `email_cleaner_web.py`
  - Interfaccia via browser agli stessi motori di scansione.

## 🧪 Testing

- I test sono eseguiti con **pytest** e si trovano in `tests/`.
- I casi di test coprono motore di scansione, logica di deduplicazione e parti critiche delle interfacce.

## 🧰 Build & Packaging (v2.5.2)

- Build tramite **Nuitka**:

  - GUI: `python setup/comp.py --clean` / `--debug`.
  - CLI: `python setup/comp-CLI.py --clean` / `--debug`.
  - Web: `python setup/comp-web.py --clean` / `--debug`.

- Installer Windows:

  - Pre-build script per sincronizzare versione (da `struttura/version.py` verso `setup/installer.nsi` e `setup/version_info.txt`).
  - Creazione installer con `makensis setup/installer.nsi`.

## 🔒 Sicurezza & Versioning

- Politiche di sicurezza e versioni supportate: `docs/SECURITY.md`.
- Versioning centralizzato in `struttura/version.py` (2.5.2) e riflesso in:
  - `CHANGELOG.md`.
  - Badge e testi in `README.md` (root).
  - Script di build e installer.

Questa struttura è valida per la **versione 2.5.2** ed è la base di riferimento per i rilasci futuri della serie 2.5.x.
