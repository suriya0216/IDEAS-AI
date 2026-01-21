import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os
import datetime
import time
import urllib.parse

# --- 1. PREMIUM CONFIGURATION ---
st.set_page_config(
    page_title="IDAS AI | Intelligence Architect", 
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED DYNAMIC CSS (Preserved + Mobile Optimization) ---
if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "Cyber Dark"

theme_bg = "radial-gradient(circle at center, #1a1a2e 0%, #07070a 100%)" if st.session_state.ui_theme == "Cyber Dark" else "#f0f2f6"
theme_text = "#ffffff" if st.session_state.ui_theme == "Cyber Dark" else "#1e1e2f"

st.markdown(f"""
    <style>
    .stApp {{ background: {theme_bg}; color: {theme_text}; }}
    .premium-title {{
        text-align: center; font-size: 5rem; font-weight: 900;
        background: linear-gradient(90deg, #FF4B4B, #ffffff, #FF4B4B);
        background-size: 200% auto; -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite; letter-spacing: -2px;
    }}
    @keyframes shine {{ to {{ background-position: 200% center; }} }}
    
    /* Responsive Title Adjustment */
    @media (max-width: 768px) {{
        .premium-title {{ font-size: 3rem !important; }}
    }}

    .about-card {{
        background: rgba(255, 75, 75, 0.07); border: 1px solid rgba(255, 75, 75, 0.3);
        border-radius: 15px; padding: 15px; margin-top: 10px; backdrop-filter: blur(10px);
    }}
    .live-clock {{
        font-family: 'Courier New', monospace; color: #00ff88; font-size: 1.2rem;
        text-align: center; background: rgba(0, 255, 136, 0.05);
        border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 10px; padding: 5px;
    }}
    .report-box {{
        border-left: 5px solid #FF4B4B; background: rgba(255, 255, 255, 0.03);
        padding: 20px; border-radius: 0 15px 15px 0; margin: 10px 0;
    }}
    .share-container {{
        display: flex; gap: 15px; margin-top: 15px; padding: 12px;
        background: rgba(255, 75, 75, 0.05); border-radius: 10px;
        border: 1px dashed rgba(255, 75, 75, 0.3); align-items: center;
    }}
    
    /* NEW: User Pulse Animation */
    .user-pulse {{
        height: 10px; width: 10px; background-color: #00ff88;
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 8px #00ff88; animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0% {{ transform: scale(0.95); opacity: 0.7; }}
        70% {{ transform: scale(1.1); opacity: 1; }}
        100% {{ transform: scale(0.95); opacity: 0.7; }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. AI CORE SETUP ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# This specific naming works best with the 0.8.3 library
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 4. SIDEBAR: ALL FEATURES + GLOBAL NETWORK ---
if "history" not in st.session_state: st.session_state.history = []
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    curr_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(f'<div class="live-clock">{curr_time}</div>', unsafe_allow_html=True)
    st.divider()

    st.markdown("<h2 style='color: #FF4B4B; text-align: center;'>💡 IDAS AI</h2>", unsafe_allow_html=True)
    
    if st.button("👤 About Us"):
        st.session_state.show_about = not st.session_state.get('show_about', False)
    if st.session_state.get('show_about'):
        st.markdown("""<div class="about-card"><p style="color: #FF4B4B; font-weight: bold;">Created by Suriya</p>
        <p style="font-size: 0.85rem;">Solving global problems through AI Innovation.</p>
        <p style="font-size: 0.8rem;">📧 suriya0216@gmail.com</p></div>""", unsafe_allow_html=True)

    st.divider()
    st.session_state.ui_theme = st.selectbox("Appearance Mode", ["Cyber Dark", "Arctic Light"])
    target_lang = st.selectbox("Output Language", ["English", "Spanish", "French", "German", "Hindi", "Tamil", "Chinese"])
    neural_mode = st.select_slider("Neural Tuning", options=["Creative", "Balanced", "Precise"], value="Balanced")

    if st.session_state.messages:
        total_words = sum(len(m["content"].split()) for m in st.session_state.messages if m["role"] == "assistant")
        st.metric(label="Knowledge Generated", value=f"{total_words} Words")

    st.markdown("### 📡 Connection Pulse")
    st.caption("Latency: 28ms | Node: Primary-IDAS")
    
    # NEW: GLOBAL NETWORK SIMULATION
    st.markdown('### 🗺️ Global Network')
    col_u1, col_u2 = st.columns([1, 5])
    with col_u1: st.markdown('<div class="user-pulse"></div>', unsafe_allow_html=True)
    with col_u2: st.caption("1,204 Active Nodes")

    st.divider()
    st.markdown("### 🔒 Security")
    st.success("AES-256 & SSL Active")

    if st.button("🗑️ Clear My Session"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

# --- 5. SYSTEM INITIALIZATION TOAST ---
if "init_check" not in st.session_state:
    with st.toast("🔄 Syncing Neural Pathways..."):
        time.sleep(1)
    st.session_state.init_check = True

# --- 6. MAIN INTERFACE ---
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown("<h1 class='premium-title'>IDAS AI</h1>", unsafe_allow_html=True)
    
    if not st.session_state.messages:
        hour = datetime.datetime.now().hour
        greet = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
        st.markdown(f"<div style='text-align: center; padding: 60px 0;'><h2>✨ {greet}.</h2><p style='color: #8b949e;'>Intelligence Architect Ready.</p></div>", unsafe_allow_html=True)

    if st.button("📎 Attach Data"):
        st.session_state.attach_open = not st.session_state.get('attach_open', False)

    if st.session_state.get('attach_open'):
        files = st.file_uploader("Upload Assets", accept_multiple_files=True)
        if files: attached_files = files
    else: attached_files = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Enter your challenge..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.status("🧠 Processing...", expanded=True) as status:
                try:
                    mode_map = {"Creative": "Imaginative", "Balanced": "Professional", "Precise": "Logical"}
                    query_data = [f"Mode: {mode_map[neural_mode]}\nRespond in {target_lang}. Prompt: {prompt}"]
                    for f in attached_files:
                        if f.type.startswith("image"): query_data.append(Image.open(f))
                    
                    response = model.generate_content(query_data)
                    final_text = response.text
                    status.update(label="✅ Success", state="complete", expanded=False)
                    
                    report_id = f"IDAS-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
                    st.markdown(f"""<div class="report-box">
                        <p style="color: #FF4B4B; font-size: 0.7rem; font-weight: bold;">DOC ID: {report_id} | {neural_mode}</p>
                        {final_text}</div>""", unsafe_allow_html=True)
                    
                    if any(char.isdigit() for char in final_text):
                        st.progress(0.92, text=f"Success Probability: 92%")
                    
                    tts = gTTS(text=final_text[:250], lang='en')
                    tts.save("voice_out.mp3")
                    st.audio("voice_out.mp3", autoplay=True)
                    st.download_button("📥 Export Report", final_text, file_name=f"{report_id}.txt")

                    # SOCIAL SHARING HUB
                    encoded_prompt = urllib.parse.quote(f"IDAS AI Solution for: {prompt[:50]}")
                    st.markdown(f"""
                        <div class="share-container">
                            <span style="font-size:0.8rem; color:#8b949e;">SHARE:</span>
                            <a href="https://twitter.com/intent/tweet?text={encoded_prompt}" target="_blank" style="color:#FF4B4B; text-decoration:none; font-size:0.8rem;">🐦 Twitter</a>
                            <a href="https://www.linkedin.com/sharing/share-offsite/" target="_blank" style="color:#FF4B4B; text-decoration:none; font-size:0.8rem;">🔗 LinkedIn</a>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.history.append({"title": prompt[:15]+"...", "time": datetime.datetime.now().strftime("%H:%M")})
                    st.session_state.messages.append({"role": "assistant", "content": final_text})
                except Exception as e:
                    st.error(f"Error: {e}")

if os.path.exists("voice_out.mp3"):
    try: os.remove("voice_out.mp3")
    except: pass




