import logging
import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .code_analyzer import test_python_file
from .code_corrector import correct_python_file
from .general_ai_assistant import GeneralAIAssistant
from .pdf import extract_text_from_pdf, get_pdf_metadata, count_pages

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialisation des assistants
code_assistant = GeneralAIAssistant("Tu es un assistant spécialisé en programmation Python. Tu dois analyser et expliquer le code Python, répondre aux questions sur la syntaxe, les bonnes pratiques et la logique de programmation.")
general_assistant = GeneralAIAssistant("Tu es un assistant général capable de répondre à une grande variété de questions sur différents sujets..")
pdf_assistant = GeneralAIAssistant("Tu es un assistant spécialisé dans l'analyse et l'explication du contenu des PDF. Tu dois répondre aux questions sur le contenu du PDF fourni.")

class ChatMessage(BaseModel):
    message: str
    content: str = ""
    assistant_type: str
# Définition du modèle de données pour les messages du chat


@app.post("/clear_history")
async def clear_history(assistant_type: str):
    try:
        if assistant_type == "code":
            code_assistant.clear_history()
        elif assistant_type == "general":
            general_assistant.clear_history()
        else:
            raise ValueError("Type d'assistant non reconnu")
        return JSONResponse(content={"message": f"Historique de l'assistant {assistant_type} effacé avec succès"})
    except Exception as e:
        logger.error(f"Error in clear_history: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'effacement de l'historique : {str(e)}")
@app.post("/analyze_pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        contents = await file.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name
    
    try:
        pdf_text = extract_text_from_pdf(temp_file_path)
        metadata = get_pdf_metadata(temp_file_path)
        page_count = count_pages(temp_file_path)
        return JSONResponse(content={
            "pdf_text": pdf_text,
            "metadata": metadata,
            "page_count": page_count
        })
    except Exception as e:
        logger.error(f"Error in analyze_pdf: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse du PDF : {str(e)}")
    finally:
        os.unlink(temp_file_path)
pdf_assistant = GeneralAIAssistant("Tu es un assistant spécialisé dans l'analyse et l'explication du contenu des PDF. Tu dois répondre aux questions sur le contenu du PDF fourni.")

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        contents = await file.read()
        temp_file.write(contents)
        temp_file_path = temp_file.name
    try:
        error = test_python_file(temp_file_path)
        
        if error:
            corrected_code = correct_python_file(temp_file_path, error)
            return JSONResponse(content={"error": error, "corrected_code": corrected_code, "original_code": contents.decode()})
        else:
            analysis = "Le code s'est exécuté sans erreur."
            return JSONResponse(content={"error": None, "analysis": analysis, "original_code": contents.decode()})
    except Exception as e:
        logger.error(f"Error in analyze_file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse du fichier : {str(e)}")
    finally:
        os.unlink(temp_file_path)

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    logger.debug(f"Received chat request: {chat_message}")
    try:
        if chat_message.assistant_type == "code":
            assistant = code_assistant
            context = f"Voici le code Python sur lequel porte la question:\n\n{chat_message.content}\n\nQuestion: {chat_message.message}"
        elif chat_message.assistant_type == "general":
            assistant = general_assistant
            context = chat_message.message
        elif chat_message.assistant_type == "pdf":
            assistant = pdf_assistant
            context = f"Voici le contenu du PDF sur lequel porte la question:\n\n{chat_message.content}\n\nQuestion: {chat_message.message}"
        else:
            logger.error(f"Invalid assistant type: {chat_message.assistant_type}")
            raise ValueError("Type d'assistant non reconnu")
        
        logger.debug(f"Using assistant: {assistant.__class__.__name__}")
        logger.debug(f"Context: {context[:100]}...")  # Log only the first 100 characters of the context
        
        response = assistant.get_response(context)
        logger.debug(f"Assistant response: {response[:100]}...")  # Log only the first 100 characters of the response
        
        return JSONResponse(content={"response": response})
    except Exception as e:
        logger.exception(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la réponse : {str(e)}")

# ... (le reste du code reste inchangé)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
