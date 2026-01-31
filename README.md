# 🛡️ BUILDEDGE: Multi-Agent Forensic Suite
**Winner/Project for Echelon Hackathon 2026** A state-of-the-art multimodal misinformation detection system using a hierarchical multi-agent architecture.

## 🚀 Overview
BUILDEDGE is a specialized forensic workstation designed to detect sophisticated digital misinformation. Unlike single-model detectors, BUILDEDGE employs a "Democratic Voting System" where specialized AI agents cross-examine media across visual, contextual, and logical dimensions.

## 🧠 Architecture: The Multi-Agent Team
Our system uses a **Master-Specialist** pattern to ensure high accuracy and explainability:

- **Master Orchestrator (Gemini 3 Flash):** The "Judge" that coordinates specialists and performs Weighted Decision Fusion.
- **Vision Specialist (CLIP ViT-L/14):** Analyzes raw pixel-to-text alignment.
- **Context Specialist (Llama 3.2-Vision):** Performs OCR to detect "Context Drift" in banners and signs.
- **Thinking Agent (DeepSeek-R1):** Executes Chain-of-Thought reasoning to find logical contradictions.

## ⚖️ Weighted Decision Fusion
To resolve conflicts (like simple geometric shapes causing low CLIP scores), our Master AI applies the following formula:
**Final Score = (Logic × 0.4) + (Context × 0.3) + (Vision × 0.3)**

## 🛠️ Installation & Setup
1. **Clone the Repo:** `git clone https://github.com/your-username/BUILDEDGE`
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Configure Secrets:** Add your API keys to `.streamlit/secrets.toml`
4. **Run App:** `streamlit run app.py`

## 📜 Forensic Audit Trail
Every analysis generates a **Forensic Audit Log** (`data/logs/forensic_audit.jsonl`), ensuring complete transparency for legal or professional investigative use.