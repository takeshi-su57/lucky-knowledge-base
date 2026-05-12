from __future__ import annotations

import os

import requests
import streamlit as st

from lkb.web_ui_helpers import format_chunk_rows


API_BASE_URL = os.getenv("LKB_API_BASE_URL", "http://127.0.0.1:8000")


def _post_json(path: str, payload: dict) -> requests.Response:
    return requests.post(f"{API_BASE_URL}{path}", json=payload, timeout=30)


def _post_file(path: str, name: str, content: bytes) -> requests.Response:
    files = {"file": (name, content, "text/markdown")}
    return requests.post(f"{API_BASE_URL}{path}", files=files, timeout=60)


st.set_page_config(page_title="Lucky Knowledge Base", layout="wide")
st.title("Lucky Knowledge Base")
st.caption("Issue 05 web UI: ask questions, inspect evidence, upload docs, and leave feedback.")

if "last_chat" not in st.session_state:
    st.session_state.last_chat = None
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "error" not in st.session_state:
    st.session_state.error = ""

with st.sidebar:
    st.subheader("Index Controls")
    uploaded = st.file_uploader("Upload markdown", type=["md"])
    if st.button("Upload", use_container_width=True):
        if uploaded is None:
            st.session_state.error = "Please choose a markdown file first."
        else:
            response = _post_file("/upload", uploaded.name, uploaded.getvalue())
            if response.ok:
                st.success(f"Uploaded {response.json()['filename']}")
                st.session_state.error = ""
            else:
                st.session_state.error = response.text

    if st.button("Re-index", use_container_width=True):
        response = _post_json("/reindex", {"full_rebuild": False})
        if response.ok:
            report = response.json()
            st.success(
                "Indexed: total_chunks={total_chunks}, indexed_documents={indexed_documents}, skipped_documents={skipped_documents}".format(
                    **report
                )
            )
            st.session_state.error = ""
        else:
            st.session_state.error = response.text

question = st.text_input("Ask your knowledge base", placeholder="What changed in topic 09?")
ask_clicked = st.button("Ask", type="primary")

if ask_clicked:
    payload = {"question": question, "top_k": 5, "threshold": 0.1, "retrieval_strategy": "hybrid"}
    response = _post_json("/chat", payload)
    if response.ok:
        st.session_state.last_chat = response.json()
        st.session_state.last_question = question
        st.session_state.error = ""
    else:
        st.session_state.error = response.text

if st.session_state.error:
    st.error(st.session_state.error)

if st.session_state.last_chat:
    chat = st.session_state.last_chat
    st.subheader("Answer")
    st.write(chat["answer"])

    left, right = st.columns(2)
    with left:
        st.subheader("Sources / Citations")
        if chat["citations"]:
            for item in chat["citations"]:
                st.markdown(f"- `{item}`")
        else:
            st.info("No citations available for this answer.")
    with right:
        st.subheader("Retrieved Chunks")
        rows = format_chunk_rows(chat["retrieved_chunks"])
        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("No retrieval chunks found.")

    st.subheader("Feedback")
    feedback_col1, feedback_col2 = st.columns(2)
    comment = st.text_input("Optional feedback comment")
    with feedback_col1:
        if st.button("Thumbs Up"):
            response = _post_json(
                "/feedback",
                {
                    "answer_id": chat["answer_id"],
                    "rating": 1,
                    "comment": comment,
                    "question": st.session_state.last_question,
                    "answer": chat["answer"],
                    "retrieved_chunks": chat["retrieved_chunks"],
                },
            )
            if response.ok:
                st.success("Feedback saved.")
            else:
                st.error(response.text)
    with feedback_col2:
        if st.button("Thumbs Down"):
            response = _post_json(
                "/feedback",
                {
                    "answer_id": chat["answer_id"],
                    "rating": -1,
                    "comment": comment,
                    "question": st.session_state.last_question,
                    "answer": chat["answer"],
                    "retrieved_chunks": chat["retrieved_chunks"],
                },
            )
            if response.ok:
                st.success("Feedback saved and bad-answer trace logged.")
            else:
                st.error(response.text)
