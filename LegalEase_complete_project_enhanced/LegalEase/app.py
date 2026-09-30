import requests
import streamlit as st

from config import BACKEND_URL
from utils.document_formatter import format_docx, format_pdf
from utils.text_utils import sanitize_text
from utils.document_formatter import format_html_preview

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .hero {text-align:center; padding: 0.5rem 0 1rem 0;}
    .hero h1 {margin-bottom:0.1rem;}
    .preview {
        background:#151922;
        color:#f2f4f8;
        padding:1.2rem;
        border-radius:12px;
        max-height:650px;
        overflow-y:auto;
        line-height:1.65;
    }
    .preview h3 {color:#ffffff; margin-top:1.2rem;}
    .preview p {margin:0.45rem 0;}
    .preview .bullet {margin:0.35rem 0 0.35rem 1rem;}
    .preview .spacer {height:0.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>⚖️ LegalEase</h1>
        <p>AI-Powered Legal Document Generator</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Backend")
    st.code(BACKEND_URL)
    st.caption(
        "LegalEase creates AI-assisted drafts. Review all generated content "
        "with an appropriate legal professional before signing or relying on it."
    )

col1, col2 = st.columns(2)

with col1:
    document_type = st.text_input(
        "Document Type",
        placeholder="Freelance Work Contract",
        help="Examples: Agreement, Contract, NDA, Lease Agreement, Employment Offer Letter.",
    )
    parties = st.text_area(
        "Parties Involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=130,
    )

with col2:
    dates = st.text_input(
        "Effective Date",
        placeholder="April 15, 2025",
    )
    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment to be made within 30 days of invoice; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=130,
        help="Use semicolons to separate terms, as specified in the project document.",
    )

if st.button("Generate Document", type="primary", use_container_width=True):
    missing = [
        name
        for name, value in [
            ("Document Type", document_type),
            ("Parties", parties),
            ("Terms", terms),
            ("Effective Date", dates),
        ]
        if not value.strip()
    ]

    if missing:
        st.error("Please provide: " + ", ".join(missing))
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
        }
        try:
            with st.spinner("Generating your document..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=180,
                )
            if response.ok:
                data = response.json()
                st.session_state["document"] = sanitize_text(data["content"])
                st.session_state["document_type"] = document_type
                st.success("Document generated successfully.")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                st.error(f"Backend error ({response.status_code}): {detail}")
        except requests.RequestException as exc:
            st.error(
                "Could not connect to FastAPI. Start the backend first. "
                f"Details: {exc}"
            )

if "document" in st.session_state:
    st.divider()
    st.subheader("Document Preview")

    preview_html = format_html_preview(st.session_state["document"])
    st.markdown(f"<div class='preview'>{preview_html}</div>", unsafe_allow_html=True)

    st.subheader("Edit Document")
    edited = st.text_area(
        "Editable document text",
        value=st.session_state["document"],
        height=500,
        label_visibility="collapsed",
    )
    st.session_state["document"] = edited

    doc_type = st.session_state["document_type"]
    txt_bytes = sanitize_text(edited).encode("utf-8")
    docx_bytes = format_docx(edited, doc_type)
    pdf_bytes = format_pdf(edited, doc_type)

    safe_name = "".join(
        c.lower() if c.isalnum() else "_"
        for c in doc_type
    ).strip("_") or "legal_document"

    d1, d2, d3 = st.columns(3)
    with d1:
        st.download_button(
            "Download TXT",
            data=txt_bytes,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name=f"{safe_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with d3:
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
