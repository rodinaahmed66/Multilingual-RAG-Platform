import logging
from google import genai
from google.genai import types
from ..LLMInterface import LLMInterface
from ..LLMEnums import GoogleEnums

class GoogleProvider(LLMInterface):

    def __init__(self,api_key:str,
                 default_input_max_characters :int=1000,
                 default_generation_output_tokens :int=1000,
                 default_generation_temperature:float=0.1):
        
        self.api_key=api_key
        self.default_input_max_characters=default_input_max_characters
        self.default_generation_output_tokens=default_generation_output_tokens
        self.default_generation_temperature=default_generation_temperature

        self.generation_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None

        self.client=genai.Client(api_key=self.api_key)

        self.logger=logging.getLogger(__name__)
        self.enums=GoogleEnums
    
    def set_generation_model(self,model_id:str):
        self.generation_model_id=model_id
    
    def set_embedding_model(self,model_id:str,
                            embedding_size:int):
        
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size
    
    def generate_text(self,prompt:str,chat_history:list=[],max_output_tokens:int=None,
                      temperature:float  =None):
        
        if not self.client:
            return self.logger.error("Google client was not set")
        
        if not self.generation_model_id:
            return self.logger.error("Embedding model id of Google is not exist")
        
        max_output_tokens=max_output_tokens if max_output_tokens else self.default_generation_output_tokens
        temperature=temperature if temperature else self.default_generation_temperature

        chat_history.append(
                self.construct_prompt(prompt=prompt,
                role=GoogleEnums.USER.value
            ))
        
        response=self.models.generate_content(
            model=self.generation_model_id,
            contents=self.process_text(prompt),
            config=types.GenerateContentConfig(
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        system_instruction=chat_history
        )
        )

        if not response or len(response.text)==0:
             self.logger.error("Error in Generating Text from Google")
             return None 
        
        return response.text
        
    def embed_text(self,text:str,document_type:str=None):

        if not self.client:
            self.logger.error("Google client was not set")
            return None
            
        if not self.embedding_model_id:
            self.logger.error("Embedding model for Google client was not set")
            return None  
            
        response = self.client.models.embed_content(
        model=self.embedding_model_id,
        contents=[self.process_text(text)]
        )

        return response.embeddings[0].values
    
    def construct_prompt(self,prompt:str,role:str):
         return{
              "role":role,
              "text":prompt
         }
    
    def process_text(self,text:str):
         return text[:self.default_input_max_characters].strip()
