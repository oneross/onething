import streamlit as st
import streamlit_shortcuts
import yaml

#######################################################################
## DEVELOPER_NOTE:                                                   ##
##    You need to edit the bottom three sections to add new intents. ##
##    - Callbacks                                                    ##
##    - Rendering                                                    ##
##    - Intent handling                                              ##
## TODO: Make dynamic                                                ##
#######################################################################
PURGE_INTENTS = False # Provided for early-stage troubleshooting


## Loading and updating intents

def load_intents():
    with open('intents.yml', 'r') as file:
        return yaml.safe_load(file)

def update_session_intents():
    file_intents = load_intents()

    if PURGE_INTENTS:
        st.session_state['intents'] = file_intents
    else:
        if 'intents' not in st.session_state:
            st.session_state['intents'] = file_intents
        elif set(st.session_state['intents']) != set(file_intents):
            st.session_state['intents'] = file_intents

## Intent getting, setting, etc.

def get_intent(intent):
    return st.session_state['intents'][intent]

def intent_state(intent):
    return st.session_state.get('intent_' + intent, False)

def trigger_intent(intent):
    st.session_state['intent_' + intent] = True

def clear_intents_matching(intent_prefix):
    intent_prefix = 'intent_' + intent_prefix
    if st.session_state['logging_enabled']:
        st.write('Clearing intents matching: ' + intent_prefix)
    for intent in st.session_state.keys():
        if intent.startswith(intent_prefix):
            if st.session_state['logging_enabled']:
                st.write('Clearing intent: ' + intent)
            st.session_state[intent] = False

def reset_intents():
    if st.session_state['logging_enabled']:
        st.write('Resetting intents')
    intents = st.session_state['intents']
    for i in intents.keys():
        st.session_state['intent_' + i] = False

## Special functions

def switch_page(page):
    reset_intents()
    st.switch_page(page)

## Callbacks (for Streamlit Shortcuts)
## NOTE: You need to edit these if you create new intents for which you want shortcuts

def write_callback():
    trigger_intent('navigate_write')

def collect_callback():
    trigger_intent('navigate_collect')

def tasks_callback():
    trigger_intent('navigate_tasks')

def preview_callback():
    trigger_intent('navigate_preview')


## Rendering
## NOTE: You need to edit these if you create new intents for which you want shortcuts

def render_intents():
    intents = st.session_state['intents']
    for i in intents.keys():
        st.checkbox(i, key='intent_' + i)

def render_intents_shortcuts():

    intent=get_intent('navigate_write')
    streamlit_shortcuts.button(intent['intent_display'], on_click=write_callback, shortcut=intent['intent_shortcut'])

    intent=get_intent('navigate_collect')
    streamlit_shortcuts.button(intent['intent_display'], on_click=collect_callback, shortcut=intent['intent_shortcut'])

    intent=get_intent('navigate_tasks')
    streamlit_shortcuts.button(intent['intent_display'], on_click=tasks_callback, shortcut=intent['intent_shortcut'])

    intent=get_intent('navigate_preview')
    streamlit_shortcuts.button(intent['intent_display'], on_click=preview_callback, shortcut=intent['intent_shortcut'])

## Intent handling
## NOTE: You need to edit these if you create new intents for which you want shortcuts

def handle_intent():
    
    if intent_state('navigate_write'):
        st.toast('navigate_write')
        switch_page('app.py')
    if intent_state('navigate_collect'):
        st.toast('navigate_collect')
        switch_page('pages/1_Collect.py')
    if intent_state('navigate_tasks'):
        st.toast('navigate_tasks')
        switch_page('pages/2_Tasks.py')
    if intent_state('navigate_preview'):
        st.toast('navigate_preview')
        switch_page('pages/3_Preview.py')

