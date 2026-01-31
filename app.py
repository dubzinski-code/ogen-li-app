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

if uploaded_file is not None:
    if uploaded_file.name.endswith(".xls"):
        df = pd.read_excel(uploaded_file, engine="xlrd")
    else:
        df = pd.read_excel(uploaded_file)

    if "תלמידי כיתה" not in df.columns:
        st.error("העמודה 'תלמידי כיתה' לא נמצאה בקובץ.")
        st.stop()

    # -----------------------------
    # לשונית 1 – תמונת מצב כיתתית
    # -----------------------------
    with tabs[0]:
        st.header("תמונת מצב כיתתית")

        st.info(
            "תצוגה זו מציגה תמונת מצב כיתתית-מערכתית המבוססת על נתוני העוגן. "
            "ההצגה לפי תחומים וכוללת שמות תלמידים רק במוקדי קושי."
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
                struggling_df = df[df[col].isin(["מתקשה", "מתקשה מאד"])]

                if not struggling_df.empty:
                    student_names = (
                        struggling_df["תלמידי כיתה"]
                        .dropna()
                        .unique()
                        .tolist()
                    )

                    # קושי משותף – התיאור השכיח ביותר
                    common_difficulty = (
                        struggling_df[col]
                        .value_counts()
                        .idxmax()
                    )

                    graph_data[domain] = len(student_names)

                    st.markdown(f"### {domain}")
                    st.write(f"**מספר תלמידים:** {len(student_names)}")
                    st.write(f"**שמות התלמידים:** {', '.join(student_names)}")
                    st.write(f"**קושי משותף בולט:** {common_difficulty}")

        if graph_data:
            st.subheader("התפלגות קשיים לפי תחומים")
            graph_df = pd.DataFrame.from_dict(
                graph_data, orient="index", columns=["מספר תלמידים מתקשים"]
            )
            st.bar_chart(graph_df)
        else:
            st.info("לא נמצאו תלמידים מתקשים או מתקשים מאד באף תחום.")

        # -----------------------------
        # חוזקות כיתתיות
        # -----------------------------
        st.subheader("חוזקות ותחומי עניין כיתתיים")

        strengths_col = "התלמיד מגלה עניין ו/או חוזקות בתחום ייחודי אחד או יותר"
        if strengths_col in df.columns:
            strengths_count = (df[strengths_col] == "כן").sum()
            total_students = df["תלמידי כיתה"].nunique()

            st.metric(
                "מספר תלמידים עם תחומי עניין / חוזקות",
                strengths_count
            )

            if strengths_count >= max(3, int(0.2 * total_students)):
                st.write(
                    "בכיתה קיימת נוכחות משמעותית של תלמידים עם תחומי עניין וחוזקות, "
                    "המהווה פוטנציאל להובלה, העשרה ויוזמה כיתתית."
                )
            else:
                st.write(
                    "זוהו מספר תלמידים עם תחומי עניין וחוזקות, "
                    "בהיקף נקודתי בשלב זה."
                )
        else:
            st.info("לא נמצאה עמודת חוזקות בקובץ.")

    # -----------------------------
    # שאר הלשוניות – שלד
    # -----------------------------
    with tabs[1]:
        st.header("תוכנית עבודה מרובדת")
        st.info("פיתוח בהמשך – בהתאם ל-MTSS.")

    with tabs[2]:
        st.header("תוכנית התערבות אישית")
        student = st.selectbox(
            "בחרי תלמיד",
            sorted(df["תלמידי כיתה"].dropna().unique())
        )
        st.subheader(f"תוכנית אישית עבור: {student}")
        st.info("פירוט אישי יורחב בשלב הבא.")

    with tabs[3]:
        st.header("המלצות גפ\"ן")
        st.info(
            "כיוונים פדגוגיים כלליים למענה כיתתי או קבוצתי "
            "(ללא ציון שמות תוכניות או ספקים)."
        )

else:
    st.warning("יש להעלות קובץ עוגן (Excel) כדי להתחיל.")
