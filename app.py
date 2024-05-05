import diskcache as dc
import time

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shortcuts

from ui.navigation_menu import navigation_intent
from ui.sidebar import render_sidebar
from ui.styles import no_deploy_button
import utils.intents as intents
from agents.openai_agent import OpenaiEditorAgent

import yaml

intents.update_session_intents()

CURRENT_PAGE_TARGET_INTENT = 'navigate_write' # TODO: Make this dynamic
CURRENT_PAGE_INDEX = 0

#######################
## COMMON PAGE SETUP ##
#######################
cache = dc.Cache('tmp')
section_height = cache.get('section_height', 500)


#######################
## UNIQUE PAGE SETUP ##
#######################
editor_height = cache.get('editor_height', 500)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

editor_agent = OpenaiEditorAgent()

####################
## USER INTERFACE ##
####################
st.set_page_config(page_title='Liz Personal Productivity App', layout="wide", page_icon='🧠', initial_sidebar_state='collapsed')

render_sidebar()

fixed = st.container()

with fixed:
    
    ui_menu_intent  = navigation_intent(CURRENT_PAGE_INDEX)
    if ui_menu_intent != CURRENT_PAGE_TARGET_INTENT:
        st.write(ui_menu_intent)
        st.write('triggering intent')
        intents.trigger_intent(ui_menu_intent)

#########################
## UNIQUE PAGE CONTENT ##
#########################


    current_content = st.text_area("Content", value=cache.get('current_content', ''), height=editor_height)
    if current_content != cache.get('current_content', ''):
        cache['current_content'] = current_content

##########
## CHAT ##
##########
scrollable = st.container(height=section_height)


with scrollable:
    st.write('This is srollable')
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

if prompt := st.chat_input("What is up?"):
    
    # Update the chat history with the user's message
    with scrollable:
        st.chat_message('User').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    
    start_time = time.time()  # Start timing the response generation
    
    # Generate and parse response
    result = editor_agent.get_edit_response(cache.get('current_content'), prompt)
    content = result.get('content', '')
    response = result.get('response', 'Error getting response')
    instruction_type = result.get('instruction_type', '')

    response_time = time.time() - start_time  # Calculate the response time
    
    # Save updated content to the session state
    cache.set(current_content, content)
    
    response_with_timing = f"{response} (Response time: {response_time:.2f} seconds)"
    
    with scrollable:
        with st.chat_message('assistant'):
            st.markdown(response_with_timing)

    st.session_state.messages.append({'role': 'assistant', 'content': response_with_timing})






## INTENT HANDLING ## Common to all pages
#####################

intent_expander = st.sidebar.expander('Intents')
shortcut_expander = st.sidebar.expander('Shortcuts', expanded=True)
    

with shortcut_expander:
    intents.render_intents_shortcuts()

intents.handle_intent()

with intent_expander:
    intents.render_intents()