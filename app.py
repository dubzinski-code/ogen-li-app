import streamlit as st
import pandas as pd
import re

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


def extract_meaningful_text(cell_text, keywords):
    """
    מחלץ את הטקסט המשמעותי (סוג קושי / חוזקה)
    מתוך תא שמכיל גם דירוג וגם תיאור.
    """
    if pd.isna(cell_text):
        return None

    text = str(cell_text).strip()

    # פיצול לפי ירידת שורה
    parts = re.split(r'\n|–|-|;|:', text)

    # מסיר מילות דירוג
    cleaned = [
        p.strip()
        for p in parts
        if p.strip() and p.strip() not in keywords
    ]

    return cleaned[0] if cleaned else None


if uploaded_file is not None:
    if uploaded_file.name.endswith(".xls"):
        df = pd.read_excel(uploaded_file, engine="xlrd")
    else:
        df = pd.read_excel(uploaded_file)

    if "תלמידי כיתה" not in df.columns:
        st.error("העמודה 'תלמידי כיתה' לא נמצאה בקובץ.")
        st.stop()

    # =============================
    # לשונית 1 – תמונת מצב כיתתית
    # =============================
    with tabs[0]:
        st.header("תמונת מצב כיתתית")

        st.info(
            "תמונה כיתתית-מערכתית המבוססת על נתוני העוגן, "
            "כוללת מוקדי קושי וחוזקות בולטים לפי שכיחות."
        )

        difficulty_columns = {
            "שפה": "שליטה במיומנויות השפה (דבורה וכתובה) בהתאם למצופה מבני הגיל",
            "מתמטיקה": "שליטה במתמטיקה בהתאם למצופה מבני הגיל",
            "אנגלית": "שליטה באנגלית בהתאם למצופה מבני הגיל (החל מכיתה ד')",
            "מוטיבציה והרגלי למידה": "מוטיבציה והרגלי למידה בהתאם למצופה מבני הגיל",
            "רגשי": "היבטים רגשיים בהתאם למצופה מבני הגיל",
            "התנהגותי": "היבטים התנהגותיים בהתאם למצופה מבני הגיל",
            "חברתי": "היבטים חברתיים בהתאם למצופה מבני הגיל",
            "קשב": "תפקודי קשב ופעלתנות יתר בהתאם למצופה מבני הגיל",
            "חושי-תנועתי-מרחבי": "תפקוד חושי - תנועתי - מרחבי בהתאם למצופה מבני הגיל"
        }

        st.subheader("מוקדי קושי כיתתיים")

        graph_data = {}

        for domain, col in difficulty_columns.items():
            if col in df.columns:
                struggling_df = df[
                    df[col].astype(str).str.contains("מתקשה", na=False)
                ]

                if not struggling_df.empty:
                    names = struggling_df["תלמידי כיתה"].dropna().unique().tolist()

                    difficulties = struggling_df[col].apply(
                        lambda x: extract_meaningful_text(
                            x, ["מתקשה", "מתקשה מאד"]
                        )
                    ).dropna()

                    common_difficulty = (
                        difficulties.value_counts().idxmax()
                        if not difficulties.empty
                        else "קושי מגוון"
                    )

                    graph_data[domain] = len(names)

                    st.markdown(f"### {domain}")
                    st.write(f"**מספר תלמידים:** {len(names)}")
                    st.write(f"**שמות התלמידים:** {', '.join(names)}")
                    st.write(f"**קושי משותף בולט:** {common_difficulty}")

        if graph_data:
            st.subheader("התפלגות קשיים לפי תחומים")
            st.bar_chart(
                pd.DataFrame.from_dict(
                    graph_data,
                    orient="index",
                    columns=["מספר תלמידים מתקשים"]
                )
            )

        # =============================
        # חוזקות כיתתיות
        # =============================
        st.subheader("חוזקות ותחומי עניין כיתתיים")

        strengths_col = "התלמיד מגלה עניין ו/או חוזקות בתחום ייחודי אחד או יותר"

        if strengths_col in df.columns:
            strengths_df = df[df[strengths_col].astype(str).str.contains("כן", na=False)]

            strengths = strengths_df[strengths_col].apply(
                lambda x: extract_meaningful_text(x, ["כן", "לא", "לא ידוע"])
            ).dropna()

            if not strengths.empty:
                common_strength = strengths.value_counts().idxmax()
                st.write(f"**החוזקה הבולטת בכיתה:** {common_strength}")
            else:
                st.write("לא זוהתה חוזקה בולטת אחת.")

    # שאר הלשוניות – שלד
    with tabs[1]:
        st.header("תוכנית עבודה מרובדת")
        st.info("פיתוח בהמשך.")

    with tabs[2]:
        st.header("תוכנית התערבות אישית")
        student = st.selectbox(
            "בחרי תלמיד",
            sorted(df["תלמידי כיתה"].dropna().unique())
        )
        st.subheader(f"תוכנית אישית עבור: {student}")

    with tabs[3]:
        st.header("המלצות גפ\"ן")
        st.info("כיוונים פדגוגיים כלליים ללא שמות תוכניות.")

else:
    st.warning("יש להעלות קובץ עוגן כדי להתחיל.")
