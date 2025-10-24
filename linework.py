import streamlit as st
from model import model

import io

#----------page configuration------------------------------------------------------
st.set_page_config(layout='centered', page_title="Linework")
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
#--------------- variables initializations---------------------------------------
gap_image = None
final_image = None

if 'nodefault' not in st.session_state:
    st.session_state['nodefault'] = False

#------------------Title + description UI -----------------------------------------

st.markdown(
    """
    <h1 style="font-size:40px; text-decoration:underline; text-decoration-color: #0F52BA;">Linework Tool for <span style="color:#0F52BA;">Animators</span></h1>
    """,
    unsafe_allow_html=True
)

col1, col2= st.columns([0.65,0.35], gap = 'small' )
with col1:
    st.markdown('###### :blue[Detects and fills in gaps] for black and white images, aiding in linework tasks for animation')
with col2:
    if st.button(":blue[Example Project using tool ✏️]"):
        st.switch_page("pages/1_Example Project✏️.py")
st.divider()


#------------------ sidebar UI + handling input --------------------------------------

input_image = st.sidebar.file_uploader(":blue[Upload Image here ↓]", type=["png"])


# Information about limitations
with st.sidebar.expander("ℹ️ Image Guidelines"):
    st.write("""
    - 1080x1920 
    - png 
    """)

st.sidebar.divider()

#-------------------handling default image------------------------------------------

if input_image is not None:
    input_image = input_image
elif st.session_state['nodefault'] == False:
    with open('./assets/25_2.0031.png', 'rb') as f:
        input_image = io.BytesIO(f.read())
#----------------------------model button UI-------------------------------------------

col1, col2 = st.columns([0.22,0.65], gap="small")
with col1:
    connectgap_button = st.button("Finish Linework ✍️",  type="primary")
with col2:
        if input_image:
            st.write("###### Press :red['Finish Linework✍️'] to clean up the :blue[image!]")
        else:
            st.write("###### Upload an image in the sidebar to start!")

#-------------------handles running the model------------------------------------------


if connectgap_button and input_image:
    final_image, gap_image = model(input_image)
    st.session_state['nodefault'] = True
elif connectgap_button and input_image is None:
     st.warning("still need an image")

#----------------------------Output image UI-------------------------------------------
if input_image is not None and st.session_state['nodefault'] == True:
    st.image(input_image, caption="original image")
    if gap_image is not None and final_image is not None:
        st.image(gap_image, caption="gaps found")
        st.image(final_image, caption="finalimage")

        
elif input_image is not None and st.session_state['nodefault'] == False:
    st.image(input_image, caption="Sample image")
    if gap_image is not None and final_image is not None:
        st.image(gap_image, caption="gaps found")
        st.image(final_image, caption="finalimage")

st.divider()
#-------------gives link to google drive with more images to try out----------------------
with st.popover(":blue[Want more Sample Images?]"):
    st.link_button("Google Drive Link", "https://drive.google.com/drive/folders/1yR-EXdu_z0q77-Ddt_kMuWTfzgdnyOJo?usp=sharing")





