import streamlit as st
import streamlit.components.v1 as components
import json
import os
from PIL import Image
import requests
import base64
from io import BytesIO
import datetime
import hashlib

# Seitenkonfiguration mit SEO
st.set_page_config(
    page_title="Heilkräuter Schweiz | Wissenschaftlich belegte Phytotherapie | Heilpflanzen-Datenbank",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.phytotherapie.ch',
        'Report a bug': None,
        'About': """
        # Europäische Heilkräuter-Datenbank
        
        Wissenschaftlich fundierte Informationen zu europäischen Heilpflanzen.
        Basierend auf ESCOP-Monographien, Kommission E und aktueller Forschung.
        
        **Wichtig:** Diese App dient nur zu Informationszwecken und ersetzt keine ärztliche Beratung.
        """
    }
)

# SEO Meta Tags und Schema.org Structured Data
st.markdown("""
<meta name="description" content="Wissenschaftlich belegte Heilkräuter aus der Schweiz und Europa. Über 26 Heilpflanzen mit Anwendung, Wirkung, Zubereitung und Sicherheitshinweisen. Inklusive KI-Pflanzenerkennung.">
<meta name="keywords" content="Heilkräuter, Phytotherapie, Heilpflanzen, Schweiz, Europa, wissenschaftlich, Tee, Naturheilkunde, Arnika, Kamille, Brennnessel, Pflanzenerkennung">
<meta name="author" content="Heilkräuter-Datenbank Schweiz">
<meta name="robots" content="index, follow">
<meta name="language" content="DE">
<meta property="og:title" content="Heilkräuter Schweiz - Wissenschaftliche Heilpflanzen-Datenbank">
<meta property="og:description" content="Über 26 wissenschaftlich belegte Heilpflanzen mit Anwendung, Wirkung und Zubereitung. Inklusive KI-Pflanzenerkennung.">
<meta property="og:type" content="website">
<meta property="og:image" content="https://your-app-url.streamlit.app/app/static/heilkraeuter-og.png">

<!-- Schema.org Structured Data for Google -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "name": "Europäische Heilkräuter-Datenbank",
  "description": "Wissenschaftlich fundierte Datenbank mit über 26 europäischen Heilpflanzen, inklusive Anwendung, Wirkung, Zubereitung und Sicherheitshinweisen.",
  "specialty": "Phytotherapy",
  "audience": {
    "@type": "PeopleAudience",
    "audienceType": "Interessierte an Naturheilkunde, Phytotherapie-Anwender"
  },
  "medicalAudience": {
    "@type": "MedicalAudience",
    "audienceType": "Patient"
  },
  "mainEntity": {
    "@type": "ItemList",
    "itemListElement": [
      {
        "@type": "Thing",
        "name": "Heilpflanzen",
        "description": "Europäische Heilkräuter mit wissenschaftlich belegter Wirkung"
      }
    ]
  }
}
</script>
""", unsafe_allow_html=True)

# Plausible Analytics Integration
# Füge deine Domain ein nach dem Setup
PLAUSIBLE_DOMAIN = "phytos.streamlit.app"

# Plausible Analytics Script (richtig eingebunden für Streamlit)
components.html(f"""
<script defer data-domain="{PLAUSIBLE_DOMAIN}" src="https://plausible.io/js/script.js"></script>
""", height=0)

# Custom Event Tracking für Plausible
def track_plausible_event(event_name, props=None):
    """Track custom events in Plausible Analytics"""
    if props:
        props_json = json.dumps(props).replace('"', '\\"')
        components.html(f"""
        <script>
        if (window.plausible) {{
            window.plausible('{event_name}', {{props: {props_json}}});
        }}
        </script>
        """, height=0)
    else:
        components.html(f"""
        <script>
        if (window.plausible) {{
            window.plausible('{event_name}');
        }}
        </script>
        """, height=0)

