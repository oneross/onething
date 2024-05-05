from dotenv import load_dotenv
import os

class OpenaiEditorAgent:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Import OpenAI library and set up the API key
        import openai
        self.openai = openai
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.openai.api_key = self.api_key
    
    def get_edit_response(self, content, prompt):
        full_prompt = f'''
        You are an intelligent agent capable of following specific instruction types. Based on the instruction in the PROMPT, edit the CONTENT. Then, determine and respond with the type of instruction. Respond with a JSON object containing:
        - 'content': the edited version of CONTENT following the instructions in PROMPT, if applicable.
        - 'response': a natural commentary including answers to any queries
        - 'instruction_type': the type of instruction processed

        Instruction types:
        EDIT - Modify text, e.g., remove the last sentence, proofread, make more concise.
        REMEMBER - Record a fact or proposition.
        REMIND_AT_TIME - Remind the user at a specified time.
        REMIND_IN_CONTEXT - Remind the user when relevant in a similar topic conversation.
        NAVIGATE_EDIT - Navigate to a page for editing content.
        NAVIGATE_COLLECT - Navigate to a page for collecting reviews.
        NAVIGATE_PLAN - Navigate to a page for planning tasks and priorities.
        QUERY - Query text, e.g., identify overused words, summarize content, find key points.

        PROMPT:
        {prompt}

        CONTENT:
        {content}
        '''
        response = self.openai.Completion.create(
            engine="text-davinci-003",
            prompt=full_prompt,
            max_tokens=1500
        )
        return response['choices'][0]['text']

# Example usage
if __name__ == "__main__":
    agent = OpenaiEditorAgent()
    edited_content = agent.get_edit_response("Your initial content here", "Edit this text to be more concise.")
    print(edited_content)
