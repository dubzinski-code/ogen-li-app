import streamlit as st
import pandas as pd

st.set_page_config(page_title="עוגן לי", layout="wide")

st.title("עוגן לי")
st.caption("כלי מבוסס נתוני עוגן לתכנון כיתתי ואישי")

uploaded_file = st.file_uploader(
    "העלאת קובץ עוגן (Excel)",
    type=["xlsx"]
)

tabs = st.tabs([
    "תמונת מצב כיתתית",
    "תוכנית עבודה מרובדת",
    "תוכנית התערבות אישית",
    "המלצות גפ\"ן"
])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    with tabs[0]:
        st.header("תמונת מצב כיתתית")
        st.dataframe(df.head())

        st.subheader("התפלגות נתונים")
        st.bar_chart(df.select_dtypes(include="number"))

    with tabs[1]:
        st.header("תוכנית עבודה מרובדת")
        st.info("כאן יוצגו מענים לפי MTSS – אוניברסלי / קבוצתי / אינטנסיבי")

    with tabs[2]:
        st.header("תוכנית התערבות אישית")
        student = st.selectbox("בחרי תלמיד", df.iloc[:, 0].unique())
        st.write("תוכנית עבור:", student)

    with tabs[3]:
        st.header("המלצות גפ\"ן")
        st.info("כיוונים פדגוגיים כלליים (ללא שמות תוכניות)")

else:
    st.warning("יש להעלות קובץ עוגן כדי להתחיל")
