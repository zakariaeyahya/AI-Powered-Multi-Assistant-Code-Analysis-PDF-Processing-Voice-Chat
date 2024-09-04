import logging
import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .code_analyzer import test_python_file
from .code_corrector import correct_python_file
from .general_ai_assistant import GeneralAIAssistant

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Initialize the AI assistant
assistant = GeneralAIAssistant()

class ChatMessage(BaseModel):
    message: str

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
            return JSONResponse(content={"error": error, "corrected_code": corrected_code})
        else:
            analysis = "Le code s'est exécuté sans erreur."
            return JSONResponse(content={"error": None, "analysis": analysis})
    except Exception as e:
        logger.error(f"Error in analyze_file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse du fichier : {str(e)}")
    finally:
        os.unlink(temp_file_path)

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        response = assistant.get_response(chat_message.message)
        return JSONResponse(content={"response": response})
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la réponse : {str(e)}")

@app.get("/")
async def root():
    return {"message": "Bienvenue dans l'API d'analyse de code Python et d'assistant IA"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
