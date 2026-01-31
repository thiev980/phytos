import streamlit as st
import json
from pathlib import Path
from PIL import Image
import os

# Seitenkonfiguration
st.set_page_config(
    page_title="Europäische Heilkräuter",
    page_icon="🌿",
    layout="wide"
)

# Daten laden
@st.cache_data
def load_data():
    with open('heilkraeuter_db.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()
pflanzen = data['pflanzen']

# Hilfsfunktionen
def get_alle_symptome():
    """Extrahiert alle einzigartigen Symptome aus der Datenbank"""
    symptome = set()
    for pflanze in pflanzen:
        symptome.update(pflanze['symptome'])
    return sorted(list(symptome))

def get_alle_wirkungen():
    """Extrahiert alle einzigartigen Wirkungen aus der Datenbank"""
    wirkungen = set()
    for pflanze in pflanzen:
        wirkungen.update(pflanze['wirkung'])
    return sorted(list(wirkungen))

def get_alle_pflanzennamen():
    """Extrahiert alle Pflanzennamen (Deutsch)"""
    return sorted([p['deutsch'] for p in pflanzen])

def get_monate():
    """Gibt eine Liste aller Monate zurück"""
    return [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]

def suche_nach_monat(monat):
    """Findet alle Pflanzen, die in einem bestimmten Monat geerntet werden können"""
    return [p for p in pflanzen if monat in p.get('erntemonate', [])]

def suche_nach_symptom(symptom):
    """Findet alle Pflanzen, die ein bestimmtes Symptom behandeln"""
    return [p for p in pflanzen if symptom in p['symptome']]

def suche_nach_wirkung(wirkung):
    """Findet alle Pflanzen mit einer bestimmten Wirkung"""
    return [p for p in pflanzen if wirkung in p['wirkung']]

def suche_pflanze(name):
    """Findet eine Pflanze nach deutschem Namen"""
    return next((p for p in pflanzen if p['deutsch'] == name), None)

def zeige_pflanze(pflanze, show_details=True):
    """Zeigt Details einer Pflanze an"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Bild anzeigen - einfach direkt laden
        bild_pfad = pflanze['bild']
        
        # Versuche das Bild zu laden
        if os.path.exists(bild_pfad):
            try:
                img = Image.open(bild_pfad)
                st.image(img, caption=pflanze['deutsch'], use_column_width=True)
            except Exception as e:
                st.error(f"Fehler beim Laden: {e}")
        else:
            st.info(f"📷 Bild noch nicht vorhanden:\n`{bild_pfad}`")
    
    with col2:
        st.subheader(f"{pflanze['deutsch']}")
        st.caption(f"*{pflanze['lateinisch']}*")
        
        st.markdown("**🎯 Symptome:**")
        st.write(", ".join(pflanze['symptome']))
        
        st.markdown("**💊 Wirkung:**")
        st.write(", ".join(pflanze['wirkung']))
        
        st.markdown("**☕ Zubereitung:**")
        st.write(pflanze['zubereitung'])
    
    # Weitere Details - nur wenn show_details=True
    if show_details:
        st.markdown("---")
        st.markdown("### 📋 Weitere Details")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("**🌸 Blüte/Erntezeit:**")
            st.write(pflanze['bluete_erntezeit'])
            if 'erntemonate' in pflanze and pflanze['erntemonate']:
                st.caption(f"Erntemonate: {', '.join(pflanze['erntemonate'])}")
            
            st.markdown("**📍 Vorkommen:**")
            st.write(pflanze['vorkommen'])
            
            st.markdown("**🍴 Als Nahrungsmittel:**")
            st.write(pflanze['nahrungsmittel'])
        
        with col4:
            st.markdown("**⚠️ Nebenwirkungen:**")
            st.write(pflanze['nebenwirkungen'])
            
            st.markdown("**🚫 Kontraindikationen:**")
            st.write(pflanze['kontraindikationen'])

# Haupttitel
st.title("🌿 Europäische Heilkräuter-Datenbank")
st.markdown("*Wissenschaftlich belegte Heilpflanzen für die einfache Anwendung*")
st.markdown("---")

# Tabs für verschiedene Suchoptionen
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Nach Symptom suchen",
    "💊 Nach Wirkung suchen", 
    "🌱 Nach Pflanze suchen",
    "📅 Nach Erntezeit suchen",
    "📚 Alle Pflanzen"
])

# Tab 1: Suche nach Symptom
with tab1:
    st.header("Suche nach Symptom")
    
    symptom = st.selectbox(
        "Wähle ein Symptom:",
        options=["---"] + get_alle_symptome(),
        key="symptom_select"
    )
    
    if symptom != "---":
        ergebnisse = suche_nach_symptom(symptom)
        st.success(f"**{len(ergebnisse)} Pflanze(n) gefunden für '{symptom}':**")
        
        for pflanze in ergebnisse:
            st.markdown("---")
            zeige_pflanze(pflanze, show_details=True)

# Tab 2: Suche nach Wirkung
with tab2:
    st.header("Suche nach Wirkung")
    
    wirkung = st.selectbox(
        "Wähle eine Wirkung:",
        options=["---"] + get_alle_wirkungen(),
        key="wirkung_select"
    )
    
    if wirkung != "---":
        ergebnisse = suche_nach_wirkung(wirkung)
        st.success(f"**{len(ergebnisse)} Pflanze(n) gefunden mit Wirkung '{wirkung}':**")
        
        for pflanze in ergebnisse:
            st.markdown("---")
            zeige_pflanze(pflanze, show_details=True)

# Tab 3: Suche nach Pflanze
with tab3:
    st.header("Suche nach Pflanze")
    
    pflanze_name = st.selectbox(
        "Wähle eine Pflanze:",
        options=["---"] + get_alle_pflanzennamen(),
        key="pflanze_select"
    )
    
    if pflanze_name != "---":
        pflanze = suche_pflanze(pflanze_name)
        if pflanze:
            zeige_pflanze(pflanze, show_details=True)

# Tab 4: Suche nach Erntezeit/Monat
with tab4:
    st.header("Suche nach Erntezeit")
    
    # Aktuellen Monat ermitteln (Default)
    from datetime import datetime
    aktuelle_monatszahl = datetime.now().month
    monate = get_monate()
    aktueller_monat = monate[aktuelle_monatszahl - 1]
    
    # Finde Index des aktuellen Monats in der Liste (mit "---" am Anfang)
    default_index = aktuelle_monatszahl  # +1 wegen "---" am Anfang, -1 für 0-basiert = 0
    
    monat = st.selectbox(
        "Wähle einen Monat:",
        options=["---"] + monate,
        index=default_index,  # Aktueller Monat vorausgewählt
        key="monat_select"
    )
    
    if monat != "---":
        ergebnisse = suche_nach_monat(monat)
        st.success(f"**{len(ergebnisse)} Pflanze(n) können im {monat} geerntet werden:**")
        
        if len(ergebnisse) == 0:
            st.info("Keine Pflanzen in diesem Monat verfügbar.")
        else:
            for pflanze in ergebnisse:
                st.markdown("---")
                zeige_pflanze(pflanze, show_details=True)

# Tab 5: Alle Pflanzen
with tab5:
    st.header("Alle Pflanzen (Übersicht)")
    
    # Kompakte Tabelle mit Expander für jede Pflanze
    for pflanze in pflanzen:
        with st.expander(f"🌿 {pflanze['deutsch']} (*{pflanze['lateinisch']}*)"):
            # Zeige Pflanze ohne zusätzliche Detail-Section (show_details=False würde reichen, aber wir zeigen direkt alles)
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Bild anzeigen - einfach direkt laden
                bild_pfad = pflanze['bild']
                
                if os.path.exists(bild_pfad):
                    try:
                        img = Image.open(bild_pfad)
                        st.image(img, caption=pflanze['deutsch'], use_column_width=True)
                    except Exception as e:
                        st.error(f"Fehler beim Laden: {e}")
                else:
                    st.info(f"📷 Bild noch nicht vorhanden")
            
            with col2:
                st.markdown(f"**Lateinisch:** *{pflanze['lateinisch']}*")
                st.markdown(f"**🎯 Symptome:** {', '.join(pflanze['symptome'])}")
                st.markdown(f"**💊 Wirkung:** {', '.join(pflanze['wirkung'])}")
                st.markdown(f"**☕ Zubereitung:** {pflanze['zubereitung']}")
            
            # Weitere Details direkt anzeigen
            st.markdown("---")
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown(f"**🌸 Blüte/Erntezeit:** {pflanze['bluete_erntezeit']}")
                if 'erntemonate' in pflanze and pflanze['erntemonate']:
                    st.caption(f"Erntemonate: {', '.join(pflanze['erntemonate'])}")
                st.markdown(f"**📍 Vorkommen:** {pflanze['vorkommen']}")
                st.markdown(f"**🍴 Als Nahrungsmittel:** {pflanze['nahrungsmittel']}")
            
            with col4:
                st.markdown(f"**⚠️ Nebenwirkungen:** {pflanze['nebenwirkungen']}")
                st.markdown(f"**🚫 Kontraindikationen:** {pflanze['kontraindikationen']}")

# Footer
st.markdown("---")
st.caption("""
**Wichtiger Hinweis:** Diese Datenbank dient nur zu Informationszwecken. 
Bei ernsthaften gesundheitlichen Beschwerden konsultieren Sie bitte einen Arzt oder Apotheker. 
Auch pflanzliche Mittel können Nebenwirkungen haben und mit Medikamenten interagieren.
""")