import streamlit as st
import pandas as pd
from src.skill_gap_engine_06 import ranked_skill_gap

# Page config
st.set_page_config(page_title="Job Skill Analyzer", page_icon="🔍", layout="centered")

# Title
st.title("🔍 Job Skill Analyzer")
st.markdown("Analyze your skill gap for different job roles")

# Load dataset
@st.cache_data
def load_data():
    try:
        return pd.read_csv("outputs/week4_market_insights.csv")
    except:
        return pd.read_csv("outputs/week4_market_insights.csv", encoding="latin1")

df = load_data()

# Input section
st.subheader("🧠 Enter Your Details")

user_input = st.text_input(
    "Enter your skills (comma-separated):",
    placeholder="e.g. python, sql, excel"
)

role_options = [
    "data analyst",
    "data scientist",
    "machine learning engineer",
    "data engineer"
]

target_role = st.selectbox("Select your target role:", role_options)

# Button
if st.button("Analyze Skill Gap"):

    if not user_input:
        st.warning("⚠️ Please enter your skills")
    else:
        user_skills = [s.strip().lower() for s in user_input.split(",")]

        try:
            result = ranked_skill_gap(user_skills, target_role, df)

            st.subheader("📊 Skill Gap Analysis")

            if isinstance(result, str):
                st.error(result)
            else:
                st.success("✅ Analysis Complete!")

                st.dataframe(result, use_container_width=True)

                st.subheader("📌 Top Skills to Learn")
                for skill in result['skill'].head(5):
                    st.write(f"👉 {skill}")

        except Exception as e:
            st.error(f"❌ Error: {e}")