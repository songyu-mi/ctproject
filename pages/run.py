import streamlit as st
from soynlp.tokenizer import RegexTokenizer
import random
import time

# ---------------- 초기 설정 ---------------- #
st.set_page_config(layout='centered', page_title='(AI 적용 CT문제) 문장을 형태소로 분석하기')
tokenizer = RegexTokenizer()

REAL_KEYWORDS = ["비", "많이", "내리", "학생", "책", "읽", "고양이", "방", "자", "나", "학교", "가", "봄바람", "부드럽게", "분"]
FORMAL_KEYWORDS = ["가", "을", "이", "에", "에서", "는다", "었다", "다"]

sentences = [
    "비가 많이 내린다.",
    "학생이 책을 읽었다.",
    "고양이가 방에서 잔다.",
    "나는 학교에 간다.",
    "봄바람이 부드럽게 분다."
]

def analyze_sentence(sentence):
    tokens = tokenizer.tokenize(sentence)
    cards = []
    for token in tokens:
        if any(r in token for r in REAL_KEYWORDS):
            cards.append("🔵")
        elif any(f in token for f in FORMAL_KEYWORDS):
            cards.append("🔴")
        else:
            cards.append("🔵")
    return tokens, cards

def countdown(t):
    timer_placeholder = st.empty()
    for sec in range(t, 0, -1):
        timer_placeholder.markdown(f"⏱ 남은 시간: **{sec}** 초")
        time.sleep(1)
    st.session_state.timeup = True
    timer_placeholder.markdown("⏰ 시간이 종료되었습니다! 다시 도전하세요.")

st.title("타이틀: (AI 적용 CT문제) 문장을 형태소로 분석하기")
st.subheader("대상 및 교과: 중학교(국어)")

with st.expander("📘 지문 보기"):
    st.write("""
    비버는 문장을 말의 가장 작은 단위(형태소)로 나눈 후, 
    각 단위의 역할에 따라 두 가지 색깔 카드로 구분하는 프로그램을 만들었습니다.

    - 🔵 파란 카드: 구체적인 대상, 동작, 상태 등 의미를 가진 말의 가장 작은 단위  
    - 🔴 빨간 카드: 말과 말 사이의 관계를 표시하거나 문장의 문법적 기능을 수행하는 말의 가장 작은 단위
    """)

if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)
if "selected_cards" not in st.session_state:
    st.session_state.selected_cards = []
if "timeup" not in st.session_state:
    st.session_state.timeup = False

st.markdown("### 📌 문제")
with st.container():
    st.info("위의 기준에 따라 문장을 형태소로 분석하고, 기능에 따라 색깔 카드를 올바르게 배열하세요.")
    st.markdown(f"#### 제시 문장: **{st.session_state.sentence}**")

time_options = {"30초": 30, "1분": 60, "1분 30초": 90, "2분": 120}
selected_time = st.selectbox("시간을 선택하세요:", list(time_options.keys()))

if st.button("문제 풀기 시작"):
    st.session_state.timeup = False
    countdown(time_options[selected_time])

st.markdown("#### 🎨 카드 선택")
cols = st.columns(4)
with cols[0]:
    if st.button("🔵 파란 카드"):
        st.session_state.selected_cards.append("🔵")
with cols[1]:
    if st.button("🔴 빨간 카드"):
        st.session_state.selected_cards.append("🔴")
with cols[2]:
    if st.button("↩️ 되돌리기"):
        if st.session_state.selected_cards:
            st.session_state.selected_cards.pop()
with cols[3]:
    if st.button("🛑 스톱"):
        tokens, correct_cards = analyze_sentence(st.session_state.sentence)
        user_answer = st.session_state.selected_cards
        if user_answer == correct_cards:
            st.success("🎉 정답입니다!")
            if st.button("다른 문제 도전하기 ▶"):
                st.session_state.sentence = random.choice(sentences)
                st.session_state.selected_cards = []
                st.experimental_rerun()
        else:
            st.error(f"❌ 오답입니다. 정답은: {' '.join(correct_cards)}")
            if st.button("다시 도전 ▶"):
                st.session_state.selected_cards = []
                st.experimental_rerun()

st.markdown("#### 현재 선택한 카드:")
st.write(" ".join(st.session_state.selected_cards))

if st.session_state.timeup:
    st.warning("⏰ 시간이 초과되었습니다! '문제 풀기 시작'을 눌러 다시 도전하세요.")
