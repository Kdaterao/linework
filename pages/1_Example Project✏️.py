import streamlit as st

#----------page configuration------------------------------------------------------

st.markdown(
    """
    <style>
    /* Make all sidebar text larger */
    section[data-testid="stSidebar"] * {
        font-size: 20px !important; /* Adjust the size as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)
#----------------------------------
#----------------------------------
video_url = "https://youtu.be/XE7Va2zaNzg"  # Replace with your YouTube video URL
st.video(video_url)

# Description
st.markdown("""
In this animation, the program was applied to the clothing and effects, streamlining the linework process for larger and more consistent shapes. The faces were completed manually, as smaller details were more prone to errors and required the precision of hand-drawn work. This approach balanced automation with artistic control, ensuring both efficiency and quality in the final piece.
""")

# Pros and Cons in two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **✅ Pros**
    - Significantly reduces time spent on large, repetitive shapes  
    - Maintains consistent line quality across clothing and effects  
    - Frees up more time for fine-tuning creative details  
    """)

with col2:
    st.markdown("""
    **⚠️ Cons**
    - Requires manual correction for delicate features like facial details  
    """)

# Fun Fact
st.markdown("""
---
**💡 Fun Fact:** All the sample images you see with the demo taken directly from this animation!
""")
