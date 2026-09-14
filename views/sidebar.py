import streamlit as st

def render_sidebar(github_user):
    with st.sidebar:
        st.header("⚙️ Repository")
        repo_input = st.text_input(
            "GitHub Repository",
            placeholder="https://github.com/owner/repository",
        )
        load_clicked = st.button(
            "🚀 Load Repository",
            use_container_width=True,
        )
        st.divider()
        st.write("### GitHub Account")
        st.success(f"Authenticated as:\n\n**{github_user.login}**")

    return repo_input, load_clicked
