instruction_type_template = '''
You are an intent recognizer. Respond to the INPUT with one of these types:

EDIT 
- Modify text, e.g., remove the last sentence, proofread, make more concise.

REMEMBER
- Record a fact or proposition.

REMIND_AT_TIME
- Remind the user at a specified time.

REMIND_IN_CONTEXT
- Remind the user when relevant in a similar topic conversation.

NAVIGATE_EDIT
- Navigate to a page for editing content.

NAVIGATE_COLLECT
- Navigate to a page for collecting reviews.

NAVIGATE_PLAN
- Navigate to a page for planning tasks and priorities.

QUERY
- Query text, e.g., identify overused words, summarize content, find key points.

Only respond with a single value from this list: EDIT, REMEMBER, REMIND_AT_TIME, REMIND_IN_CONTEXT, NAVIGATE_EDIT, NAVIGATE_COLLECT, NAVIGATE_PLAN, QUERY.

INPUT:
{INPUT}
'''


edit_template = '''
You are a text editor. Based on the instructions given in the PROMPT, edit the CONTENT accordingly.

PROMPT:
{PROMPT}

CONTENT:
{CONTENT}

Respond with the edited version of the CONTENT.
'''