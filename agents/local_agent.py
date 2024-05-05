class LocalEditorAgent:
    def __init__(self):
        from langchain_community.llms import Ollama
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        from agents.prompt_templates import instruction_type_template, edit_template
        
        self.Ollama = Ollama
        self.PromptTemplate = PromptTemplate
        self.LLMChain = LLMChain
        self.instruction_type_template = instruction_type_template
        self.edit_template = edit_template

    def get_instruction_type(self, input):
        llm = self.Ollama(model="phi3")
        prompt = self.PromptTemplate(input_variables=['INPUT'], template=self.instruction_type_template)
        chain = self.LLMChain(llm=llm, prompt=prompt)
        result = chain.run({'INPUT': input})
        return result

    def get_edited_content(self, prompt, content):
        llm = self.Ollama(model="phi3")
        prompt = self.PromptTemplate(input_variables=['PROMPT', 'CONTENT'], template=self.edit_template)
        chain = self.LLMChain(llm=llm, prompt=prompt)
        result = chain.run({'PROMPT': prompt, 'CONTENT': content})
        return result

    def get_edit_response(self, content, prompt):
        instruction_type = self.get_instruction_type(prompt)
        if instruction_type == 'EDIT':
            edited_content = self.get_edited_content(prompt, content)
        else:
            edited_content = content

        rd = {'content': edited_content,
              'response': f'You said: {prompt} which was a {instruction_type} with content: {content}',
              'instruction_type': instruction_type,
              }
        
        return rd

