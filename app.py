import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 15: O Pitilidan", page_icon="🏫", layout="centered")

# --- CSS 美化 (學術藍) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #E8EAF6 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #3F51B5;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #303F9F; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #E8EAF6;
        border-left: 5px solid #5C6BC0;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #C5CAE9; color: #1A237E; border: 2px solid #3F51B5; padding: 12px;
    }
    .stButton>button:hover { background-color: #9FA8DA; border-color: #303F9F; }
    .stProgress > div > div > div > div { background-color: #3F51B5; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 15) ---
vocab_data = [
    {"amis": "Pitilidan", "chi": "學校", "icon": "🏫", "source": "Row 318/2362"},
    {"amis": "Singsi", "chi": "老師", "icon": "👩‍🏫", "source": "Row 10"},
    {"amis": "Mitiliday", "chi": "學生", "icon": "🎒", "source": "Row 314"},
    {"amis": "Codad", "chi": "書 / 書本", "icon": "📖", "source": "Row 7460"},
    {"amis": "Mitilid", "chi": "寫字 / 讀書", "icon": "✍️", "source": "Row 473"},
    {"amis": "Micodad", "chi": "讀書 / 閱讀", "icon": "📚", "source": "Row 2362"},
    {"amis": "Kapot", "chi": "同學 / 同伴", "icon": "👫", "source": "Row 20"},
    {"amis": "Widang", "chi": "朋友", "icon": "🤝", "source": "Row 7"},
    {"amis": "Misa'icel", "chi": "努力 / 加油", "icon": "💪", "source": "Row 473"},
    {"amis": "Minokay", "chi": "回家", "icon": "🏠", "source": "Row 497"},
]

sentences = [
    {"amis": "O singsi kora a kaying.", "chi": "那位小姐是老師。", "icon": "👩‍🏫", "source": "Row 10"},
    {"amis": "Misa'icel kako a mitilid.", "chi": "我很努力讀書。", "icon": "💪", "source": "Row 473"},
    {"amis": "Tayra kami i pitilidan.", "chi": "我們去學校。", "icon": "🏫", "source": "Row 485 (Adapted)"},
    {"amis": "Micodad ko mitiliday.", "chi": "學生在讀書。", "icon": "📖", "source": "Grammar"},
    {"amis": "Nani pitilidan a minokay.", "chi": "從學校回家。", "icon": "🚶", "source": "Row 497"},
]

# --- 3. 隨機題庫 ---
quiz_pool = [
    {
        "q": "O singsi kora a kaying.",
        "audio": "O singsi kora a kaying",
        "options": ["那位小姐是老師", "那位小姐是學生", "那位小姐是朋友"],
        "ans": "那位小姐是老師",
        "hint": "Singsi 是老師"
    },
    {
        "q": "Misa'icel kako a mitilid.",
        "audio": "Misa'icel kako a mitilid",
        "options": ["我很努力讀書", "我很努力吃飯", "我很努力睡覺"],
        "ans": "我很努力讀書",
        "hint": "Misa'icel (努力) + Mitilid (讀書/寫字)"
    },
    {
        "q": "Tayra kami i pitilidan.",
        "audio": "Tayra kami i pitilidan",
        "options": ["我們去學校", "我們去市場", "我們去台東"],
        "ans": "我們去學校",
        "hint": "Pitilidan 是學校"
    },
    {
        "q": "單字測驗：Codad",
        "audio": "Codad",
        "options": ["書本", "筆", "桌子"],
        "ans": "書本",
        "hint": "讀書是 Micodad"
    },
    {
        "q": "單字測驗：Kapot",
        "audio": "Kapot",
        "options": ["同學 / 同伴", "老師", "家長"],
        "ans": "同學 / 同伴",
        "hint": "一起學習的人"
    },
    {
        "q": "Nani pitilidan a minokay.",
        "audio": "Nani pitilidan a minokay",
        "options": ["從學校回家", "去學校讀書", "在學校玩耍"],
        "ans": "從學校回家",
        "hint": "Minokay 是回家"
    },
    {
        "q": "「學生」的阿美語怎麼說？",
        "audio": None,
        "options": ["Mitiliday", "Singsi", "Widang"],
        "ans": "Mitiliday",
        "hint": "正在讀書/寫字的人"
    }
]

# --- 4. 狀態初始化 ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.quiz_questions = random.sample(quiz_pool, 3)
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #303F9F;'>Unit 15: O Pitilidan</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>學校生活 (School Life)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #1A237E;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 3**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #C5CAE9; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #1A237E;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會學校生活的對話了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_questions = random.sample(quiz_pool, 3)
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            safe_rerun()
