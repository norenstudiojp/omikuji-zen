import streamlit as st
import random
import google.generativeai as genai
import streamlit.components.v1 as components

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Noren Labs - Zen Omikuji", page_icon="⛩️", layout="centered")

# 【重要】Google AdSense 審査用コードの埋め込み
# あなたのAdSense管理画面で発行された「ca-pub-XXXXXXXXXXXXXXXX」をここに反映させてください
adsense_id = "ca-pub-8982760985669430" # 後で書き換えてください
adsense_script = f"""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={adsense_id}"
     crossorigin="anonymous"></script>
"""
# 審査用コードをヘッドに認識させるために不可視のコンポーネントとして挿入
components.html(adsense_script, height=0)

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
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: INFORMATION & POLICY ---
with st.sidebar:
    st.title("⛩️ Noren Labs")
    st.write("Crafting digital Zen experiences.")
    
    with st.expander("Privacy Policy"):
        st.markdown("""
        **1. Data Collection**
        We use Google Generative AI (Gemini) to generate wisdom. No personal identifiers are stored.
        
        **2. Advertisements**
        We use Google AdSense. Google and third-party vendors use cookies to serve ads based on your prior visits. You can opt out of personalized advertising by visiting Google Ads Settings.
        
        **3. Analytics**
        We use basic metrics to improve user experience.
        
        *Copyright © 2026 Noren Labs*
        """)

# --- LOGIC ---
def get_zen_wisdom(fortune_level, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Provide a one-sentence Zen wisdom in English for someone who drew '{fortune_level}' in a Japanese Omikuji. Keep it profound, minimalist, and global."
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "Silence is also an answer. (Check API Key)"

# --- UI ---
st.title("⛩️ Noren Labs")
st.subheader("Zen Omikuji")
st.write("Embrace the void. Discover your path.")

# Draw Fortune Logic
if st.button("Draw Fortune"):
    fortunes = {
        "Great Blessing (Dai-Kichi)": "The universe aligns with your intent.",
        "Middle Blessing (Chu-Kichi)": "Steady progress leads to the mountain top.",
        "Small Blessing (Sho-Kichi)": "A single spark can start a fire.",
        "Blessing (Kichi)": "You are where you need to be.",
        "Terrible Luck (Kyo)": "Resistance is the greatest teacher."
    }
    
    level = random.choice(list(fortunes.keys()))
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    
    with st.spinner("Seeking wisdom..."):
        wisdom = get_zen_wisdom(level, api_key) if api_key else "Please set API Key."

    st.markdown(f"""
        <div class="fortune-box">
            <h2 style="color: #E60012;">{level}</h2>
            <p><strong>Insight:</strong> {fortunes[level]}</p>
            <div class="zen-wisdom">“{wisdom}”</div>
        </div>
        """, unsafe_allow_html=True)

    share_text = f"Noren Labs - Zen Omikuji\nFortune: {level}\nWisdom: {wisdom}\n#ZenOmikuji #NorenLabs"
    st.text_area("Share your Zen moment:", value=share_text, height=100)

# --- AD SPACE ---
# 審査通過後、ここに自動広告が配信されるか、個別にユニットを配置します
st.markdown("---")
st.caption("ADVERTISEMENT")
components.html(adsense_script, height=100)
