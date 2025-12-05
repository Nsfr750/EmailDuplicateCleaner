# 📍 Email Duplicate Cleaner – Roadmap (v2.5.2)

Questa roadmap descrive lo stato attuale del progetto alla **versione 2.5.2** e i piani principali per le versioni future.

## ✅ Stato attuale – v2.5.2

- **Versione**: 2.5.2

- **Interfacce**:

  - GUI desktop (PySide6) – `email_cleaner_gui.py`
  - Interfaccia Web (Flask) – `email_cleaner_web.py`
  - CLI – `email_duplicate_cleaner.py`

- **Funzionalità chiave**:

  - Rilevamento duplicati con criteri multipli (`strict`, `content`, `headers`, `subject-sender`)
  - Analisi avanzata (sender, timeline, allegati, thread, duplicati)
  - Supporto per più client email (Thunderbird, Apple Mail, Outlook, formati generici)
  - Modalità demo per test sicuri
  - Sistema di logging centralizzato (`struttura/logger.py`)
  - Sistema di versioning centralizzato (`struttura/version.py`)
  - Sistema di help/about/sponsor/menu modularizzato (`struttura/*`)
  - Build tramite **Nuitka** per GUI, CLI e Web (`setup/comp.py`, `setup/comp-CLI.py`, `setup/comp-web.py`)

## 🧩 Obiettivi a breve termine (2.5.x)

- **Miglioramenti UX**

  - Raffinare messaggi di errore e feedback nelle UI (GUI e Web)
  - Migliorare i testi di help e le traduzioni (IT/EN)

- **Strumenti di build e packaging**

  - Consolidare gli script di build GUI/CLI/Web
  - Rifinire l'installer NSIS (launcher per tutte le modalità dove applicabile)

- **Documentazione**

  - Ampliare esempi pratici nella documentazione (`docs/USER_GUIDE.md`, `docs/API_REFERENCE.md`)

## 🎯 Obiettivi di medio termine (2.6.x)

- **Funzionalità di analisi aggiuntive**

  - Report più dettagliati esportabili (HTML/PDF) dall’analisi
  - Filtri avanzati nella GUI/Web per analisi e risultati di scansione

- **Miglior integrazione con client email**

  - Migliore auto-rilevamento dei profili (Thunderbird/Outlook)
  - Wizard guidato per la prima configurazione account

- **Performance e scalabilità**

  - Ottimizzazioni per mailbox molto grandi
  - Miglior gestione della memoria durante le scansioni lunghe

## 🚀 Obiettivi di lungo termine (3.x)

- **Supporto multi-piattaforma avanzato**

  - Packaging nativo per più OS (Windows, possibili port per macOS/Linux desktop)

- **Plugin / estendibilità**

  - API pubblica più stabile per integrazioni esterne
  - Possibilità di aggiungere strategie di rilevamento duplicati personalizzate

- **Automazione**

  - Scheduling di scansioni automatiche tramite job esterni o integrazioni (es. Task Scheduler/cron)

## 📌 Linee guida

- Il progetto segue **Semantic Versioning**.
- Le novità e i cambiamenti concreti vengono documentati in **`CHANGELOG.md`**.
- Questa roadmap è indicativa e può cambiare in base a feedback, priorità e problemi di sicurezza/bug critici.
