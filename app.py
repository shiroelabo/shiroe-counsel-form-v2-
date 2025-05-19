
import streamlit as st
import requests
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="SHIROE LABO カウンセリングシート", layout="centered")

# ロゴとタイトル
st.image("logo.png", width=300)
st.markdown("<h2 style='text-align: center;'>カウンセリングシート</h2>", unsafe_allow_html=True)

def lookup_address(zipcode):
    if len(zipcode) == 7 and zipcode.isdigit():
        response = requests.get(f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={zipcode}")
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                result = data["results"][0]
                return f"{result['address1']}{result['address2']}{result['address3']}"
    return ""

with st.form(key="counseling_form"):
    st.subheader("■ 基本情報")

    col1, col2 = st.columns(2)
    with col1:
        last_name = st.text_input("姓")
    with col2:
        first_name = st.text_input("名")

    col3, col4 = st.columns(2)
    with col3:
        last_name_kana = st.text_input("セイ（カタカナ）")
    with col4:
        first_name_kana = st.text_input("メイ（カタカナ）")

    gender = st.radio("性別", ["女性", "男性", "その他"])

    st.markdown("### 生年月日")
    col_year, col_month, col_day = st.columns(3)
    with col_year:
        birth_year = st.selectbox("年", list(range(1950, datetime.today().year + 1)), index=30)
    with col_month:
        birth_month = st.selectbox("月", list(range(1, 13)))
    with col_day:
        birth_day = st.selectbox("日", list(range(1, 32)))

    try:
        birth_date = datetime(birth_year, birth_month, birth_day)
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        st.markdown(f"**年齢：{age}歳**")
    except:
        st.warning("正しい生年月日を選択してください。")

    zipcode = st.text_input("郵便番号（ハイフンなし）")
    address_default = lookup_address(zipcode)
    address = st.text_input("住所", value=address_default)
    phone = st.text_input("電話番号")

    st.subheader("■ 印象・目的について")

    st.markdown("**なりたい印象（複数選択可）**")
    impressions = []
    for opt in ["清潔感がある", "若々しく見える", "自信に溢れて信頼感がある", "垢抜けている",
                "健康的な印象"]:
        if st.checkbox(opt, key=f"imp_{opt}"):
            impressions.append(opt)

    st.markdown("**ご来店の目的・背景（複数選択可）**")
    motives = []
    for opt in ["仕事・面接に向けて", "恋愛・婚活", "大切な予定のため", "自分磨き", "SNSなどで気になった"]:
        if st.checkbox(opt, key=f"mot_{opt}"):
            motives.append(opt)

    st.markdown("**現在の歯の状態（複数選択可）**")
    states = []
    for opt in ["少し黄ばみが気になる", "人と比べて気になる", "鏡や写真で気になる", "笑う時に気になる"]:
        if st.checkbox(opt, key=f"state_{opt}"):
            states.append(opt)

    st.markdown("**これまでのホワイトニング経験（複数選択可）**")
    histories = []
    for opt in ["初めて", "歯科ホワイトニング", "セルフホワイトニング（サロン）",
                "ホームホワイトニング（歯科キット）", "市販ホワイトニング（歯磨き粉・シート等）"]:
        if st.checkbox(opt, key=f"hist_{opt}"):
            histories.append(opt)

    st.markdown("**理想の通い方（複数選択可）**")
    styles = []
    for opt in ["週1〜2回で集中して通いたい", "月2回くらいのペースで通いたい",
                "不定期でも気になったときに通いたい", "一度白くしたら、その後は維持として通いたい"]:
        if st.checkbox(opt, key=f"style_{opt}"):
            styles.append(opt)

    st.markdown("**その他、気になること・不安など**")
    concerns = st.text_area("")

    st.subheader("■ 同意事項")
    with st.expander("▼ ご確認ください（クリックで表示）", expanded=False):
        st.markdown("""
●施術後の仕上がりには個人差があります。  
●医療機関で治療中の方は医師へ確認の上で施術を行ってください。  
●施術後の返金には応じかねます。
        """)

    agree = st.checkbox("上記注意事項をすべて確認し、同意しました。")
    date = datetime.today().strftime("%Y-%m-%d")
    st.markdown(f"**同意日：{date}**")

    st.subheader("■ 署名欄")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#ffffff",
        height=150,
        width=400,
        drawing_mode="freedraw",
        key="canvas"
    )

    if agree:
        submit_btn = st.form_submit_button("送信", type="primary")
    else:
        submit_btn = st.form_submit_button("送信")

    if submit_btn and agree:
        st.success("回答を受け付けました（※保存処理は後で接続）")
        if canvas_result.image_data is not None:
            st.image(canvas_result.image_data, caption="署名画像（プレビュー）")
        else:
            st.warning("署名が見つかりません。もう一度お試しください。")
    elif submit_btn and not agree:
        st.error("注意事項への同意が必要です。")
