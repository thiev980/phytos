#!/usr/bin/env python3
"""
Debug Script: Prüft welche Pflanzen Bilder haben und welche nicht
"""

import json
import os
from pathlib import Path

# Lade Datenbank
print("=" * 60)
print("🔍 BILDER-DEBUG für Heilkräuter-Datenbank")
print("=" * 60)
print()

with open('heilkraeuter_db.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    pflanzen = data['pflanzen'] if 'pflanzen' in data else data

print(f"📊 Total: {len(pflanzen)} Pflanzen in der Datenbank")
print()

# Prüfe welche Bilder existieren
images_folder = Path('images')

if not images_folder.exists():
    print("❌ FEHLER: Ordner 'images/' existiert nicht!")
    print()
    print("Erstelle Ordner:")
    print("  mkdir images")
    print()
    exit(1)

print(f"✅ Ordner 'images/' gefunden")
print()

# Liste alle Dateien im images/ Ordner
image_files = list(images_folder.glob('*'))
print(f"📁 Dateien im images/ Ordner: {len(image_files)}")
print()

if image_files:
    print("Gefundene Dateien:")
    for f in sorted(image_files):
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.1f} KB)")
    print()

# Prüfe jede Pflanze
missing = []
found = []
wrong_path = []

extensions = ['.webp', '.jpg', '.jpeg', '.png', '.WEBP', '.JPG', '.JPEG', '.PNG']

for pflanze in pflanzen:
    name = pflanze['deutsch']
    bild_path = pflanze.get('bild', 'N/A')
    
    # Extrahiere Dateinamen aus bild_path
    if bild_path != 'N/A' and bild_path.startswith('images/'):
        # z.B. "images/kamille.png" -> "kamille.png"
        bild_filename = Path(bild_path).name
        
        # Prüfe ob genau diese Datei existiert
        actual_path = images_folder / bild_filename
        
        if actual_path.exists():
            found.append({
                'name': name,
                'path': bild_path,
                'actual': str(actual_path),
                'size': actual_path.stat().st_size / 1024
            })
        else:
            # Datei fehlt - prüfe ob mit anderer Extension existiert
            base_without_ext = actual_path.stem
            image_found = False
            actual_file = None
            
            for ext in extensions:
                test_path = images_folder / f"{base_without_ext}{ext}"
                if test_path.exists():
                    image_found = True
                    actual_file = test_path
                    break
            
            if image_found:
                wrong_path.append({
                    'name': name,
                    'path_in_db': bild_path,
                    'actual_file': str(actual_file),
                    'suggestion': f"Ändere 'bild' zu: images/{actual_file.name}"
                })
            else:
                missing.append({
                    'name': name,
                    'expected_path': bild_path,
                    'expected_file': str(actual_path)
                })
    else:
        wrong_path.append({
            'name': name,
            'path': bild_path
        })

# Ausgabe
print("=" * 60)
print("📊 ZUSAMMENFASSUNG")
print("=" * 60)
print()

print(f"✅ Bilder gefunden:  {len(found)}/{len(pflanzen)} ({len(found)/len(pflanzen)*100:.1f}%)")
print(f"❌ Bilder fehlen:    {len(missing)}/{len(pflanzen)} ({len(missing)/len(pflanzen)*100:.1f}%)")
print(f"⚠️  Falscher Pfad:   {len(wrong_path)}/{len(pflanzen)}")
print()

if found:
    print("=" * 60)
    print("✅ PFLANZEN MIT BILDERN")
    print("=" * 60)
    print()
    for item in found:
        print(f"✅ {item['name']}")
        print(f"   Pfad in DB: {item['path']}")
        print(f"   Datei:      {item['actual']}")
        print(f"   Größe:      {item['size']:.1f} KB")
        print()

if missing:
    print("=" * 60)
    print("❌ PFLANZEN OHNE BILDER")
    print("=" * 60)
    print()
    for item in missing:
        print(f"❌ {item['name']}")
        print(f"   Pfad in DB:     {item['expected_path']}")
        print(f"   Datei fehlt:    {item['expected_file']}")
        print()

if wrong_path:
    print("=" * 60)
    print("⚠️  PFLANZEN MIT FALSCHER EXTENSION")
    print("=" * 60)
    print()
    for item in wrong_path:
        print(f"⚠️  {item['name']}")
        print(f"   Pfad in DB:       {item['path_in_db']}")
        print(f"   Tatsächliche Datei: {item['actual_file']}")
        print(f"   💡 Vorschlag:      {item['suggestion']}")
        print()

# Empfehlungen
print("=" * 60)
print("💡 EMPFEHLUNGEN")
print("=" * 60)
print()

if missing:
    print("🔧 Fehlende Bilder:")
    print()
    for item in missing:
        filename = Path(item['expected_file']).name
        print(f"  - {filename}")
    print()
    
    print("  → Erstelle diese Bilder oder verwende Placeholder")
    print()

if wrong_path:
    print("🔧 Falsche Extension:")
    print()
    print("  Die Dateien existieren, aber mit anderer Extension.")
    print("  Entweder:")
    print("    A) Dateinamen im images/ Ordner ändern")
    print("    B) 'bild' Pfad im JSON ändern (siehe Vorschläge oben)")
    print()

print("📋 Naming Convention:")
print("  - Dateiname sollte Kleinbuchstaben sein")
print("  - Leerzeichen mit nichts ersetzen: 'Echte Kamille' → 'echtekamille.png'")
print("  - Oder: 'Echte Kamille' → 'kamille.png' (kurz)")
print("  - Extension: .png, .webp, .jpg (wird automatisch erkannt)")
print()

print("=" * 60)
print("✅ Debug abgeschlossen!")
print("=" * 60)