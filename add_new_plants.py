#!/usr/bin/env python3
"""
Script zum Hinzufügen der 10 neuen Schweizer Heilpflanzen zur bestehenden Datenbank
"""

import json

# Lade bestehende Datenbank
print("Lade bestehende Datenbank...")
with open('heilkraeuter_db.json', 'r', encoding='utf-8') as f:
    datenbank = json.load(f)

# Lade neue Pflanzen
print("Lade neue Pflanzen...")
with open('neue_pflanzen.json', 'r', encoding='utf-8') as f:
    neue_pflanzen_data = json.load(f)

# Füge neue Pflanzen hinzu
print(f"\nAktuelle Anzahl Pflanzen: {len(datenbank['pflanzen'])}")
datenbank['pflanzen'].extend(neue_pflanzen_data['neue_pflanzen'])
print(f"Neue Anzahl Pflanzen: {len(datenbank['pflanzen'])}")

# Speichere erweiterte Datenbank
print("\nSpeichere erweiterte Datenbank...")
with open('heilkraeuter_db_erweitert.json', 'w', encoding='utf-8') as f:
    json.dump(datenbank, f, ensure_ascii=False, indent=2)

print("\n✅ Fertig! Die erweiterte Datenbank wurde als 'heilkraeuter_db_erweitert.json' gespeichert.")
print("\nNeue Pflanzen:")
for pflanze in neue_pflanzen_data['neue_pflanzen']:
    print(f"  - {pflanze['deutsch']} ({pflanze['lateinisch']})")

print("\n📝 Nächste Schritte:")
print("1. Prüfe die neue Datei 'heilkraeuter_db_erweitert.json'")
print("2. Wenn alles ok ist, ersetze die alte Datei:")
print("   mv heilkraeuter_db_erweitert.json heilkraeuter_db.json")
print("3. Starte die App neu: streamlit run app.py")