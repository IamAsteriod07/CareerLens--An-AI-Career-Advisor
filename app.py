import streamlit as st
from main_mod import analyze_resume_vs_jd
import json

st.set_page_config(page_title="AI Career Advisor", layout="centered")
st.title("🤖 AI Career Advisor")
st.markdown("Upload your **Resume (PDF)** and paste a **Job Description (JD)** to get career insights.")

# File uploader
uploaded_resume = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

# Job description input
jd_text = st.text_area("🧾 Paste Job Description", height=200)

# Auto-run with button interaction
if st.button("🔍 Analyze"):
    if uploaded_resume and jd_text.strip():
        with st.spinner("Analyzing resume against job description..."):
            result = analyze_resume_vs_jd(uploaded_resume, jd_text)
        
        st.success("✅ Analysis Complete")

        if "error" in result:
            st.error("⚠️ Could not parse the LLM output.")
            st.text_area("📝 Raw LLM Output", result["raw_output"], height=300)
        else:
            # 📊 Match Score
            st.markdown("### 📈 <span style='font-size:22px;'>Match Score</span>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color:#4CAF50'>{result['match_score']}%</h2>", unsafe_allow_html=True)

            # 🔍 Missing Skills
            st.markdown("### 🧠 <span style='font-size:22px;'>Missing Skills</span>", unsafe_allow_html=True)
            if result['missing_skills']:
                st.markdown(
                    "".join([f"- {skill}<br>" for skill in result['missing_skills']]),
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("*None!* ✅")

            # 💡 Recommendations
            st.markdown("### 🛠️ <span style='font-size:22px;'>Recommendations</span>", unsafe_allow_html=True)
            for rec in result["recommendations"]:
                st.markdown(f"🔹 {rec}")

            # 🎯 Career Advice
            st.markdown("### 🎯 <span style='font-size:22px;'>Career Advice</span>", unsafe_allow_html=True)
            st.info(result["feedback"])
    else:
        st.warning("⚠️ Please upload a resume and paste a job description.")
import email_utils  # whichever file you placed your function in

if "error" not in result:
    st.markdown("### Email Results to Yourself")
    user_email = st.text_input("Enter your email to receive the report:")
    if st.button("📧 Send Email"):
        report = f"""AI Career Advisor Results
Match Score: {result.get("match_score")}
Missing Skills: {', '.join(result.get("missing_skills", []))}
Recommendations: {', '.join(result.get('recommendations', []))}
Career Advice: {result.get('feedback')}
        """
        # SMTP version:
        # feedback = email_utils.send_email(
        #     sender_email=os.environ.get("SENDER_EMAIL"),
        #     sender_password=os.environ.get("SENDER_PASSWORD"),
        #     receiver_email=user_email,
        #     subject="Your AI Career Advisor Results",
        #     body=report
        # )
        # SendGrid version:
        feedback = email_utils.send_email_sendgrid(
            receiver_email=user_email,
            subject="Your AI Career Advisor Results",
            body=report
        )
        st.info(feedback)
