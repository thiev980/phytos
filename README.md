# 🌿 Europäische Heilkräuter-Datenbank

Eine interaktive Web-App zur Suche von europäischen Heilpflanzen mit wissenschaftlich belegter Wirksamkeit.

## Features

- 🔍 **Suche nach Symptomen** - Finde Pflanzen, die bei bestimmten Beschwerden helfen
- 💊 **Suche nach Wirkung** - Filtere nach gewünschter Wirkweise (z.B. entzündungshemmend)
- 🌱 **Pflanzenprofile** - Detaillierte Informationen zu jeder Pflanze
- 📅 **Saisonale Suche** - Finde heraus, welche Pflanzen im aktuellen Monat geerntet werden können
- 📚 **Vollständige Übersicht** - Browse durch alle 20 Heilpflanzen

## Enthaltene Informationen

Jede Pflanze enthält:
- Lateinischer und deutscher Name
- Symptome und Wirkungen
- Zubereitungsanleitungen
- Erntezeit und Vorkommen
- Nebenwirkungen und Kontraindikationen
- Verwendung als Nahrungsmittel
- Fotos

## Technologie

- **Frontend:** Streamlit (Python)
- **Daten:** JSON-basierte Datenbank
- **Bilder:** PNG-Format

## Lokal ausführen

```bash
# Repository klonen
git clone https://github.com/thiev980/phytos.git
cd phytos

# Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# oder
.venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt

# App starten
streamlit run app.py
```

Die App öffnet sich unter `http://localhost:8501`

## Deployment

Diese App ist deployed auf Streamlit Community Cloud und öffentlich zugänglich.

## Hinweis

Diese Datenbank dient nur zu Informationszwecken. Bei ernsthaften gesundheitlichen Beschwerden konsultieren Sie bitte einen Arzt oder Apotheker. Auch pflanzliche Mittel können Nebenwirkungen haben und mit Medikamenten interagieren.

## Lizenz

Dieses Projekt ist für Bildungszwecke erstellt.