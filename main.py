import streamlit as st
import random
import google.generativeai as genai

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Noren Labs - Zen Omikuji", page_icon="⛩️", layout="centered")

# Japanese Minimalism CSS
st.markdown("""
    <style>
    .main { background-color: #F5F5F5; color: #1A1A1A; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .stButton>button {
        background-color: #E60012; color: white; border-radius: 0px; border: none;
        padding: 0.5rem 2rem; font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1A1A1A; color: #F5F5F5; }
    .fortune-box {
        border-left: 5px solid #E60012; padding: 20px; background: white;
        margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .zen-wisdom { font-style: italic; color: #555; margin-top: 10px; }
    .ad-placeholder { color: #CCC; text-align: center; font-size: 10px; margin-top: 50px; border-top: 1px solid #EEE; padding-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: PRIVACY POLICY ---
with st.sidebar:
    st.title("About Noren Labs")
    if st.checkbox("Privacy Policy"):
        st.markdown("""
        ### Privacy Policy
        **1. Data Collection**
        We use Google Generative AI (Gemini) to generate wisdom. No personal identifiers are stored on our servers.
        
        **2. Advertisements**
        We use Google AdMob/AdSense. These third-party vendors use cookies to serve ads based on your prior visits.
        
        **3. Analytics**
        We may use basic analytics to improve user experience.
        
        *Noren Labs - Zen Omikuji*
        """)

# --- LOGIC ---
def get_zen_wisdom(fortune_level, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Provide a one-sentence Zen wisdom in English for someone who drew '{fortune_level}' in a Japanese Omikuji. Keep it profound, minimalist, and global."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Silence is also an answer. (API Key Error or Limitation)"

# --- UI ---
st.title("⛩️ Noren Labs")
st.subheader("Zen Omikuji")
st.write("Embrace the void. Discover your path.")

if st.button("Draw Fortune"):
    fortunes = {
        "Great Blessing (Dai-Kichi)": "The universe aligns with your intent.",
        "Middle Blessing (Chu-Kichi)": "Steady progress leads to the mountain top.",
        "Small Blessing (Sho-Kichi)": "A single spark can start a fire.",
        "Blessing (Kichi)": "You are where you need to be.",
        "Terrible Luck (Kyo)": "Resistance is the greatest teacher."
    }
    
    level = random.choice(list(fortunes.keys()))
    
    # API Key from Secrets
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    
    with st.spinner("Seeking wisdom..."):
        wisdom = get_zen_wisdom(level, api_key) if api_key else "Wisdom is hidden until the key is set."

    # Display Result
    st.markdown(f"""
        <div class="fortune-box">
            <h2 style="color: #E60012;">{level}</h2>
            <p><strong>Insight:</strong> {fortunes[level]}</p>
            <div class="zen-wisdom">“{wisdom}”</div>
        </div>
        """, unsafe_allow_html=True)

    # Shareability
    share_text = f"Noren Labs - Zen Omikuji\nFortune: {level}\nWisdom: {wisdom}\n#ZenOmikuji #NorenLabs"
    st.text_area("Copy to share your Zen moment:", value=share_text, height=100)

# --- AD REPLACEMENT ---
import streamlit.components.v1 as components

# AdMob / AdSense HTML Code
# 注: 審査に通るまではプレースホルダーが表示されます
ad_code = """
<div style="text-align:center; margin-top:20px;">
    <p style="color:#CCC; font-size:10px;">ADVERTISEMENT</p>
    <div style="width:100%; height:90px; background:#EEE; display:flex; align-items:center; justify-content:center;">
        <span style="color:#999;">Ad Space</span>
    </div>
</div>
"""
components.html(ad_code, height=150)
