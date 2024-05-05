#!/usr/bin/env python3

# Standard Python Imports
import pandas as pd
from datetime import datetime

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shortcuts

from ui.navigation_menu import navigation_intent
from ui.sidebar import render_sidebar
import utils.intents as intents


intents.update_session_intents()

CURRENT_PAGE_INDEX = 1

if 'Collection' not in st.session_state:
    dummy_data = {
        'edited_dt': ['2023-01-01-12-00-00', '2023-01-02-12-00-00', '2023-01-03-12-00-00', '2023-01-04-12-00-00', '2023-01-05-12-00-00'],
        'summary': ['First Entry', 'Second Entry', 'Third Entry', 'Fourth Entry', 'Fifth Entry'],
        'content': [
            'Once upon a time in a land far, far away, there lived a brave knight named Sir Lancelot.',
            'In the heart of the deep forest, the mysterious and wise old wizard Merlin spent his days.',
            'High above the clouds, the fierce dragon Dracarys guarded the ancient castle ruins.',
            'Beneath the ocean waves, the mermaid princess Ariel dreamed of life on land.',
            'In the bustling city of Metropolis, the superhero Clark Kent saved the day from villains.'
        ]
    }
    st.session_state['Collection'] = pd.DataFrame(dummy_data)


render_sidebar()

intent = navigation_intent(CURRENT_PAGE_INDEX)  # Changed to use navigation_intent

st.write(intent)

st.write('Collect Page')


if 'current_content' not in st.session_state:
    st.session_state['current_content'] = ""
current_content = st.text_area("Content", value=st.session_state['current_content'])
if current_content != st.session_state['current_content']:
    st.session_state['current_content'] = current_content

content_editor_ui_left, content_editor_ui_right = st.columns([1, 4])

with content_editor_ui_left:
    st.write("Left")
with content_editor_ui_right:
    selected_option = option_menu(None, ['Load', 'Save', 'Clear', 'Send'], 
        icons=['upload', 'save', 'trash', 'send'], 
        menu_icon='cast', default_index=0, orientation='horizontal')
    

if selected_option == 'Save':
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    new_entry = {
        'datetime': [current_datetime],
        'summary': ['Summary'],
        'content': [st.session_state['current_content']]
    }

    new_entry_df = pd.DataFrame(new_entry)
    st.session_state['Collection'] = pd.concat([st.session_state['Collection'], new_entry_df], ignore_index=True)


collection_df = st.session_state['Collection']
new_collection_df = st.data_editor(collection_df)
if not new_collection_df.equals(collection_df):
    st.session_state['Collection'] = new_collection_df
    st.success('Changes saved successfully!')

#####################
## INTENT HANDLING ## Common to all pages
#####################

intent_expander = st.sidebar.expander('Intents')
shortcut_expander = st.sidebar.expander('Shortcuts', expanded=True)
    

with shortcut_expander:
    intents.render_intents_shortcuts()

intents.handle_intent()

with intent_expander:
    intents.render_intents()