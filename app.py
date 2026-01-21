import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os

# --- CONFIGURATION ---
genai.configure(api_key="AIzaSyDKvrTZc55pPtaY-4CRxTu7cY7xcCCOT4I")
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="IDAS AI", page_icon="💡")
st.title("💡 IDAS AI: Advanced Solver")

# --- INITIALIZE MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: IMAGE UPLOAD ---
with st.sidebar:
    st.header("📸 Visual Input")
    uploaded_file = st.file_uploader("Upload a photo of the problem", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), caption="Uploaded Image")

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("How can I help you solve a problem today?"):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("IDAS AI is thinking..."):
            try:
                # Build context (including image if exists)
                content = [prompt]
                if uploaded_file:
                    content.append(Image.open(uploaded_file))
                
                response = model.generate_content(content)
                full_response = response.text
                st.markdown(full_response)
                
                # 3. VOICE OUTPUT
                tts = gTTS(text=full_response[:300], lang='en') # Speak first 300 chars
                tts.save("response.mp3")
                st.audio("response.mp3", format="audio/mp3", autoplay=True)
                
                # Save to memory
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {e}")

# Cleanup old audio file
if os.path.exists("response.mp3"):
    try: os.remove("response.mp3")
    except: pass
