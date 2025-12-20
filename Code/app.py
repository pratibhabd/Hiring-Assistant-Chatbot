import streamlit as st
from llm_utils import generate_questions, evaluate_answers
from utils import *

# ---------------- UI HELPER ----------------
def assistant_box(text):
    return f"""
    <div style="
        background: linear-gradient(135deg, #e0f2fe, #f0f9ff);
        border-left: 6px solid #3b82f6;
        padding: 18px 20px;
        border-radius: 16px;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 10px;
    ">
        {text}
    
    """

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Hiring Assistant",
    page_icon="🧑‍💼",
    layout="centered"
)

st.title("Hiring Assistant")

st.markdown("""
<style>
div.stButton > button {
    font-weight: 900;
    font-size: 15px;
    background-color: #fee2e2;
    color: #991b1b;
    border: 1px solid #fecaca;
    border-radius: 10px;
    padding: 10px 16px;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([8, 2])

with col2:
    if st.button("🚪 Quit Interview"):
        st.session_state.quit_interview = True
        st.session_state.interview_completed = True

# ✅ FULL-WIDTH MESSAGE (outside columns)
if st.session_state.get("interview_completed"):
    st.markdown("""
    <div style="
        width: 100%;
        padding: 16px;
        margin-top: 12px;
        background-color: #EAF4FF;
        border-radius: 12px;
        font-size: 16px;
    ">
   🚪 <b>Thanks for your time!</b><b>🤝All the best!</b>
    </div>
    """, unsafe_allow_html=True)

# ---------------- SESSION STATE INIT ----------------
defaults = {
    "started": False,
    "messages": [],
    "last_question": None,
    "questions": [],
    "answers": [],
    "evaluations": [],
    "q_index": 0
}
if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False

if "quit_interview" not in st.session_state:
    st.session_state.quit_interview = False

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- GREETING ----------------
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content":
            """
            <div style="
            background: linear-gradient(135deg, #e0f2fe, #f0f9ff);
            border-left: 6px solid #3b82f6;
            padding: 18px 20px;
            border-radius: 16px;
            font-family: 'Poppins', sans-serif;
        ">
            <h3 style="margin: 0; color: #1e3a8a; font-weight: 700;">
                👋 Welcome!
            </h3>
            <p style="margin: 10px 0; color: #1f2937; font-size: 15px;">
                I’m your <b style="color:#2563eb;">AI Hiring Assistant</b>, here to guide you through a
                <b>structured</b> and <b>fair</b> interview process.
            </p>
            <p style="margin: 0; font-size: 15px;">
                ✨ <b style="color:#047857;">When you’re ready</b>, type
                <span style="background:#dbeafe; padding:4px 8px; border-radius:8px; font-weight:600;">hi</span>
                or
                <span style="background:#dbeafe; padding:4px 8px; border-radius:8px; font-weight:600;">ok</span>
                to begin.
            </p>
        </div>
        """
    })
# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# ---------------- USER INPUT ----------------
query = None
if not st.session_state.interview_completed:
    query = st.chat_input("Answer and hit Enter!")
else:
    st.info("🔒 Interview completed. Chat is now closed.")
#query = st.chat_input("Answer and hit Enter!")

if query:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # ---------------- FLOW CONTROL ----------------
    if not st.session_state.started:
        if query.lower() in ["hi", "ok", "start", "okay"]:
            st.session_state.started = True
            st.session_state.last_question = "name"
            response = assistant_box("Great! 😊<br><br>What is your <b>full name</b>?")
        else:
            response = assistant_box("Please type <b>hi</b> or <b>ok</b> to start.")

    else:
        # ---------------- BASIC DETAILS ----------------
        if st.session_state.last_question == "name":
            valid, msg = validate_name(query)
            response = assistant_box(
                f"Nice to meet you, {query}! 📧 What is your <b>email address</b>?"
            ) if valid else assistant_box(f"⚠️ {msg}")
            if valid:
                st.session_state.user_name = query
                st.session_state.last_question = "email"

        elif st.session_state.last_question == "email":
            if validate_email(query):
                st.session_state.user_email = query
                st.session_state.last_question = "role"
                response = assistant_box("Thanks! 💼 What is your <b>current role</b>?")
            else:
                response = assistant_box("⚠️ Please enter a valid email.")

        elif st.session_state.last_question == "role":
            valid, msg = validate_role_semantic(query)
            response = assistant_box(
                "Thanks! What is your <b>experience (years/months)</b>?"
            ) if valid else assistant_box(f"⚠️ {msg}")
            if valid:
                st.session_state.user_role = query
                st.session_state.last_question = "experience"

        elif st.session_state.last_question == "experience":
            if validate_experience(query):
                st.session_state.user_experience = query
                st.session_state.last_question = "phone"
                response = assistant_box("Great! What is your <b>phone number</b>?")
            else:
                response = assistant_box("⚠️ Please enter valid experience.")

        elif st.session_state.last_question == "phone":
            if validate_indian_phone(query):
                st.session_state.user_phonenumber = query
                st.session_state.last_question = "techstack"
                response = assistant_box("Thanks! What is your <b>tech stack</b>?")
            else:
                response = assistant_box("⚠️ Please enter valid phone number.")

        # ---------------- QUESTION GENERATION ----------------
        elif st.session_state.last_question == "techstack":
            valid, msg = validate_tech_stack(query)
            if valid:
                st.session_state.user_techstack = query
                raw = generate_questions(
                    st.session_state.user_experience,
                    st.session_state.user_role,
                    query
                )
                st.session_state.questions = [
                    q.strip() for q in raw.split("\n") if q.strip()
                ]
                st.session_state.q_index = 0
                st.session_state.last_question = "asking_questions"
                response = assistant_box(
                    f"<b>Question 1:</b><br>{st.session_state.questions[0]}"
                )
            else:
                response = assistant_box(f"⚠️ {msg}")

        # ---------------- INTERVIEW QUESTIONS ----------------
        elif st.session_state.last_question == "asking_questions":
            st.session_state.answers.append(query)

            evaluation = evaluate_answers(
                role=st.session_state.user_role,
                experience=st.session_state.user_experience,
                tech_stack=st.session_state.user_techstack,
                question=st.session_state.questions[st.session_state.q_index],
                answer=query
            )
            st.session_state.evaluations.append(evaluation)

            summary = "<br>".join(
                [f"Q{i+1}: {e}" for i, e in enumerate(st.session_state.evaluations)]
            )

            st.session_state.q_index += 1

            if st.session_state.q_index < len(st.session_state.questions):
                next_q = st.session_state.questions[st.session_state.q_index]
                response = assistant_box(f"""
                💡 Evaluation:{evaluation}<br><br>
                📊 <b>Progress:</b><br>{summary}<br><br>
                👉 <b>Next Question:</b><br>{next_q}
                """)
            else:
                response = assistant_box(f"""
                💡 Final Evaluation:{evaluation}
                ✅ <b>Interview completed!</b><br><br>
                📊 <b>Summary:</b><br>{summary}<br><br>
                {goodbye_message()}
                
                """)
                # 🔒 BLOCK CHAT FROM HERE ON
                st.session_state.interview_completed = True

    # ---------------- SHOW ASSISTANT MESSAGE ----------------
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response, unsafe_allow_html=True)
