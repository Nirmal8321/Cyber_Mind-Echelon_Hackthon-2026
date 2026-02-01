import streamlit as st
from PIL import Image
import requests
import base64
from io import BytesIO
import uuid

from core.orchestrator import orchestrator
from utils.video_utils import extract_frames
from utils.report_gen import generate_pdf_report


# ---------- Page Config ----------
st.set_page_config(
    page_title="BUILDEDGE | Verification Suite",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Modern Dark Glass UI ----------
st.markdown("""
<style>

/* Background */
html, body, .stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e5e7eb;
}

/* Typography */
h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 700;
}

p, label, span {
    color: #cbd5f5 !important;
}

/* Glass Cards */
[data-testid="stVerticalBlock"] > div {
    background: rgba(17, 24, 39, 0.65);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* File Uploader */
[data-testid="stFileUploader"] {
    border-radius: 14px;
    border: 1px dashed #38bdf8;
    background-color: rgba(2, 6, 23, 0.6);
}

/* Text Area */
textarea {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    color: white !important;
    border-radius: 14px;
    height: 3.6em;
    font-size: 1rem;
    font-weight: 700;
    border: none;
    transition: all 0.25s ease-in-out;
    box-shadow: 0 10px 25px rgba(37,99,235,0.35);
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 15px 30px rgba(6,182,212,0.45);
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(2, 6, 23, 0.7);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.06);
}

[data-testid="stMetricLabel"] p {
    color: #94a3b8 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
    font-size: 1.6rem;
    font-weight: 800;
}

/* Progress Bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #22c55e, #06b6d4);
    border-radius: 10px;
}

/* Alerts */
.stAlert {
    background: rgba(2, 6, 23, 0.8);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
}

.stAlert p {
    color: #e5e7eb !important;
    font-weight: 600;
}

/* Expander */
details {
    background: rgba(2, 6, 23, 0.75);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 10px;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #38bdf8, transparent);
}

</style>
""", unsafe_allow_html=True)


# ---------- Header ----------
st.title("🛡️ BUILDEDGE")
st.caption("AI-Powered Media Verification • Multi-Agent Forensics • Trust Engine")
st.info("Echelon Hackathon 2026 | Content Integrity & Authenticity Analysis")


# ---------- ImgBB Upload ----------
def upload_to_imgbb(image):
    try:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": st.secrets["IMGBB_API_KEY"],
            "image": img_str
        }
        res = requests.post(url, payload)
        if res.status_code == 200:
            return res.json()["data"]["url"]
        return None
    except Exception as e:
        st.warning(f"Image upload failed: {e}")
        return None


# ---------- Layout ----------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📤 Input Media")
    uploaded_file = st.file_uploader(
        "Upload Image or Video",
        type=["jpg", "png", "jpeg", "mp4", "mov"]
    )

    user_text = st.text_area(
        "Context / Headline",
        placeholder="Enter the claim associated with this media..."
    )

    start_audit = st.button(
        "🚀 Start Multi-Agent Verification Audit",
        use_container_width=True,
        disabled=not uploaded_file or not user_text
    )


with col2:
    if start_audit and uploaded_file and user_text:

        # ---------- Media Processing ----------
        if uploaded_file.name.endswith((".mp4", ".mov")):
            video_path = f"temp_{uuid.uuid4().hex}.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            frames = extract_frames(video_path, interval=1)

            if not frames:
                st.error("Failed to extract frames from video.")
                st.stop()

            image_to_analyze = Image.open(frames[len(frames)//2])
            st.video(uploaded_file)

        else:
            image_to_analyze = Image.open(uploaded_file)
            st.image(image_to_analyze, caption="Source Media", use_container_width=True)

        # ---------- AI Orchestration ----------
        with st.spinner("🔍 AI agents are auditing content integrity..."):
            public_url = upload_to_imgbb(image_to_analyze)
            results = orchestrator.run_full_forensics(
                image_to_analyze,
                user_text,
                image_url=public_url
            )

        # ---------- Results ----------
        st.divider()
        st.subheader("📊 Verification Audit Scorecard")

        reports = results.get("reports", {})
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Vision", f"{reports.get('Vision', 0):.1f}")
        m2.metric("Context", f"{reports.get('Context', 0):.1f}")
        m3.metric("Ground Truth", f"{reports.get('Ground Truth', 0):.1f}")
        m4.metric("Logic", f"{reports.get('Logic', 0):.1f}")

        score = results.get("final_score", 0.0)
        st.markdown(f"### Authenticity Index: **{score:.1f}% Real**")
        st.progress(min(score / 100, 1.0))

        if score < 40:
            st.error("🔴 VERDICT: NOT TRUE")
        elif score < 65:
            st.warning("🟡 VERDICT: INCONCLUSIVE")
        else:
            st.success("🟢 VERDICT: VERIFIED TRUE")

        # ---------- Summary ----------
        st.markdown("---")
        raw_reason = results.get("reason", "")

        if "MASTER EXPLAINER:" in raw_reason:
            parts = raw_reason.split("MASTER EXPLAINER:")
            summary_part = parts[0].replace("SUMMARY:", "").strip()
            explainer_part = parts[1].strip()
        else:
            summary_part = "Audit summary not available."
            explainer_part = raw_reason

        st.markdown("### 📝 Summary")
        st.info(summary_part)

        with st.expander("📖 View Master Explainer", expanded=True):
            st.write(explainer_part)

        # ---------- PDF ----------
        pdf_bytes = generate_pdf_report(results, user_text)
        st.download_button(
            "📥 Download Verification Audit Report (PDF)",
            data=pdf_bytes,
            file_name="Verification_Audit_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    else:
        st.markdown("### 👋 Verification Hub")
        st.write("Upload media and enter context on the left to begin the audit.")
