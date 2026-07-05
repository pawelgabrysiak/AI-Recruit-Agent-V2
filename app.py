import streamlit as st
import json
import os
from utils.logger import setup_logger
from utils.config import config

logger = setup_logger("streamlit_app")

# ──────────────────────────────────────────
# Konfiguracja strony
# ──────────────────────────────────────────
st.set_page_config(
    page_title="AI-Recruit-Agent V2",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────
# CSS – ciemny, nowoczesny motyw
# ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #0d0f14;
    --surface: #161923;
    --surface2: #1e2330;
    --accent: #6c8aff;
    --accent2: #a78bfa;
    --success: #34d399;
    --warning: #fbbf24;
    --danger: #f87171;
    --text: #e2e8f0;
    --muted: #64748b;
    --border: rgba(108,138,255,0.15);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

/* Karty */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.card:hover { border-color: rgba(108,138,255,0.35); }

/* Metric box */
.metric-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.metric-box .value {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-box .label {
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 4px;
}

/* Skill badge */
.skill-ok   { background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.3);  color: #34d399; border-radius: 8px; padding: 6px 12px; display: inline-block; margin: 3px; font-size: 0.85rem; }
.skill-warn { background: rgba(251,191,36,0.12);  border: 1px solid rgba(251,191,36,0.3);  color: #fbbf24; border-radius: 8px; padding: 6px 12px; display: inline-block; margin: 3px; font-size: 0.85rem; }
.skill-bad  { background: rgba(248,113,113,0.12); border: 1px solid rgba(248,113,113,0.3); color: #f87171; border-radius: 8px; padding: 6px 12px; display: inline-block; margin: 3px; font-size: 0.85rem; }

/* Progress bar */
.progress-wrap { background: var(--surface2); border-radius: 99px; height: 10px; overflow: hidden; margin-top: 8px; }
.progress-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--accent), var(--accent2)); transition: width 0.6s ease; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.4rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Text areas & inputs */
.stTextArea textarea, .stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* File uploader */
.stFileUploader {
    background: var(--surface2) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 12px !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Alert boxes */
.stSuccess { background: rgba(52,211,153,0.08) !important; border-left: 3px solid #34d399 !important; }
.stWarning { background: rgba(251,191,36,0.08)  !important; border-left: 3px solid #fbbf24 !important; }
.stError   { background: rgba(248,113,113,0.08) !important; border-left: 3px solid #f87171 !important; }

/* Hero header */
.hero {
    background: linear-gradient(135deg, rgba(108,138,255,0.08), rgba(167,139,250,0.08));
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 32px;
}
.hero h1 { font-size: 2.4rem; margin-bottom: 8px; }
.hero p  { color: var(--muted); font-size: 1.05rem; }

/* Tag */
.tag { background: rgba(108,138,255,0.15); color: var(--accent); border-radius: 6px; padding: 2px 10px; font-size: 0.8rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────
for key, default in {
    "profile": None,
    "offer_text": "",
    "analysis": None,
    "cover_letter": "",
    "model": config.get("models", {}).get("default", "mistral"),
    "groq_api_key": "",
    "gemini_api_key": "",
    "deepseek_api_key": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ──────────────────────────────────────────
# SIDEBAR – NAWIGACJA
# ──────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 AI-Recruit-Agent V2")
    st.markdown("---")

    page = st.radio(
        "Nawigacja",
        ["🏠  Strona główna", "👤  Profil kandydata", "🔍  Analiza AI", "📄  List motywacyjny", "ℹ️  Jak to działa"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Ustawienia modelu
    st.markdown("#### ⚙️ Ustawienia modelu")
    st.session_state.model = st.selectbox(
        "Wybierz dostawcę i model",
        config.get("models", {}).get("available", ["mistral", "llama3"]),
        index=0
    )
    
    if st.session_state.model.startswith("groq/"):
        st.session_state.groq_api_key = st.text_input("Klucz API Groq", value=st.session_state.groq_api_key, type="password")
        if not st.session_state.groq_api_key and not os.environ.get("GROQ_API_KEY"):
            st.warning("Podaj klucz API Groq w polu powyżej lub w pliku .env")
            
    elif st.session_state.model.startswith("gemini/"):
        st.session_state.gemini_api_key = st.text_input("Klucz API Gemini", value=st.session_state.gemini_api_key, type="password")
        if not st.session_state.gemini_api_key and not os.environ.get("GEMINI_API_KEY"):
            st.warning("Podaj klucz API Gemini w polu powyżej lub w pliku .env")
            
    elif st.session_state.model.startswith("deepseek/"):
        st.session_state.deepseek_api_key = st.text_input("Klucz API DeepSeek", value=st.session_state.deepseek_api_key, type="password")
        if not st.session_state.deepseek_api_key and not os.environ.get("DEEPSEEK_API_KEY"):
            st.warning("Podaj klucz API DeepSeek w polu powyżej lub w pliku .env")

    if st.session_state.profile:
        st.markdown("---")
        name = f"{st.session_state.profile.get('imie','')} {st.session_state.profile.get('nazwisko','')}"
        st.markdown(f"**Profil:** {name}")
        skills_count = len(st.session_state.profile.get("umiejetnosci", []))
        st.markdown(f"**Umiejętności:** {skills_count}")


# ──────────────────────────────────────────
# STRONY
# ──────────────────────────────────────────

# ── 1. STRONA GŁÓWNA ──
if page == "🏠  Strona główna":
    st.markdown("""
    <div class="hero">
        <h1>🤖 AI-Recruit-Agent V2</h1>
        <p>Twój inteligentny asystent do szukania pracy. Wgraj CV jako PDF, a my ocenimy Twoje dopasowanie do oferty i wygenerujemy spersonalizowany list motywacyjny. Obsługuje potężne chmury (Groq, Gemini, DeepSeek) oraz w pełni prywatną, lokalną Ollamę.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="card">
            <h3>👤 Profil kandydata</h3>
            <p style="color:#64748b">Wczytaj swój profil JSON lub uzupełnij dane ręcznie.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="card">
            <h3>🔍 Analiza AI</h3>
            <p style="color:#64748b">AI ocenia dopasowanie Twoich umiejętności do wymagań oferty.</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="card">
            <h3>📄 List motywacyjny</h3>
            <p style="color:#64748b">Wygeneruj spersonalizowany list gotowy do wysyłki.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("### 🚀 Jak zacząć?")
    st.markdown("""
    1. Przejdź do **Profil kandydata** i wczytaj swój plik JSON (lub uzupełnij ręcznie)
    2. Wklej treść ogłoszenia o pracę
    3. Przejdź do **Analiza AI** i kliknij „Analizuj"
    4. Przejdź do **List motywacyjny** i wygeneruj list
    """)

    if not st.session_state.profile:
        st.info("👆 Zacznij od uzupełnienia profilu w zakładce **Profil kandydata**")
    else:
        st.success(f"✅ Profil wczytany: **{st.session_state.profile['imie']} {st.session_state.profile['nazwisko']}**")


# ── 2. PROFIL KANDYDATA ──
elif page == "👤  Profil kandydata":
    st.markdown("## 👤 Profil kandydata")

    tab1, tab2 = st.tabs(["📂 Wczytaj plik JSON", "✏️ Uzupełnij ręcznie"])

    with tab1:
        profile_file = st.file_uploader("Wybierz plik z profilem kandydata (JSON lub PDF)", type=["json", "pdf"])
        if profile_file:
            try:
                from utils.parser import profile_from_dict, parse_pdf_resume, extract_profile_from_text
                
                if profile_file.name.lower().endswith(".json"):
                    raw = json.load(profile_file)
                    st.session_state.profile = profile_from_dict(raw)
                    st.success("✅ Profil wczytany pomyślnie!")
                elif profile_file.name.lower().endswith(".pdf"):
                    with st.spinner("📄 Przetwarzanie PDF przez AI (może to zająć chwilę)..."):
                        with open("temp.pdf", "wb") as f:
                            f.write(profile_file.getbuffer())
                        
                        pdf_text = parse_pdf_resume("temp.pdf")
                        api_keys_dict = {"GROQ_API_KEY": st.session_state.groq_api_key, "GEMINI_API_KEY": st.session_state.gemini_api_key, "DEEPSEEK_API_KEY": st.session_state.deepseek_api_key}
                        st.session_state.profile = extract_profile_from_text(pdf_text, model=st.session_state.model, api_keys=api_keys_dict)
                        
                        import os
                        if os.path.exists("temp.pdf"):
                            os.remove("temp.pdf")
                            
                    st.success("✅ Profil wyekstrahowany z pliku PDF!")
            except Exception as e:
                st.error(f"❌ Błąd: {e}")

        if st.session_state.profile:
            st.markdown("#### Podgląd profilu:")
            st.json(st.session_state.profile)

    with tab2:
        st.markdown("Uzupełnij dane ręcznie:")
        col1, col2 = st.columns(2)
        with col1:
            imie = st.text_input("Imię")
            nazwisko = st.text_input("Nazwisko")
            lokalizacja = st.text_input("Lokalizacja (np. Warszawa)")
        with col2:
            umiejetnosci_raw = st.text_area("Umiejętności (każda w nowej linii)", height=120,
                                             placeholder="Python\nSQL\nMachine Learning")
            projekty_raw = st.text_area("Projekty (każdy w nowej linii)", height=80,
                                         placeholder="System rekomendacyjny\nAnaliza danych")

        if st.button("💾 Zapisz profil"):
            if not imie or not nazwisko or not umiejetnosci_raw:
                st.warning("Wypełnij przynajmniej: imię, nazwisko i umiejętności.")
            else:
                st.session_state.profile = {
                    "imie": imie,
                    "nazwisko": nazwisko,
                    "lokalizacja": lokalizacja,
                    "umiejetnosci": [s.strip() for s in umiejetnosci_raw.strip().splitlines() if s.strip()],
                    "projekty": [p.strip() for p in projekty_raw.strip().splitlines() if p.strip()],
                    "doswiadczenie": []
                }
                st.success("✅ Profil zapisany!")

    st.markdown("---")
    st.markdown("## 📄 Ogłoszenie o pracę")
    st.session_state.offer_text = st.text_area(
        "Wklej treść ogłoszenia o pracę",
        value=st.session_state.offer_text,
        height=250,
        placeholder="Wklej tutaj pełną treść ogłoszenia..."
    )
    if st.session_state.offer_text:
        st.success(f"✅ Ogłoszenie wczytane ({len(st.session_state.offer_text)} znaków)")


# ── 3. ANALIZA AI ──
elif page == "🔍  Analiza AI":
    st.markdown("## 🔍 Analiza dopasowania AI")

    if not st.session_state.profile:
        st.warning("⚠️ Najpierw uzupełnij profil w zakładce **Profil kandydata**.")
        st.stop()
    if not st.session_state.offer_text.strip():
        st.warning("⚠️ Najpierw wklej ogłoszenie o pracę w zakładce **Profil kandydata**.")
        st.stop()

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        run = st.button("🧠 Uruchom analizę AI", use_container_width=True)
    with col_info:
        st.markdown(f"<span class='tag'>Model: {st.session_state.model}</span>", unsafe_allow_html=True)

    if run:
        with st.spinner(f"🧠 Analizuję z modelem {st.session_state.model}..."):
            try:
                logger.info(f"Starting AI analysis with model {st.session_state.model}")
                from utils.analyzer import analyze_match_ai
                api_keys_dict = {"GROQ_API_KEY": st.session_state.groq_api_key, "GEMINI_API_KEY": st.session_state.gemini_api_key, "DEEPSEEK_API_KEY": st.session_state.deepseek_api_key}
                result = analyze_match_ai(
                    st.session_state.profile,
                    st.session_state.offer_text,
                    model=st.session_state.model,
                    api_keys=api_keys_dict
                )
                st.session_state.analysis = result
            except Exception as e:
                st.error(f"❌ Błąd API: {e}")
                st.info("Sprawdź poprawność klucza API, lub upewnij się, że Ollama jest uruchomiona (`ollama serve`) jeśli używasz modelu lokalnego.")
                st.stop()

    if st.session_state.analysis:
        analysis = st.session_state.analysis

        # Metryki ogólne
        score = analysis.get("ocena_ogolna", 0)
        dopasowanie = analysis.get("dopasowanie", {})
        ok_count   = sum(1 for v in dopasowanie.values() if isinstance(v, dict) and v.get("status") == "✅")
        warn_count = sum(1 for v in dopasowanie.values() if isinstance(v, dict) and v.get("status") == "⚠️")
        bad_count  = sum(1 for v in dopasowanie.values() if isinstance(v, dict) and v.get("status") == "❌")
        total = len(dopasowanie)

        st.markdown("### 📊 Wynik ogólny")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="metric-box"><div class="value">{score}%</div><div class="label">Dopasowanie ogólne</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="metric-box"><div class="value" style="color:#34d399">{ok_count}</div><div class="label">✅ Spełnione</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="metric-box"><div class="value" style="color:#fbbf24">{warn_count}</div><div class="label">⚠️ Częściowe</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="metric-box"><div class="value" style="color:#f87171">{bad_count}</div><div class="label">❌ Brakujące</div></div>""", unsafe_allow_html=True)

        # Progress bar
        st.markdown(f"""
        <div class="progress-wrap">
            <div class="progress-fill" style="width:{score}%"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Umiejętności
        st.markdown("### 🎯 Analiza umiejętności")
        skills_html = ""
        for skill, data in dopasowanie.items():
            if isinstance(data, dict):
                status = data.get("status", "❌")
                comment = data.get("komentarz", "")
                css = "skill-ok" if status == "✅" else ("skill-warn" if status == "⚠️" else "skill-bad")
                skills_html += f'<span class="{css}" title="{comment}">{status} {skill}</span>'
            else:
                css = "skill-ok" if data == "✅" else "skill-bad"
                skills_html += f'<span class="{css}">{data} {skill}</span>'
        st.markdown(skills_html, unsafe_allow_html=True)

        # Szczegółowe komentarze
        with st.expander("📋 Szczegółowe komentarze do umiejętności"):
            for skill, data in dopasowanie.items():
                if isinstance(data, dict) and data.get("komentarz"):
                    st.markdown(f"**{data['status']} {skill}**: {data['komentarz']}")

        st.markdown("---")
        col_a, col_b = st.columns(2)

        with col_a:
            mocne = analysis.get("mocne_strony", [])
            if mocne:
                st.markdown("### 💪 Mocne strony")
                for punkt in mocne:
                    st.markdown(f"✅ {punkt}")

        with col_b:
            braki = analysis.get("braki", [])
            if braki:
                st.markdown("### 📚 Obszary do rozwoju")
                for brak in braki:
                    st.markdown(f"❌ {brak}")

        rekomendacja = analysis.get("rekomendacja", "")
        if rekomendacja:
            st.markdown("---")
            st.markdown("### 💡 Rekomendacja AI")
            st.markdown(f"""<div class="card">{rekomendacja}</div>""", unsafe_allow_html=True)

        slowa = analysis.get("brakujace_slowa_kluczowe", [])
        if slowa:
            st.markdown("### 🔑 Słowa kluczowe do dodania do CV")
            st.markdown(" ".join([f"<span class='tag'>{s}</span>" for s in slowa]), unsafe_allow_html=True)

        st.markdown("---")
        st.success("✅ Analiza gotowa! Przejdź do zakładki **List motywacyjny** aby wygenerować list.")


# ── 4. LIST MOTYWACYJNY ──
elif page == "📄  List motywacyjny":
    st.markdown("## 📄 List motywacyjny")

    if not st.session_state.profile:
        st.warning("⚠️ Najpierw uzupełnij profil w zakładce **Profil kandydata**.")
        st.stop()
    if not st.session_state.offer_text.strip():
        st.warning("⚠️ Najpierw wklej ogłoszenie w zakładce **Profil kandydata**.")
        st.stop()

    col1, col2 = st.columns([2, 1])
    with col1:
        style = st.selectbox(
            "Styl listu",
            ["profesjonalny", "entuzjastyczny", "zwiezly"],
            format_func=lambda x: {
                "profesjonalny": "💼 Profesjonalny",
                "entuzjastyczny": "🔥 Entuzjastyczny",
                "zwiezly": "⚡ Zwięzły"
            }[x]
        )
    with col2:
        st.markdown(f"<br><span class='tag'>Model: {st.session_state.model}</span>", unsafe_allow_html=True)

    extra = st.text_area(
        "Dodatkowe wskazówki (opcjonalnie)",
        placeholder="np. Podkreśl doświadczenie z dużymi zbiorami danych, wspomnij o pracy zdalnej...",
        height=80
    )

    col_gen, col_imp = st.columns(2)
    with col_gen:
        generate = st.button("✍️ Wygeneruj list", use_container_width=True)
    with col_imp:
        improve_btn = st.button("🔄 Ulepsz istniejący list", use_container_width=True,
                                 disabled=not bool(st.session_state.cover_letter))

    if generate:
        with st.spinner("✍️ Generuję list motywacyjny..."):
            try:
                from utils.generator import generate_cover_letter_with_ollama
                api_keys_dict = {"GROQ_API_KEY": st.session_state.groq_api_key, "GEMINI_API_KEY": st.session_state.gemini_api_key, "DEEPSEEK_API_KEY": st.session_state.deepseek_api_key}
                letter = generate_cover_letter_with_ollama(
                    st.session_state.profile,
                    st.session_state.offer_text,
                    model=st.session_state.model,
                    style=style,
                    extra_notes=extra,
                    api_keys=api_keys_dict
                )
                st.session_state.cover_letter = letter
            except Exception as e:
                st.error(f"❌ Błąd API: {e}")
                st.info("Sprawdź poprawność klucza API, lub upewnij się, że Ollama jest uruchomiona i model jest pobrany.")

    if improve_btn and st.session_state.cover_letter:
        feedback = st.text_area("Co poprawić?", placeholder="np. Zrób go krótszym, dodaj więcej o projektach...")
        if st.button("▶️ Zastosuj poprawki"):
            with st.spinner("🔄 Ulepszam list..."):
                try:
                    from utils.generator import improve_cover_letter
                    api_keys_dict = {"GROQ_API_KEY": st.session_state.groq_api_key, "GEMINI_API_KEY": st.session_state.gemini_api_key, "DEEPSEEK_API_KEY": st.session_state.deepseek_api_key}
                    improved = improve_cover_letter(
                        st.session_state.cover_letter,
                        feedback,
                        model=st.session_state.model,
                        api_keys=api_keys_dict
                    )
                    st.session_state.cover_letter = improved
                    st.success("✅ List ulepszony!")
                except Exception as e:
                    st.error(f"❌ Błąd: {e}")

    if st.session_state.cover_letter:
        st.markdown("---")
        st.markdown("### 📄 Gotowy list:")
        edited = st.text_area(
            "Możesz edytować list przed pobraniem:",
            value=st.session_state.cover_letter,
            height=400,
            key="letter_editor"
        )
        if edited != st.session_state.cover_letter:
            st.session_state.cover_letter = edited

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                "📥 Pobierz jako .txt",
                data=st.session_state.cover_letter,
                file_name="list_motywacyjny.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_dl2:
            st.download_button(
                "📋 Pobierz jako .md",
                data=st.session_state.cover_letter,
                file_name="list_motywacyjny.md",
                mime="text/markdown",
                use_container_width=True
            )

        chars = len(st.session_state.cover_letter)
        words = len(st.session_state.cover_letter.split())
        st.caption(f"📊 Długość: {chars} znaków · {words} słów")


# ── 5. JAK TO DZIAŁA ──
elif page == "ℹ️  Jak to działa":
    st.markdown("## ℹ️ Jak to działa")

    st.markdown("""
    <div class="card">
        <h3>🏗️ Architektura projektu</h3>
        <pre style="color:#94a3b8; font-size:0.85rem">
AI-RekrutAgent/
├── app.py                  ← Streamlit UI (ta aplikacja)
├── main.py                 ← Wersja CLI
├── requirements.txt
├── data/
│   ├── profil_kandydata.json
│   └── oferta1.txt
├── utils/
│   ├── analyzer.py         ← Analiza AI + fallback regex
│   ├── generator.py        ← Generowanie listu
│   └── parser.py           ← Wczytywanie plików
└── output/                 ← Wyniki CLI
        </pre>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🔍 Analiza dopasowania</h3>
            <p style="color:#64748b">Model AI analizuje całą ofertę pracy i Twój profil, oceniając każdą umiejętność w kontekście wymagań. Daje ocenę procentową, wskazuje mocne strony i braki, oraz sugeruje słowa kluczowe do CV.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card">
            <h3>✍️ Generowanie listu</h3>
            <p style="color:#64748b">Specjalnie skonstruowany prompt zapewnia naturalny, polski styl listu. Możesz wybrać styl (profesjonalny / entuzjastyczny / zwięzły) i dodać własne wskazówki. List można też ulepszyć po wygenerowaniu.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Wymagania")
    st.markdown("""
    Wersja V2 wspiera potężne i **darmowe API Chmurowe** (Groq, Gemini, DeepSeek). Wystarczy podać klucz API w bocznym panelu aplikacji!
    
    Jeśli wolisz działać w 100% lokalnie i prywatnie (offline):
    1. Zainstaluj **Ollama**: [ollama.com](https://ollama.com)
    2. Pobierz wybrany model: `ollama pull llama3.2`
    3. Uruchom serwer Ollama w tle: `ollama serve`
    """)

    st.markdown("### 🧠 Dostępne modele (Chmura + Ollama)")
    st.markdown("""
    Aplikacja centralnie zarządza listą modeli przez plik `config.yaml`.
    
    | Dostawca | Przykładowe Modele | Wymagania |
    |---|---|---|
    | **Groq** | `llama-3.3-70b-versatile`, `llama-3.1-8b-instant` | Darmowy klucz API |
    | **Google Gemini** | `gemini-2.5-flash`, `gemini-2.5-pro` | Darmowy klucz API |
    | **DeepSeek** | `deepseek-chat`, `deepseek-coder` | Klucz API |
    | **Ollama** (Lokalnie)| `llama3.2`, `mistral`, `gemma2` | Pobrany model na dysku |
    """)
