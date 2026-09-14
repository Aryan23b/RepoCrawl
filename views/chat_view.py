import streamlit as st

def render_chat(chat_viewmodel):
    st.divider()
    st.subheader("💬 Chat")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask something about the repository...")
    if not question:
        return

    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("🔍 Searching repository..."):
                result = chat_viewmodel.ask(
                    question,
                    st.session_state.documents,
                    st.session_state.embeddings,
                )

            st.markdown(result["answer"])

            with st.expander("📚 Sources used"):
                for source in result["sources"]:
                    chunk = source["chunk"]
                    st.markdown(
                        f"**{chunk.path}** "
                        f"(lines {chunk.start_line}-{chunk.end_line}) — "
                        f"similarity `{source['score']:.4f}`"
                    )

            st.session_state.messages.append({
                "role": "assistant",
                "content": result["answer"],
            })

        except Exception as exc:
            text = str(exc)

            if "429" in text:
                message = "⚠️ Hugging Face rate limit reached. Please wait and try again."
            elif any(code in text for code in ("503", "UNAVAILABLE", "500", "502", "504")):
                message = "⚠️ Hugging Face is temporarily busy. Please try again."
            else:
                message = f"❌ Error generating answer:\n\n{text}"

            st.error(message)
            st.session_state.messages.append({
                "role": "assistant",
                "content": message,
            })
