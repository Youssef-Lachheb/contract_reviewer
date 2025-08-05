# === Imports ===
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from agno.team import Team
from textwrap import dedent
from pypdf import PdfReader
from agno.agent import Agent
from agno.models.openai import OpenAIChat

st.set_page_config(page_title="WhatsApp Contract AI", layout="centered")

# === WhatsApp UI Header ===
st.markdown("""
<style>
.whatsapp-chat {
    background-color: #e5ddd5;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    color: #000;
}
.user-msg {
    background-color: #dcf8c6;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 10px;
    max-width: 100%;
}
.ai-msg {
    background-color: white;
    padding: 10px;
    border-radius: 8px;
    max-width: 100%;
    border: 1px solid #ccc;
}
</style>
""", unsafe_allow_html=True)

st.title("📱 WhatsApp Contract Review Bot")
st.markdown("Simulate sending a contract via WhatsApp and getting a full AI review.")

# === Simulated WhatsApp Input ===
st.markdown('<div class="whatsapp-chat">', unsafe_allow_html=True)
st.markdown('<div class="user-msg">📎 You: [Sent a contract PDF]</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Contract PDF (Simulated WhatsApp Upload)", type=["pdf"])
full_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    full_text = "".join(page.extract_text() or "" for page in reader.pages)
    if not full_text:
        st.error("⚠️ No text found in the contract.")
        st.stop()

    # === Document Tool ===
    def get_document():
        return {
            "content": full_text,
            "meta_data": {"source": uploaded_file.name}
        }

    # === Agents (same as before) ===
    structure_agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        name="Structure Agent",
        role="Contract Structuring Expert",
        instructions=dedent("""
            You are a Contract Structuring Expert. Your role is to evaluate the structure of a contract and suggest improvements or build a proper structure from scratch if not provided.
            You will use the tool `get_document` to retrieve the full contract text.
            Your task is to analyze the contract and determine if it is structured in a clear, complete, and legally appropriate way.
            You must identify missing or unclear sections.
            If a contract is missing structure, suggest a full structure using standard section headers (e.g., Definitions, Terms, Obligations, Termination, Governing Law, etc.).
            Avoid legal interpretation – focus only on organization, clarity, and logical flow.
            Be concise but clear in your analysis.
            Output a markdown-style structure if creating a new structure, or bullet-pointed comments if evaluating an existing one.
        """),
        tools=[get_document],
        show_tool_calls=False,
        markdown=True
    )

    legal_agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        name="Legal Agent",
        role="Legal Issue Analyst",
        instructions=dedent("""
            You are a Legal Framework Analyst tasked with identifying legal issues, risks, and key legal principles in the uploaded contract.

            Use the `get_document` tool to access the full contract text. For every legal issue or observation, you MUST:

            - Quote the exact clause, sentence, or paragraph from the contract that your point is based on.
            - Start a new line with 'Issue:' followed by a short, clear explanation of the legal concern or principle.
            - Clearly refer to the section title, heading, or paragraph number if available. If not, describe its location (e.g., "section starting with 'Termination...'").
            - DO NOT make any legal assessment or comment unless it is directly supported by a quote from the contract.

            Your task:
            - Identify the legal domain of the contract (e.g., commercial law, employment, NDA, etc.)
            - Determine the likely jurisdiction or applicable law
            - Highlight any potential legal issues or problematic clauses

            Format each finding as follows:
            🔹 Clause: "Quoted contract text here."
            📍 Section: [Section title or location]
            ⚠️ Issue: Your brief analysis of why this clause may present a legal concern.
        """),
        tools=[get_document],
        show_tool_calls=False,
        markdown=True
    )

    negotiate_agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        name="Negotiation Agent",
        role="Contract Negotiation Strategist",
        instructions=dedent("""
            You are a Contract Negotiation Strategist.

            Your job is to identify parts of a contract that are commonly negotiable or potentially unbalanced. You MUST:

            – Always quote the exact paragraph or clause you're referring to.
            – Clearly explain why it may be negotiable or needs adjustment.
            – Suggest a counter-offer or alternative phrasing.

            Structure your analysis like this:
            1. **Quoted clause** (exact text from contract)
            2. **Why it is negotiable or problematic**
            3. **Example strategy or counter suggestion**

            Do NOT make general comments. Every point you make must be backed by a direct quote from the contract, and your output must clearly show which part of the contract you're referring to.
        """),
        tools=[get_document],
        show_tool_calls=False,
        markdown=True
    )

    manager_agent = Team(
        members=[structure_agent, legal_agent, negotiate_agent],
        model=OpenAIChat(id="gpt-3.5-turbo"),
        mode="coordinate",
        success_criteria=dedent("""
            A well-organized and traceable summary of the contract that includes:
            – Legal context highlighting potential legal issues with quoted contract text as evidence
            – Structural review with clarity and formatting suggestions
            – Negotiation strategies directly tied to specific paragraphs or clauses
        """),
        instructions=dedent("""
            You are the lead summarizer. You must combine input from:
            1. Legal Agent
            2. Structure Agent
            3. Negotiation Agent

            Key Requirements:
            – For all legal and negotiation points, preserve quoted clauses from the contract as evidence.
            – The Legal Agent should highlight specific legal issues, followed by a short 'Issue:' explanation.
            – The Structure Agent should suggest formatting or structural improvements.
            – The Negotiation Agent should explain why certain parts are negotiable and suggest alternatives.
            
            Present a clean, readable, and logically ordered report.
        """)
    )

    with st.spinner("🧠 Analyzing contract via simulated WhatsApp..."):
        result = manager_agent.run("Use the get_document tool to access the full contract and summarize it.")

    # === Simulated WhatsApp Reply
    st.markdown('<div class="ai-msg"><b>🤖 AI Assistant:</b><br>' + result.content.replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # close .whatsapp-chat

