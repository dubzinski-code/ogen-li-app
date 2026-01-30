import streamlit as st
import pandas as pd

st.set_page_config(page_title="עוגן לי", layout="wide")

st.title("עוגן לי")
st.caption("כלי מבוסס נתוני עוגן לתכנון כיתתי ואישי")

uploaded_file = st.file_uploader(
    "העלאת קובץ עוגן (Excel)",
    type=["xlsx", "xls"]
)

tabs = st.tabs([
    "תמונת מצב כיתתית",
    "תוכנית עבודה מרובדת",
    "תוכנית התערבות אישית",
    "המלצות גפ\"ן"
])

    if uploaded_file.name.endswith(".xls"):
    df = pd.read_excel(uploaded_file, engine="xlrd")
else:
    df = pd.read_excel(uploaded_file)

    # ניקוי נתונים בסיסי
    df = df.dropna(subset=["תלמידי כיתה"])

    with tabs[0]:
        st.header("תמונת מצב כיתתית")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="מספר תלמידים בכיתה",
                value=df["תלמידי כיתה"].nunique()
            )

        with col2:
            st.metric(
                label="מספר רשומות בקובץ",
                value=len(df)
            )

        st.subheader("רשימת תלמידים")
        st.dataframe(
            df[["תלמידי כיתה"]].drop_duplicates().reset_index(drop=True),
            use_container_width=True
        )

        st.subheader("התפלגות נתונים מספריים")
        numeric_cols = df.select_dtypes(include="number")
        if not numeric_cols.empty:
            st.bar_chart(numeric_cols)
        else:
            st.info("לא נמצאו עמודות מספריות להצגת גרף.")

    with tabs[1]:
        st.header("תוכנית עבודה מרובדת")
        st.info("בשלב הבא יוצגו מענים לפי MTSS (אוניברסלי / קבוצתי / אינטנסיבי)")

    with tabs[2]:
        st.header("תוכנית התערבות אישית")

        student = st.selectbox(
            "בחרי תלמיד",
            sorted(df["תלמידי כיתה"].unique())
        )

        st.subheader(f"תוכנית אישית עבור: {student}")
        st.write("כאן יוצגו מוקדי קושי, חוזקות ומענים אישיים.")

    with tabs[3]:
        st.header("המלצות גפ\"ן")
        st.info(
            "כיוונים פדגוגיים כלליים למענה כיתתי או קבוצתי "
            "(ללא ציון שמות תוכניות או ספקים)."
        )

else:
    st.warning("יש להעלות קובץ עוגן כדי להתחיל")
