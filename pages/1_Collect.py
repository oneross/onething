import diskcache as dc
import pyperclip
import pytesseract
from PIL import Image
import io

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_shortcuts

from ui.navigation_menu import navigation_intent
from ui.sidebar import render_sidebar
import utils.intents as intents

intents.update_session_intents()

CURRENT_PAGE_TARGET_INTENT = 'navigate_collect' # TODO: Make this dynamic
CURRENT_PAGE_INDEX = 1

#######################
## COMMON PAGE SETUP ##
#######################
cache = dc.Cache('tmp')
section_height = cache.get('section_height', 500)


#######################
## UNIQUE PAGE SETUP ##
#######################
import pandas as pd
from datetime import datetime

if 'Collection' not in cache:
    dummy_data = {
        'datetime': ['2023-01-01-12-00-00', '2023-01-02-12-00-00', '2023-01-03-12-00-00', '2023-01-04-12-00-00', '2023-01-05-12-00-00'],
        'content': [
            'Once upon a time in a land far, far away, there lived a brave knight named Sir Lancelot.',
            'In the heart of the deep forest, the mysterious and wise old wizard Merlin spent his days.',
            'High above the clouds, the fierce dragon Dracarys guarded the ancient castle ruins.',
            'Beneath the ocean waves, the mermaid princess Ariel dreamed of life on land.',
            'In the bustling city of Metropolis, the superhero Clark Kent saved the day from villains.'
        ]
    }
    cache['Collection'] = pd.DataFrame(dummy_data)

# def render_collection_row(row):


####################
## USER INTERFACE ##
####################
st.set_page_config(layout="wide", page_icon='🧠', initial_sidebar_state='collapsed')

render_sidebar() # Common Sidebar Elements

fixed = st.container()

with fixed:
    ui_menu_intent  = navigation_intent(CURRENT_PAGE_INDEX)
    if ui_menu_intent != CURRENT_PAGE_TARGET_INTENT:
        intents.trigger_intent(ui_menu_intent)

#########################
## UNIQUE PAGE CONTENT ##
#########################

    clipboard_content = pyperclip.paste()
    current_content = cache.get('current_content', '')

    if clipboard_content and clipboard_content != current_content:
        ## TODO: Actually make recognize image.
        if clipboard_content.startswith(('http', 'https')) and clipboard_content.endswith(('.png', '.jpg', '.jpeg')):
            st.info('Image in clipboard')
            image_response = requests.get(clipboard_content)
            image = Image.open(io.BytesIO(image_response.content))
            st.image(image, caption='Clipboard Image')
            if st.button('Extract text from image'):
                extracted_text = pytesseract.image_to_string(image)
                pyperclip.copy(extracted_text)
                st.success('Text extracted and copied to clipboard')
        else:
            # Save current content to collection if it's not empty
            if current_content:
                current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                new_entry = {
                    'datetime': [current_datetime],
                    'content': [current_content]
                }
                new_entry_df = pd.DataFrame(new_entry)
                collection_df = cache.get('Collection', pd.DataFrame())
                cache['Collection'] = pd.concat([new_entry_df, collection_df], ignore_index=True)
            
            # Load new text content from clipboard into current content
            cache['current_content'] = clipboard_content
            st.rerun()

    current_content = st.text_area("Content", value=cache.get('current_content', ''))
    if current_content != cache.get('current_content', ''):
        cache['current_content'] = current_content

    content_editor_ui_left, content_editor_ui_right = st.columns([1, 6])

    with content_editor_ui_left:
        character_count = len(current_content)
        word_count = len(current_content.split())
        approx_token_count = int(word_count * 0.75)
        if character_count > 0:
            st.markdown(f't{approx_token_count} w{word_count}c{character_count}')

    with content_editor_ui_right:
        selected_option = option_menu(None, ['Edit', 'Save', 'Load', 'Clear', 'All', 'Swap', 'Trash'], 
            icons=['pencil', 'save', 'upload', 'app', 'check-square', 'arrow-down-up', 'trash'], 
            menu_icon='cast', default_index=0, orientation='horizontal')
        
        intents.clear_intents_matching('collection_editor_')
        intents.trigger_intent('collection_editor_' + selected_option.lower())

        if st.session_state['logging_enabled']: 
            st.markdown('### Intents')
            st.markdown(f'collection_editor_edit: {intents.intent_state("collection_editor_edit")}')
            st.markdown(f'collection_editor_save: {intents.intent_state("collection_editor_save")}')
            st.markdown(f'collection_editor_load: {intents.intent_state("collection_editor_load")}')
            st.markdown(f'collection_editor_clear: {intents.intent_state("collection_editor_clear")}')

## SAVE ##
if intents.intent_state('collection_editor_save') and cache.get('current_content', '') != '':
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    new_entry = {
        'datetime': [current_datetime],
        'content': [cache.get('current_content')]
    }

    new_entry_df = pd.DataFrame(new_entry)
    cache['Collection'] = pd.concat([new_entry_df, cache['Collection']], ignore_index=True)
    cache.set('current_content', '')
        

collection_df = cache['Collection']
collection_df.insert(0, 'order', range(0, len(collection_df)))
collection_df.insert(0, 'act', False) ## TODO: something here for select all

new_collection_df = st.data_editor(collection_df, 
                                   hide_index=True, 
                                   use_container_width=False,
)

## SWAP ##
if intents.intent_state('collection_editor_swap'):
    # Get rows where 'act' is True
    active_rows = new_collection_df[new_collection_df['act'] == True]
    if len(active_rows) == 2:
        # Get the indices of the rows to swap
        idx1, idx2 = active_rows.index
        # Swap the 'order' values
        new_collection_df.at[idx1, 'order'], new_collection_df.at[idx2, 'order'] = new_collection_df.at[idx2, 'order'], new_collection_df.at[idx1, 'order']

## TRASH ##
if intents.intent_state('collection_editor_trash'):
    # Remove rows from new_collection_df where 'act' is True
    intents.clear_intents_matching('collection_editor_trash')
    new_collection_df = new_collection_df[new_collection_df['act'] == False]
    stripped_new_collection_df = new_collection_df.drop(columns=['act'])
    cache['Collection'] = stripped_new_collection_df
    
## LOAD ##
if intents.intent_state('collection_editor_load'):
    loaded_content = new_collection_df[new_collection_df['act'] == True]['content'].str.cat(sep='\n')
    new_collection_df['act'] = False
    st.session_state['current_content'] = loaded_content
    cache['current_content'] = loaded_content

## CLEAR ##
## set act = False for all rows in new_collection_df
new_collection_df['act'] = False

## ALL ##
## set act = True for all rows in new_collection_df
new_collection_df['act'] = True

stripped_new_collection_df = new_collection_df.sort_values(by='order', ascending=True).drop(columns=['act', 'order'])

if not stripped_new_collection_df.equals(collection_df):
    cache['Collection'] = stripped_new_collection_df
    st.toast('Changes saved successfully!')

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