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


def extract_meaningful_line(cell_text):
    """
    מחלץ את הטקסט המשמעותי מתוך תא בעוגן.
    לוקח אך ורק שורה שמתחילה במקף (או bullet),
    ומתעלם משורות סטטוס (מתקשה / כן וכו').
    """
    if pd.isna(cell_text):
        return None

    lines = str(cell_text).splitlines()

    for line in lines:
        raw = line.strip()

        # דילוג על שורות סטטוס
        if (
            "מתקשה" in raw
            or raw in ["כן", "לא", "לא ידוע"]
        ):
            continue

        # חיפוש שורה שמתחילה במקף / bullet
        if re.match(r'^[\-\–\—\•\*]', raw):
            clean = re.sub(r'^[\-\–\—\•\*\s]+', '', raw)
            clean = re.sub(r'\s+', ' ', clean).strip()
            if clean:
                return clean

    return None


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
            if col not in df.columns:
                continue

            struggling_df = df[
                df[col].astype(str).str.contains("מתקשה", na=False)
            ]

            if struggling_df.empty:
                continue

            names = struggling_df["תלמידי כיתה"].dropna().unique().tolist()

            difficulties = struggling_df[col].apply(
                extract_meaningful_line
            ).dropna()

            if not difficulties.empty:
                common_difficulty = difficulties.value_counts().idxmax()
            else:
                common_difficulty = "לא צוין סוג קושי שכיח בנתונים"

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
            strengths_df = df[
                df[strengths_col].astype(str).str.contains("כן", na=False)
            ]

            strengths = strengths_df[strengths_col].apply(
                extract_meaningful_line
            ).dropna()

            if not strengths.empty:
                common_strength = strengths.value_counts().idxmax()
            else:
                common_strength = "לא צוין תחום חוזקה שכיח"

            st.write(f"**החוזקה הבולטת בכיתה:** {common_strength}")

    # =============================
    # לשוניות נוספות – שלד
    # =============================
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