# Custom CSS für besseres Design + SEO
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2e7d32;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        font-style: italic;
    }
    .seo-text {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #e0e0e0;
        margin: 20px 0;
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 8px;
    }
    .seo-text h3 {
        color: #4caf50;
        margin-top: 0;
    }
    .seo-text h4 {
        color: #81c784;
        margin-top: 20px;
    }
    .seo-text ul {
        color: #e0e0e0;
    }
    .disclaimer {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        margin: 20px 0;
        border-radius: 4px;
        color: #856404;
    }
    .disclaimer strong {
        color: #856404;
    }
    
    /* Back to top button */
    .back-to-top {
        position: fixed;
        bottom: 40px;
        right: 40px;
        background-color: #4caf50;
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        cursor: pointer;
        z-index: 1000;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s;
    }
    .back-to-top:hover {
        background-color: #45a049;
        transform: translateY(-5px);
    }
    
    @media (max-width: 768px) {
        .back-to-top {
            bottom: 20px;
            right: 20px;
            width: 45px;
            height: 45px;
            font-size: 20px;
        }
    }
    
    /* Improved mobile tabs */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        /* Make tabs wrap on mobile */
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
            gap: 5px;
        }
        
        .stTabs [data-baseweb="tab"] {
            flex-shrink: 0;
            white-space: nowrap;
            padding: 8px 12px;
            font-size: 0.9rem;
        }
        
        /* Sidebar optimization for mobile */
        [data-testid="stSidebar"] {
            width: 100%;
        }
        
        /* Make radio buttons larger on mobile */
        .stRadio > label {
            font-size: 1.1rem;
            padding: 12px 8px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Daten laden
@st.cache_data
def lade_pflanzen():
    with open('heilkraeuter_db.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['pflanzen'] if 'pflanzen' in data else data

pflanzen = lade_pflanzen()

# Hilfsfunktionen für Suche
def get_alle_symptome():
    symptome = set()
    for pflanze in pflanzen:
        symptome.update(pflanze['symptome'])
    return sorted(list(symptome))

def get_alle_wirkungen():
    wirkungen = set()
    for pflanze in pflanzen:
        wirkungen.update(pflanze['wirkung'])
    return sorted(list(wirkungen))

def get_alle_pflanzennamen():
    return sorted([p['deutsch'] for p in pflanzen])

def suche_nach_symptom(symptom):
    return [p for p in pflanzen if symptom in p['symptome']]

def suche_nach_wirkung(wirkung):
    return [p for p in pflanzen if wirkung in p['wirkung']]

def suche_pflanze(name):
    for p in pflanzen:
        if p['deutsch'].lower() == name.lower():
            return p
    return None

def suche_nach_lateinischem_namen(latin_name):
    """Sucht Pflanze nach lateinischem Namen (case-insensitive, flexibel)"""
    latin_name = latin_name.lower().strip()
    
    for p in pflanzen:
        pflanze_latin = p['lateinisch'].lower()
        
        if pflanze_latin == latin_name:
            return p
        
        if pflanze_latin.split()[0:2] == latin_name.split()[0:2]:
            return p
            
        if pflanze_latin.startswith(latin_name.split()[0]):
            return p
    
    return None

def suche_nach_erntezeit(monat):
    return [p for p in pflanzen if monat in p.get('erntemonate', [])]

# Pl@ntNet API Integration
def identify_plant_with_plantnet(image_file, api_key):
    try:
        
        url = "https://my-api.plantnet.org/v2/identify/all"
        
        image = Image.open(image_file)
        
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        buffered.seek(0)
        
        params = {'api-key': api_key}
        files = [('images', ('plant.jpg', buffered, 'image/jpeg'))]
        data = {'organs': ['auto']}
        
        response = requests.post(url, params=params, files=files, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Fehler: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"Fehler bei der Pflanzenerkennung: {str(e)}")
        return None

def zeige_pflanze(pflanze, show_details=False):
    """Zeigt eine Pflanze mit allen Details an"""
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Verwende bild-Pfad aus JSON statt deutschen Namen
        if 'bild' in pflanze and pflanze['bild']:
            image_path = pflanze['bild']
            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    st.image(img, use_column_width=True, caption=pflanze['deutsch'])
                except Exception as e:
                    st.info("📷 Bild nicht verfügbar")
            else:
                st.info("📷 Bild nicht verfügbar")
        else:
            st.info("📷 Bild nicht verfügbar")
    
    with col2:
        st.subheader(f"🌿 {pflanze['deutsch']}")
        st.markdown(f"*{pflanze['lateinisch']}*")
        st.markdown(f"**🩺 Symptome:** {', '.join(pflanze['symptome'])}")
        st.markdown(f"**💊 Wirkungen:** {', '.join(pflanze['wirkung'])}")
        
        if show_details:
            st.markdown("---")
            st.markdown("**📋 Anwendung & Zubereitung:**")
            st.markdown(f"{pflanze['zubereitung']}")
            
            st.markdown("---")
            st.markdown("**🌸 Erntezeit & Vorkommen:**")
            st.markdown(f"**Blüte/Erntezeit:** {pflanze['bluete_erntezeit']}")
            if 'erntemonate' in pflanze:
                st.markdown(f"**Erntemonate:** {', '.join(pflanze['erntemonate'])}")
            st.markdown(f"**Vorkommen:** {pflanze['vorkommen']}")
            st.markdown(f"**Als Nahrungsmittel:** {pflanze['nahrungsmittel']}")
            
            st.markdown("---")
            st.markdown("**⚠️ Sicherheitshinweise:**")
            st.markdown(f"**Nebenwirkungen:** {pflanze['nebenwirkungen']}")
            st.markdown(f"**Kontraindikationen:** {pflanze['kontraindikationen']}")

# Header mit SEO-Content - klickbar für Zurück zum Start
st.markdown("""
<style>
.main-header-link {
    text-decoration: none;
    color: inherit;
}
.main-header-link:hover {
    opacity: 0.8;
    cursor: pointer;
}
</style>
<a href="#europäische-heilkräuter-datenbank" class="main-header-link">
<div class="main-header">🌿 Europäische Heilkräuter-Datenbank</div>
</a>
""", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Wissenschaftlich belegte Heilpflanzen für die einfache Anwendung</div>', unsafe_allow_html=True)

# SEO-optimierter Intro-Text (kollabierbar)
with st.expander("ℹ️ Über diese Datenbank - Jetzt lesen!"):
    st.markdown("""
    <div class="seo-text">
    <h3>🌿 Heilkräuter aus der Schweiz und Europa – Wissenschaftlich fundiert</h3>
    
    Willkommen in der **wissenschaftlich fundierten Heilpflanzen-Datenbank mit integrierter KI-Pflanzenerkennung**! 
    Entdecke über **26 sorgfältig recherchierte Heilkräuter** mit praktischen Anwendungen, 
    die du zu Hause selbst umsetzen kannst.
    
    <h4>Was du hier findest:</h4>
    
    ✅ **Wissenschaftliche Fundierung**: Alle Pflanzen basieren auf ESCOP-Monographien, 
    Kommission E-Bewertungen und aktueller Phytotherapie-Forschung
    
    ✅ **Praktische Anwendung**: Einfache Zubereitungsmethoden wie Tees, die du zu Hause 
    selbst herstellen kannst
    
    ✅ **Sicherheit zuerst**: Detaillierte Informationen zu Nebenwirkungen, Kontraindikationen 
    und korrekter Dosierung
    
    ✅ **KI-Pflanzenerkennung**: Lade ein Foto hoch und lasse die Pflanze automatisch 
    identifizieren (powered by Pl@ntNet)
    
    ✅ **Saisonale Suche**: Finde heraus, welche Heilkräuter gerade Saison haben
    
    <h4>Für wen ist diese Datenbank?</h4>
    
    - 🌱 **Naturheilkunde-Interessierte**, die mehr über heimische Heilpflanzen lernen möchten
    - 🏔️ **Kräutersammler** in den Schweizer Alpen und im Mittelland
    - 🍵 **Tee-Liebhaber**, die eigene Heilkräuter-Tees zubereiten möchten
    - 📚 **Studierende** der Phytotherapie und Naturheilkunde
    - 👨‍⚕️ **Gesundheitsbewusste Menschen**, die pflanzliche Alternativen suchen
    
    <h4>Häufige Anwendungsbereiche:</h4>
    
    - Erkältungen und Atemwegserkrankungen (Thymian, Spitzwegerich, Holunder)
    - Verdauungsbeschwerden (Kamille, Pfefferminze, Fenchel)
    - Schlaf und Nervosität (Baldrian, Melisse, Hopfen)
    - Haut und Wundheilung (Ringelblume, Arnika, Kamille)
    - Harnwege (Brennnessel, Goldrute, Schachtelhalm)
    
    <h4>Wissenschaftliche Quellen:</h4>
    
    Diese Datenbank basiert auf anerkannten phytotherapeutischen Standardwerken:
    - ESCOP Monographs (European Scientific Cooperative on Phytotherapy)
    - Kommission E Monographien
    - Schweizerische Medizinische Gesellschaft für Phytotherapie
    - Institut für Komplementärmedizin, Universität Zürich
    - Agroscope Forschung Heilpflanzen
    
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Accordion-Style Navigation - Single Page mit aufklappbaren Sections
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 20px; border-radius: 10px; margin-bottom: 25px;
            text-align: center;">
    <h3 style="margin: 0; color: white;">🧭 Wähle eine Kategorie</h3>
    <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9rem;">
    Klicke auf eine Kategorie, um sie zu öffnen
    </p>
</div>
""", unsafe_allow_html=True)

# 🔍 SECTION 1: Nach Symptom suchen
with st.expander("🔍 **Nach Symptom suchen**", expanded=False):
    st.header("Suche nach Symptom")
    st.markdown("*Wähle ein Symptom, um passende Heilpflanzen zu finden*")
    
    symptom = st.selectbox(
        "Wähle ein Symptom:",
        options=["---"] + get_alle_symptome(),
        key="symptom_select"
    )
    
    if symptom != "---":
        # Track custom event
        track_plausible_event("Symptom Search", {"symptom": symptom})
        
        ergebnisse = suche_nach_symptom(symptom)
        if ergebnisse:
            st.success(f"**{len(ergebnisse)} Pflanze(n) gefunden für '{symptom}':**")
            
            for pflanze in ergebnisse:
                st.markdown("---")
                zeige_pflanze(pflanze, show_details=True)
        else:
            st.warning("Keine Pflanzen gefunden.")

# 💊 SECTION 2: Nach Wirkung suchen
with st.expander("💊 **Nach Wirkung suchen**", expanded=False):
    st.header("Suche nach Wirkung")
    st.markdown("*Finde Heilpflanzen mit bestimmten pharmakologischen Wirkungen*")
    
    wirkung = st.selectbox(
        "Wähle eine Wirkung:",
        options=["---"] + get_alle_wirkungen(),
        key="wirkung_select"
    )
    
    if wirkung != "---":
        # Track custom event
        track_plausible_event("Wirkung Search", {"wirkung": wirkung})
        
        ergebnisse = suche_nach_wirkung(wirkung)
        if ergebnisse:
            st.success(f"**{len(ergebnisse)} Pflanze(n) gefunden mit Wirkung '{wirkung}':**")
            
            for pflanze in ergebnisse:
                st.markdown("---")
                zeige_pflanze(pflanze, show_details=True)
        else:
            st.warning("Keine Pflanzen gefunden.")

# 🌿 SECTION 3: Nach Pflanze suchen
with st.expander("🌿 **Nach Pflanze suchen**", expanded=False):
    st.header("Suche nach Pflanze")
    st.markdown("*Detaillierte Informationen zu einzelnen Heilpflanzen*")
    
    pflanze_name = st.selectbox(
        "Wähle eine Pflanze:",
        options=["---"] + get_alle_pflanzennamen(),
        key="pflanze_select"
    )
    
    if pflanze_name != "---":
        # Track custom event
        track_plausible_event("Plant View", {"plant": pflanze_name})
        
        pflanze = suche_pflanze(pflanze_name)
        if pflanze:
            zeige_pflanze(pflanze, show_details=True)

# 📅 SECTION 4: Nach Erntezeit suchen
with st.expander("📅 **Nach Erntezeit suchen**", expanded=False):
    st.header("Suche nach Erntezeit")
    st.markdown("*Finde heraus, welche Heilkräuter gerade Saison haben*")
    
    monate = ["Januar", "Februar", "März", "April", "Mai", "Juni", 
              "Juli", "August", "September", "Oktober", "November", "Dezember"]
    aktueller_monat = monate[datetime.datetime.now().month - 1]
    
    monat = st.selectbox(
        "Wähle einen Monat:",
        options=monate,
        index=monate.index(aktueller_monat),
        key="monat_select"
    )
    
    # Track custom event
    track_plausible_event("Harvest Search", {"month": monat})
    
    ergebnisse = suche_nach_erntezeit(monat)
    
    if ergebnisse:
        st.success(f"**{len(ergebnisse)} Pflanze(n) im {monat} verfügbar:**")
        for pflanze in ergebnisse:
            st.markdown("---")
            zeige_pflanze(pflanze, show_details=True)
    else:
        st.info(f"Keine Pflanzen für {monat} in der Datenbank.")

# 📚 SECTION 5: Alle Pflanzen
with st.expander("📚 **Alle Pflanzen anzeigen**", expanded=False):
    st.header("Alle Pflanzen (Übersicht)")
    st.markdown(f"*Gesamte Datenbank: {len(pflanzen)} wissenschaftlich belegte Heilpflanzen*")
    
    for pflanze in pflanzen:
        st.markdown("---")
        st.markdown(f"### 🌿 {pflanze['deutsch']}")
        st.markdown(f"*{pflanze['lateinisch']}*")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown(f"**🩺 Symptome:** {', '.join(pflanze['symptome'])}")
            st.markdown(f"**💊 Wirkungen:** {', '.join(pflanze['wirkung'])}")
            st.markdown(f"**📋 Zubereitung:** {pflanze['zubereitung']}")
        
        with col4:
            st.markdown(f"**🌸 Blüte/Erntezeit:** {pflanze['bluete_erntezeit']}")
            if 'erntemonate' in pflanze:
                st.markdown(f"**📅 Erntemonate:** {', '.join(pflanze['erntemonate'])}")
            st.markdown(f"**📍 Vorkommen:** {pflanze['vorkommen']}")
            st.markdown(f"**🍴 Als Nahrungsmittel:** {pflanze['nahrungsmittel']}")
        
        st.markdown(f"**⚠️ Nebenwirkungen:** {pflanze['nebenwirkungen']}")
        st.markdown(f"**🚫 Kontraindikationen:** {pflanze['kontraindikationen']}")

# 📸 SECTION 6: Pflanze erkennen
with st.expander("📸 **Pflanze erkennen (KI)**", expanded=False):
    st.header("📸 Pflanze erkennen")
    st.markdown("""
    Lade ein Foto einer Pflanze hoch und die App versucht, sie zu identifizieren.
    
    **Tipps für bessere Ergebnisse:**
    - 📸 Fotografiere Blätter, Blüten oder Früchte deutlich
    - ☀️ Gutes Licht verwenden
    - 🎯 Pflanze sollte im Fokus sein
    - 🌿 Mehrere Pflanzenteile auf einem Foto sind hilfreich
    """)
    
    st.markdown("---")
    
    try:
        api_key = st.secrets["PLANTNET_API_KEY"]
        st.success("✅ API Key geladen - bereit zur Pflanzenerkennung!")
    except (KeyError, FileNotFoundError):
        st.markdown("### 🔑 Pl@ntNet API Setup")
        st.info("💡 Kein API Key hinterlegt. Bitte gib deinen eigenen Key ein.")
        
        with st.expander("ℹ️ Wie bekomme ich einen API Key?"):
            st.markdown("""
            1. Gehe zu [Pl@ntNet API](https://my.plantnet.org/)
            2. Erstelle einen kostenlosen Account
            3. Erstelle einen API Key unter "Your API keys"
            4. Füge den Key unten ein
            
            **Kostenlos:** 500 Identifikationen pro Tag
            """)
        
        api_key = st.text_input(
            "Pl@ntNet API Key:",
            type="password",
            help="Dein Pl@ntNet API Key. Wird nicht gespeichert."
        )
        
        if not api_key:
            st.warning("⚠️ Bitte gib deinen Pl@ntNet API Key ein, um fortzufahren.")
            st.stop()
    
    st.markdown("---")
    st.markdown("### 📤 Foto hochladen")
    
    uploaded_file = st.file_uploader(
        "Wähle ein Pflanzenfoto:",
        type=['jpg', 'jpeg', 'png'],
        help="Unterstützte Formate: JPG, PNG"
    )
    
    if uploaded_file is not None:
        # Track image upload event
        track_plausible_event("Image Upload", {"feature": "plant_recognition"})
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Hochgeladenes Bild", use_column_width=True)
        
        with col2:
            st.markdown("### 🔍 Identifikation läuft...")
            
            with st.spinner("Pflanze wird analysiert..."):
                result = identify_plant_with_plantnet(uploaded_file, api_key)
            
            if result and 'results' in result:
                st.success("✅ Identifikation abgeschlossen!")
                
                st.markdown("---")
                st.markdown("### 🌿 Gefundene Pflanzen:")
                
                for i, plant in enumerate(result['results'][:5], 1):
                    score = plant['score'] * 100
                    species_name = plant['species']['scientificNameWithoutAuthor']
                    common_names = plant['species'].get('commonNames', [])
                    
                    matched_plant = suche_nach_lateinischem_namen(species_name)
                    
                    st.markdown("---")
                    st.markdown(f"### #{i} - {species_name}")
                    st.markdown(f"**Übereinstimmung:** {score:.1f}%")
                    st.progress(score / 100)
                    
                    if common_names:
                        st.markdown(f"**Volksnamen:** {', '.join(common_names[:3])}")
                    
                    if matched_plant:
                        st.success("✨ Diese Pflanze ist in unserer Heilkräuter-Datenbank!")
                        st.markdown("---")
                        
                        col_a, col_b = st.columns([1, 2])
                        
                        with col_a:
                            # Verwende bild-Pfad aus JSON
                            if 'bild' in matched_plant and matched_plant['bild']:
                                image_path = matched_plant['bild']
                                if os.path.exists(image_path):
                                    try:
                                        img = Image.open(image_path)
                                        st.image(img, use_column_width=True, caption=matched_plant['deutsch'])
                                    except Exception as e:
                                        st.info("📷 Bild nicht verfügbar")
                                else:
                                    st.info("📷 Bild nicht verfügbar")
                            else:
                                st.info("📷 Bild nicht verfügbar")
                        
                        with col_b:
                            st.subheader(f"🌿 {matched_plant['deutsch']}")
                            st.markdown(f"*{matched_plant['lateinisch']}*")
                            st.markdown(f"**🩺 Symptome:** {', '.join(matched_plant['symptome'])}")
                            st.markdown(f"**💊 Wirkungen:** {', '.join(matched_plant['wirkung'])}")
                        
                        st.markdown("---")
                        st.markdown("**📋 Anwendung & Zubereitung:**")
                        st.markdown(f"- **Zubereitung:** {matched_plant['zubereitung']}")
                        
                        st.markdown("**🌸 Erntezeit & Vorkommen:**")
                        st.markdown(f"- **Blüte/Erntezeit:** {matched_plant['bluete_erntezeit']}")
                        if 'erntemonate' in matched_plant:
                            st.markdown(f"- **Erntemonate:** {', '.join(matched_plant['erntemonate'])}")
                        st.markdown(f"- **Vorkommen:** {matched_plant['vorkommen']}")
                        st.markdown(f"- **Als Nahrungsmittel:** {matched_plant['nahrungsmittel']}")
                        
                        st.markdown("**⚠️ Sicherheitshinweise:**")
                        st.markdown(f"- **Nebenwirkungen:** {matched_plant['nebenwirkungen']}")
                        st.markdown(f"- **Kontraindikationen:** {matched_plant['kontraindikationen']}")
                    else:
                            st.info("ℹ️ Diese Pflanze ist nicht in unserer Heilkräuter-Datenbank.")
                            st.markdown(f"*Möglicherweise keine dokumentierte Heilwirkung für europäische Phytotherapie.*")
            
            elif result:
                st.warning("⚠️ Keine Pflanzen erkannt. Versuche ein anderes Foto.")
            else:
                st.error("❌ Fehler bei der Identifikation. Bitte versuche es erneut.")


# 📖 SECTION 7: Anwendungs-Guide
with st.expander("📖 **Anwendungs-Guide**", expanded=False):
    
    st.header("📖 Anwendungs-Guide für Heilkräuter")
    st.markdown("*Praktisches Wissen für die sichere Anwendung zu Hause*")
    
    st.markdown("---")
    
    # Übersicht
    st.info("""
    **In diesem Guide:** Tee-Zubereitung • Sammeln & Trocknen • Umschläge & Bäder • 
    Tinkturen & Salben • Sicherheit & Dosierung
    """)
    
    # 🍵 TEE-ZUBEREITUNG
    st.markdown("---")
    st.markdown("## 🍵 Tee-Zubereitung")
    st.markdown("""
    ### Heißer Aufguss (Infus)
    **Für:** Blüten, Blätter (Kamille, Pfefferminze, Thymian)  
    **Methode:** 1-2 TL mit kochendem Wasser übergießen, zudecken, 5-10 Min ziehen, abseihen  
    **Wichtig:** Zudecken, damit ätherische Öle nicht verdampfen!
    
    ### Kaltauszug (Mazeration)
    **Für:** Schleimstoffhaltige Pflanzen (Eibisch, Malve, Baldrian)  
    **Methode:** 1-2 TL mit kaltem Wasser, 2-8 Std ziehen, optional leicht erwärmen  
    **Warum:** Schleimstoffe lösen sich besser in kaltem Wasser
    
    ### Abkochung (Dekokt)
    **Für:** Wurzeln, Rinden (Baldrianwurzel, Schachtelhalm)  
    **Methode:** 1-2 TL mit kaltem Wasser ansetzen, 10-15 Min kochen, abseihen  
    **Warum:** Wirkstoffe aus harten Teilen brauchen Hitze
    
    **Dosierung:** 2-3 Tassen täglich • Nicht länger als 2-3 Wochen ohne Pause
    """)
    
    # 🌿 SAMMELN & TROCKNEN
    st.markdown("---")
    st.markdown("## 🌿 Sammeln & Trocknen")
    st.markdown("""
    ### Sammeln
    **Wann:** Vormittag nach dem Tau (10-12 Uhr), trockenes Wetter  
    **Wo:** Saubere Standorte, nicht an Straßen!  
    **Wie:** Max. 1/3 ernten, geschützte Arten meiden (Arnika!)
    
    ### Trocknen
    **Methode 1 - Lufttrocknung (beste!):**  
    • Lose auf Tuch ausbreiten oder Bündel aufhängen  
    • Dunkel, warm (20-25°C), luftig  
    • Täglich wenden  
    • 5-10 Tage
    
    **Methode 2 - Dörrautomat:**  
    • Max. 35°C (bei ätherischen Ölen)  
    • 4-8 Stunden
    
    ### Lagerung
    **Behälter:** Dunkelglas, Papiertüten  
    **Bedingungen:** Kühl, trocken, dunkel  
    **Haltbarkeit:** Blüten/Blätter 1 Jahr, Wurzeln 2-3 Jahre  
    **Beschriften:** Name, Pflanzenteil, Datum
    """)
    
    # 🧴 UMSCHLÄGE & BÄDER
    st.markdown("---")
    st.markdown("## 🧴 Umschläge & Bäder")
    st.markdown("""
    ### Kalter Umschlag
    **Wann:** Entzündungen, Schwellungen, Prellungen  
    **Wie:** Starken Tee (3-4 TL) zubereiten, abkühlen, Tuch tränken, 15-20 Min auflegen  
    **Beispiel:** Arnika bei Prellungen
    
    ### Warmer Umschlag
    **Wann:** Verspannungen, Krämpfe  
    **Wie:** Heißen Tee, Tuch tränken (nicht zu heiß!), 20-30 Min auflegen  
    **Beispiel:** Kamille bei Bauchschmerzen
    
    ### Breiumschlag (Frisch)
    **Wann:** Insektenstiche, erste Hilfe unterwegs  
    **Wie:** Frische Blätter zerquetschen, direkt auflegen  
    **Beispiel:** Spitzwegerich bei Mückenstichen
    
    ### Vollbad
    **Wie:** 100-200g Kräuter auf 2-3L Wasser, Sud ins Bad, 36-38°C, max. 20 Min  
    **Beispiele:** Kamille (Haut), Thymian (Atemwege)
    
    ### Sitzbad
    **Wie:** 50g Kräuter auf 1L Wasser, Sud in Sitzwanne, 36-38°C, 10-15 Min  
    **Beispiel:** Kamille bei Hämorrhoiden
    """)
    
    # 💊 TINKTUREN & SALBEN
    st.markdown("---")
    st.markdown("## 💊 Tinkturen & Salben")
    st.markdown("""
    ### Tinktur (alkoholischer Auszug)
    **Herstellung:**  
    1. Glas zu 1/3-1/2 mit Kräutern füllen  
    2. Mit 40-70% Alkohol (Korn, Wodka) bedecken  
    3. 2-6 Wochen ziehen, täglich schütteln  
    4. Abseihen, in dunkle Tropfflasche füllen  
    
    **Dosierung:** 3x täglich 20-30 Tropfen in Wasser  
    **Haltbarkeit:** 3-5 Jahre  
    **Nicht für:** Kinder, Schwangere, Alkoholiker
    
    ### Ölauszug
    **Herstellung:**  
    1. Getrocknete Kräuter (2/3) in Glas  
    2. Mit Öl (Oliven-, Mandelöl) bedecken  
    3. 4-6 Wochen auf Fensterbank, täglich schütteln  
    4. Abseihen  
    
    **Verwendung:** Massage, Basis für Salben  
    **Haltbarkeit:** 6-12 Monate  
    **Beispiel:** Johanniskraut-Rotöl
    
    ### Salbe
    **Rezept:** 100ml Ölauszug + 10-15g Bienenwachs  
    **Herstellung:** Im Wasserbad schmelzen, in Tiegel füllen  
    **Haltbarkeit:** 6-12 Monate
    """)
    
    # ⚠️ SICHERHEIT
    st.markdown("---")
    st.markdown("## ⚠️ Sicherheit & Dosierung")
    st.markdown("""
    ### Dosierung
    **Erwachsene:** 1-2 TL getrocknete Kräuter pro Tasse, 2-3 Tassen täglich  
    **Kinder (6-12 Jahre):** Halbe Dosis  
    **Kinder (2-6 Jahre):** Viertel Dosis, nur milde Kräuter  
    **Säuglinge:** Nur nach ärztlicher Anweisung!
    
    ### Anwendungsdauer
    **Akut (Erkältung):** Max. 2-3 Wochen  
    **Chronisch:** 6-8 Wochen, dann 2 Wochen Pause  
    **Kuren:** 4-6 Wochen, dann 4 Wochen Pause
    
    ### Schwangerschaft & Stillzeit
    **❌ Nicht verwenden:** Johanniskraut, Salbei (therapeutisch), Gundermann, Schafgarbe  
    **✅ In Maßen ok:** Kamille, Fenchel, Lindenblüten, Melisse  
    **Grundregel:** IMMER mit Arzt/Hebamme absprechen!
    
    ### Wechselwirkungen
    **Johanniskraut:** Viele! (Antidepressiva, Pille, Blutverdünner)  
    **Baldrian:** Verstärkt Schlafmittel  
    **Grundregel:** Bei Dauermedikation Arzt/Apotheker fragen!
    
    ### Wann zum Arzt?
    - Starke Schmerzen, hohes Fieber (>39°C)
    - Atemnot, allergische Reaktionen
    - Keine Besserung nach 1 Woche
    - Bei chronischen Erkrankungen immer ärztliche Begleitung
    
    ### Korbblütler-Allergie
    **Vorsicht bei:** Kamille, Arnika, Ringelblume, Schafgarbe  
    **Test:** Kleine Menge trinken, 24h warten  
    **Bei Allergie:** Diese Pflanzen meiden!
    """)
    
    st.markdown("---")
    
    st.warning("""
    **⚠️ Wichtig:** Dieser Guide ersetzt keine ärztliche Beratung! Bei Krankheiten 
    immer einen Arzt konsultieren. Heilkräuter sind wirksam, aber nicht harmlos - 
    richtige Anwendung ist entscheidend!
    """)

# Info-Box mit Statistiken
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); 
            color: white; padding: 20px; border-radius: 10px; margin: 20px 0;
            text-align: center;">
    <h3 style="margin: 0 0 10px 0; color: white;">🌿 Datenbank-Info</h3>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 15px;">
        <div>
            <div style="font-size: 2rem; font-weight: bold;">36</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Heilpflanzen</div>
        </div>
        <div>
            <div style="font-size: 2rem; font-weight: bold;">100%</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">Wissenschaftlich belegt</div>
        </div>
        <div>
            <div style="font-size: 2rem; font-weight: bold;">🔬</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">ESCOP + Kommission E</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Back to Top Button
components.html("""
<a href="#europäische-heilkräuter-datenbank" style="text-decoration: none;">
    <div class="back-to-top" title="Zurück nach oben">
        ↑
    </div>
</a>
""", height=0)

# Footer mit SEO-Content
st.markdown("---")
st.markdown("""
<div class="disclaimer">
<strong>⚠️ Wichtiger medizinischer Hinweis:</strong><br>
Diese Datenbank dient ausschließlich zu Informationszwecken. Die Informationen ersetzen keine 
ärztliche Beratung, Diagnose oder Behandlung. Bei ernsthaften gesundheitlichen Beschwerden 
konsultieren Sie bitte einen Arzt, Apotheker oder Heilpraktiker. Auch pflanzliche Mittel können 
Nebenwirkungen haben und mit Medikamenten interagieren.
</div>
""", unsafe_allow_html=True)

st.caption("""
**Wissenschaftliche Quellen:** ESCOP Monographs, Kommission E, Schweizerische Medizinische Gesellschaft 
für Phytotherapie, Institut für Komplementärmedizin (Universität Zürich), Agroscope

**Pflanzenerkennung:** Powered by Pl@ntNet API | **Datenbank:** {} Heilpflanzen | **Stand:** Februar 2026
""".format(len(pflanzen)))