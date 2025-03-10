import streamlit as st

def show_image(image_path):
    # Read about GDG on Campus PUP
    st.markdown("""
    <style>
        .rounded-image img {
            border-radius: 10px;  /* Adjust the value to control the roundness */
        }
    </style>
    """, unsafe_allow_html=True)

    # Apply the rounded-image class to a container
    with st.container():
        st.markdown('<div class="rounded-image">', unsafe_allow_html=True)
        st.image(f"{image_path}", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
