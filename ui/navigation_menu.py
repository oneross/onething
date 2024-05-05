import streamlit as st
from streamlit_option_menu import option_menu
import yaml

def navigation_intent(current_page):
    if st.session_state['logging_enabled']:
        st.write('Logging enabled')
        st.markdown('### Session State')
        st.write(st.session_state)
    
    intents = st.session_state['intents']
    
    # Ensure that 'intents' is a dictionary before proceeding
    if isinstance(intents, dict):
        menu_options = [details['intent_display'] for key, details in intents.items() if 'intent_display' in details]
        icons = [details['intent_extra_info']['intent_icon'] for key, details in intents.items() if 'intent_extra_info' in details and 'intent_icon' in details['intent_extra_info']]
    else:
        # Fallback or error handling if intents are not in the expected format
        st.error("Error: Intents data is not in the expected format.")
        return None
    
    default_index = current_page
    selected_option = option_menu(None, menu_options, 
                                  icons=icons, 
                                  menu_icon='cast', default_index=default_index, orientation='horizontal')
    
    # Parse through intents to find which key has intent_display that matches selected_option
    for intent, details in intents.items():
        if details.get('intent_display') == selected_option:
            selected_intent = intent
            break

    # Return the intent corresponding to the selected option
    return selected_intent
