





class OpenaiEditorAgent:
    def __init__(self):
        from openai import OpenAI
        import os

        # Set up the OpenAI API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI()
        
    def get_edit_response(self, content, prompt):
        # Define the prompt with instructions, as a list of messages
        messages = [
            {'role': 'system', 'content': 'You are an intelligent agent capable of following specific instruction types. Based on the instruction in the PROMPT, edit the CONTENT. Then, determine and respond with the type of instruction. Respond with a JSON object containing: - \'content\': the edited version of CONTENT, if applicable - \'response\': a natural commentary including answers to any queries - \'instruction_type\': the type of instruction processed'},
            {'role': 'user', 'content': prompt},
            {'role': 'user', 'content': content}
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1500
            )

        # Extracting the desired information from the response
        last_response = response['choices'][0]['message']['content']
        
        # Assume last_response is already in JSON format
        return last_response


# Example usage
if __name__ == "__main__":
    agent = OpenaiEditorAgent()
    edited_content = agent.get_edit_response("Your initial content here", "Edit this text to be more concise.")
    print(edited_content)
