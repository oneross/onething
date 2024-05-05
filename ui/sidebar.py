import diskcache as dc

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shortcuts

from ui.styles import no_deploy_button

cache = dc.Cache('tmp')




def render_sidebar():
    ## Universal
    no_deploy_button()

    ## Editor Height callbacks
    def update_slider_editor_height():
        st.session_state.ehs = st.session_state.ehn
    def update_numeric_editor_height():
        st.session_state.ehn = st.session_state.ehs

    ## Section Height callbacks
    def update_slider_section_height():
        st.session_state.shs = st.session_state.shn
    def update_numeric_section_height():
        st.session_state.shn = st.session_state.shs

    ## Cache
    default_editor_height = cache.get('editor_height', 300)
    default_section_height = cache.get('section_height', 800)
    # TODO: Add agent default and cache retrievals
    
    with st.sidebar:

        ## Token
        auth_url = 'FAKEIT' # TODO
        st.markdown(f'[Click here for token]({auth_url})')
        jwt_token = st.text_input('Token', value='')
        
        with st.expander('Settings', expanded=False):

            ## UI Setting
            st.markdown('## UI Settings')

            ## Editor Height
            st.markdown('Editor Height')
            ehl, ehr = st.columns([0.8, 0.2])
            ehn = ehr.number_input(label='Editor Height Numeric', label_visibility='collapsed', value=default_editor_height, key='ehn', on_change=update_slider_editor_height)
            editor_height = ehl.slider(label='Editor Height Slider', label_visibility='collapsed', min_value=100, max_value=800, value=ehn, key='ehs', on_change=update_numeric_editor_height)
        
            ## Section Height
            st.markdown('Section Height')
            shl, shr = st.columns([0.8, 0.2])
            shn = shr.number_input('Section Height Numberic', label_visibility='collapsed', value=default_section_height, key='shn', on_change=update_slider_section_height)
            section_height = shl.slider('Section Height Slider', label_visibility='collapsed', min_value=100, max_value=1600, value=shn, key='shs', on_change=update_numeric_section_height)

            if editor_height != default_editor_height or section_height != default_section_height:
                cache.set('editor_height', editor_height)
                cache.set('section_height', section_height)

            ## Agent Settings
            st.markdown('---')
            st.markdown('## Agent Settings')
            env = st.text_input('Environment', value='')
            editor_agent_id = st.text_input('Editor Agent ID', value='')
            document_agent_id = st.text_input('Document Agent ID', value='')
            coach_agent_id = st.text_input('Coach Agent ID', value='')
            summarizer_agent_id = st.text_input('Summarizer Agent ID', value='')
            large_model_agent_id = st.text_input('Large Model Agent ID', value='')
            fast_agent_id = st.text_input('Fast Agent ID', value='')
            local_model_agent_id = st.text_input('Local Model Agent ID', value='')

            ## Others
            st.markdown('---')
            st.markdown('## Debugging')

            view_session_state = st.checkbox('View Session State', value=False)
            view_cache = st.checkbox('View Cache', value=False)

            logging_enabled = st.checkbox('Enable Logging', value=cache.get('logging_enabled', False))
            cache.set('logging_enabled', logging_enabled)
            st.session_state['logging_enabled'] = logging_enabled

        if view_session_state:
            st.markdown('---')
            st.markdown('## Session State')
            st.write(st.session_state)

        if view_cache:
            st.markdown('---')
            st.markdown('## Cache Viewer')
            view_contents = st.checkbox('View Contents')
            show_delete = st.checkbox('Allow Deletes')
            with st.expander("Cache", expanded=True):
                for item in cache:
                    st.markdown('### ' + item)
                    if view_contents:
                        st.write(cache[item])
                    if show_delete:
                        if st.button('delete_'+item):
                            cache.delete(item)
