import diskcache as dc

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shortcuts

from ui.navigation_menu import navigation_intent
from ui.sidebar import render_sidebar
import utils.intents as intents

intents.update_session_intents()


CURRENT_PAGE_TARGET_INTENT = 'navigate_preview'
CURRENT_PAGE_INDEX = 3

#######################
## COMMON PAGE SETUP ##
#######################
cache = dc.Cache('tmp')
section_height = cache.get('section_height', 500)



#######################
## UNIQUE PAGE SETUP ##
#######################


####################
## USER INTERFACE ##
####################
st.set_page_config(layout="wide", page_icon='🧠', initial_sidebar_state='collapsed')

render_sidebar() # Common Sidebar Elements


ui_menu_intent  = navigation_intent(CURRENT_PAGE_INDEX)
if ui_menu_intent != CURRENT_PAGE_TARGET_INTENT:
    intents.trigger_intent(ui_menu_intent)

#########################
## UNIQUE PAGE CONTENT ##
#########################



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