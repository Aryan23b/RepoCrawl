import streamlit as st

def render_repository(repository, chunks):
    st.divider()
    st.subheader(f"📂 {repository.full_name}")
    st.success(f"Repository ready — {len(chunks)} chunks indexed.")

    with st.expander("Repository details"):
        st.write(f"**Owner:** {repository.owner}")
        st.write(f"**Default branch:** {repository.default_branch}")
        st.write(f"**URL:** {repository.url}")
