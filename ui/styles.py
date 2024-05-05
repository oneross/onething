import streamlit as st

def no_deploy_button():
    st.markdown("""
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            .stDeployButton {display:none;}
        </style>
        """, unsafe_allow_html=True)
    
## Original
    # st.markdown("""
    #     <style>
    #         .reportview-container {
    #             margin-top: -2em;
    #         }
    #         #MainMenu {visibility: hidden;}
    #         .stDeployButton {display:none;}
    #         footer {visibility: hidden;}
    #         #stDecoration {display:none;}
    #     </style>
    #     """, unsafe_allow_html=True)