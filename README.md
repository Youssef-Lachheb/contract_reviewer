# contract_reviewer

# 🤖 AI Contract Reviewer Suite

This repository contains two AI-powered contract review apps built with **Streamlit**, **Agno framework**, and **OpenAI** models. Developed as part of a timed technical test for **TalentPerformer**, these apps demonstrate real-world agentic reasoning, tool use, and production-ready integration strategies.

---

## 🗂️ Contents

### 1. `contract_reviewer1.py` — Classic Review Interface
> Upload a contract PDF, press **Review**, and get a detailed report analyzing:
- 🔍 **Legal Issues** — Risks, gaps, and clauses of concern
- 🏗️ **Structural Review** — Formatting, missing sections, clarity
- 🤝 **Negotiation Opportunities** — Clauses that are commonly negotiated

### 2. `contract_reviewer2.py` — Simulated WhatsApp UX
> Mimics a conversational upload and response flow:
- 📎 User "sends" contract like a WhatsApp file
- 💬 AI "responds" as if chatting, with insights and advice

---

## 💡 Features

- ✅ Built using **Agno** multi-agent orchestration
- ⚖️ Modular agents: Legal, Structural, and Negotiation Experts
- 📂 PDF Parsing via `pypdf`
- 📬 Simulated chatbot UI for a real client workflow
- 🤖 Powered by OpenAI's `gpt-4o` and `gpt-3.5-turbo` (switchable)

---


