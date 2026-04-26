import streamlit as st
import pandas as pd
import os

from src.skill_gap_engine_06 import ranked_skill_gap

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(page_title="Job Skill Analyzer", page_icon="🔍", layout="centered")

# ── Gemini Setup (new google.genai package) ───────────────────────
# Locally:  .streamlit/secrets.toml  →  GEMINI_API_KEY = "your-key"
# Streamlit Cloud: App Settings → Secrets → same line
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

gemini_client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.warning(f"⚠️ Could not init Gemini: {e}")

gemini_client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.warning(f"⚠️ Could not init Gemini: {e}")


# ── Helper: call Gemini safely ────────────────────────────────────
def ask_gemini(prompt: str) -> str:
    if not gemini_client:
        return "⚠️ Gemini API key not configured. Add GEMINI_API_KEY to .streamlit/secrets.toml"
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"❌ Gemini error: {e}"


# ── GenAI Feature 1: Skill Prioritizer ───────────────────────────
def get_skill_priority(missing_skills: list, target_role: str) -> str:
    prompt = f"""
You are a technical recruiter. A CS student wants to become a {target_role}.

They are missing these skills:
{chr(10).join(f"- {s}" for s in missing_skills)}

Rank them from MOST to LEAST important for getting hired.
For each skill write:
  [Rank]. [Skill] — [one-line reason] [🔴 Critical / 🟡 Important / 🟢 Nice-to-have]

Be concise. No markdown tables. Max 10 skills.
"""
    return ask_gemini(prompt)


# ── GenAI Feature 2: 4-Week Roadmap ──────────────────────────────
def get_learning_roadmap(missing_skills: list, target_role: str) -> str:
    top_skills = missing_skills[:6]
    prompt = f"""
Create a practical 4-week learning roadmap for a student targeting a {target_role} role.

Skills to learn:
{chr(10).join(f"- {s}" for s in top_skills)}

Use this exact format:
📅 WEEK 1 — [Theme]
  • Day 1-3: [specific task]
  • Day 4-5: [specific task]
  • Day 6-7: [specific task]
  📚 Free Resource: [course or link name]

📅 WEEK 2 — [Theme]
  ...

📅 WEEK 3 — [Theme]
  ...

📅 WEEK 4 — Projects & Portfolio
  ...

⚡ Quick Win: [One thing they can do TODAY in under 2 hours to get started]

Free resources only. Be specific and actionable.
"""
    return ask_gemini(prompt)


# ── GenAI Feature 3: Career Chatbot ──────────────────────────────

def career_chat(user_message: str, target_role: str, history: list) -> str:
    if not gemini_client:
        return "⚠️ Gemini API key not configured."
    try:
        # Build full conversation as a single prompt (simpler, works with new SDK)
        system_ctx = (
            f"You are CareerBot, a friendly and concise technical career advisor. "
            f"The user is a CS student targeting a '{target_role}' role. "
            f"Give short, actionable answers. No fluff.\n\n"
        )
        # Append history as conversation context
        convo = system_ctx
        for msg in history:
            role = "User" if msg["role"] == "user" else "CareerBot"
            convo += f"{role}: {msg['parts'][0]}\n"
        convo += f"User: {user_message}\nCareerBot:"

        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=convo
        )
        return response.text
    except Exception as e:
        return f"❌ Gemini error: {e}"




# ── Load dataset ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        return pd.read_csv("outputs/week4_market_insights.csv")
    except Exception:
        return pd.read_csv("outputs/week4_market_insights.csv", encoding="latin1")

df = load_data()


# ═════════════════════════════════════════════════════════════════
#  UI
# ═════════════════════════════════════════════════════════════════

st.title("🔍 Job Skill Analyzer")
st.markdown("Analyze your skill gap for different job roles — powered by **Google Gemini AI**")

if not GEMINI_API_KEY:
    st.warning("⚠️ AI features disabled. Add your **GEMINI_API_KEY** in `.streamlit/secrets.toml` to enable them.")
    st.write("Debug - all secrets:", list(st.secrets.keys()) if st.secrets else "NO SECRETS FOUND")

# ── Input Section ─────────────────────────────────────────────────
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

# ── Analyze Button ────────────────────────────────────────────────
if st.button("Analyze Skill Gap", type="primary"):

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
                result = result.drop_duplicates(subset=['skill'], keep='first')
                result = result.reset_index(drop=True)
                st.dataframe(result, use_container_width=True)

                st.subheader("📌 Top Skills to Learn")
                seen = set()
                count = 0
                for skill in result['skill']:
                    if skill not in seen:
                        seen.add(skill)
                        st.write(f"👉 {skill}")
                        count += 1
                    if count == 5:
                        break

                # Save missing skills to session state for AI features below
                seen_skills = []
                seen_set = set()
                for skill in result['skill']:
                    if skill not in seen_set:
                       seen_set.add(skill)
                       seen_skills.append(skill)
                st.session_state.missing_skills = seen_skills
                st.session_state.target_role = target_role
        except Exception as e:
                st.error(f"❌ Error: {e}")


# ═════════════════════════════════════════════════════════════════
#  AI FEATURES — shown after analysis is run
# ═════════════════════════════════════════════════════════════════

if st.session_state.get("missing_skills"):
    missing_skills = st.session_state.missing_skills
    target_role    = st.session_state.target_role

    st.markdown("---")
    st.markdown("## 🤖 AI-Powered Career Insights")
    st.caption("Powered by Google Gemini · Results are AI-generated and may vary")

    # ── AI Feature 1: Skill Prioritizer ──────────────────────────
    with st.expander("🎯 Which skills should I learn FIRST?", expanded=True):
        st.markdown("Get a ranked list of your skill gaps sorted by hiring importance.")
        if st.button("Prioritize My Skill Gaps"):
            with st.spinner("Ranking your skills by market demand..."):
                output = get_skill_priority(missing_skills, target_role)
            st.text(output)

    # ── AI Feature 2: Roadmap ─────────────────────────────────────
    with st.expander("🗓️ Generate My 4-Week Learning Roadmap"):
        st.markdown("Get a week-by-week study plan with **free resources** for your top skill gaps.")
        if st.button("Build My Roadmap"):
            with st.spinner("Crafting your personalized roadmap..."):
                output = get_learning_roadmap(missing_skills, target_role)
            st.text(output)

    # ── AI Feature 3: Career Chatbot ──────────────────────────────
    with st.expander("💬 Ask CareerBot Anything"):
        st.markdown(f"Ask anything about becoming a **{target_role}** — interview tips, tools, salary, projects...")

        # Session state for chat
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []     # Gemini format
        if "chat_display" not in st.session_state:
            st.session_state.chat_display = []     # display format

        # Render past messages
        for msg in st.session_state.chat_display:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Chat input
        user_msg = st.chat_input("e.g. What projects should I build for this role?")
        if user_msg:
            with st.chat_message("user"):
                st.write(user_msg)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    reply = career_chat(user_msg, target_role, st.session_state.chat_history)
                st.write(reply)

            # Update histories
            st.session_state.chat_display.append({"role": "user",      "content": user_msg})
            st.session_state.chat_display.append({"role": "assistant",  "content": reply})
            st.session_state.chat_history.append({"role": "user",  "parts": [user_msg]})
            st.session_state.chat_history.append({"role": "model", "parts": [reply]})