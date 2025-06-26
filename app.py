
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
import platform

# Pretendard 폰트 설정
matplotlib.rc('font', family='Malgun Gothic')  # Pretendard 대체
matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="조직문화 진단 통합 대시보드", layout="wide")

st.title("🏢 조직문화 진단 통합 대시보드")
uploaded_file = st.file_uploader("📎 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    menu = st.sidebar.radio("메뉴 선택", ["📊 정량 진단 분석", "☁️ 정성 워드클라우드"])

    if menu == "📊 정량 진단 분석":
        st.subheader("📊 정량 데이터 분석")

        # 유형별 문항 그룹 정의
        question_groups = {
            "회사에 대한 긍정인식_미래 비전 신뢰": [col for col in df.columns if col.startswith("회사에 대한 긍정인식_미래 비전 신뢰")],
            "조직 커뮤니케이션_업무 고충 소통": [col for col in df.columns if col.startswith("조직 커뮤니케이션_업무 고충 소통")],
            "업무_의사결정 참여 기회": [col for col in df.columns if col.startswith("업무_의사결정 참여 기회")],
            "직속상사 리더십_상사에 대한 신뢰": [col for col in df.columns if col.startswith("직속상사 리더십_상사에 대한 신뢰")],
            "동료와의 관계_우호적 동료관계": [col for col in df.columns if col.startswith("동료와의 관계_우호적 동료관계")],
            "성장 기회_경력개발 기회": [col for col in df.columns if col.startswith("성장 기회_경력개발 기회")],
            "인정과 보상_비금전적 보상": [col for col in df.columns if col.startswith("인정과 보상_비금전적 보상")],
            "심리적 안전감_신뢰관계": [col for col in df.columns if col.startswith("심리적 안전감_신뢰관계")]
        }

        for category, cols in question_groups.items():
            st.markdown(f"### 🔹 {category}")
            scores = df[cols].mean(axis=1)
            avg = round(scores.mean(), 2)
            st.write(f"📌 평균 점수: **{avg}점**")

            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.hist(scores, bins=7, range=(1, 7), edgecolor='black')
            ax.set_xlabel("평균 점수")
            ax.set_ylabel("응답자 수")
            ax.set_title(f"{category} 점수 분포")
            st.pyplot(fig)

    elif menu == "☁️ 정성 워드클라우드":
        st.subheader("☁️ 정성 응답 워드클라우드")
        subjective_questions = [col for col in df.columns if col.startswith("주관식")]
        selected_q = st.selectbox("문항 선택", subjective_questions)

        if selected_q:
            text_data = " ".join(df[selected_q].dropna().astype(str))
            if text_data.strip() == "":
                st.warning("응답 내용이 없습니다.")
            else:
                wordcloud = WordCloud(
                    font_path="C:/Windows/Fonts/malgun.ttf",
                    background_color="white",
                    width=800,
                    height=400
                ).generate(text_data)

                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
