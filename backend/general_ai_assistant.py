import logging
import os
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

logger = logging.getLogger(__name__)

class GeneralAIAssistant:
    def __init__(self, description: str = "Tu es un assistant IA général."):
        os.environ["GROQ_API_KEY"] = "api_groq"#remplacer par votre api
        self.groq_api_key=os.environ["GROQ_API_KEY"]
        if not self.groq_api_key:
            raise ValueError("La clé API Groq n'est pas définie. Utilisez os.environ['GROQ_API_KEY'] = 'votre_clé_api' pour la définir.")
        
        self.llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.7, groq_api_key=self.groq_api_key)
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
        self.description = description
        logger.info(f"GeneralAIAssistant initialized with description: {description}")

    def get_response(self, user_input: str) -> str:
        try:
            context = f"{self.description}\n\nQuestion de l'utilisateur : {user_input}"
            response = self.conversation.predict(input=context)
            logger.info("Response generated successfully")
            return response
        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}", exc_info=True)
            return f"Erreur lors de la génération de la réponse : {str(e)}"
