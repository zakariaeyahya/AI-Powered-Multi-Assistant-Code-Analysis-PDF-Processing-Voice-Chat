import torch
import torchaudio
import numpy as np
from transformers import SeamlessM4Tv2Model, AutoProcessor
import logging
import time
from tqdm import tqdm

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SeamlessModel:
    def __init__(self):
        logger.info("Initialisation du SeamlessModel")
        self.device = torch.device("cpu")
        logger.info(f"Utilisation du device: {self.device}")

        logger.info("Début du chargement du processeur")
        start_time = time.time()
        try:
            self.processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
            logger.info(f"Processeur chargé en {time.time() - start_time:.2f} secondes")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du processeur: {e}")
            raise

        logger.info("Début du chargement du modèle")
        start_time = time.time()
        try:
            # Utilisation de tqdm pour afficher une barre de progression
            with tqdm(total=1, desc="Chargement du modèle") as pbar:
                self.model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large", 
                                                                local_files_only=False)
                pbar.update(1)
            logger.info(f"Modèle chargé en {time.time() - start_time:.2f} secondes")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            raise

        logger.info("Initialisation du SeamlessModel terminée")
        logger.info(f"Taille du modèle: {sum(p.numel() for p in self.model.parameters())} paramètres")

    def clean_output(self, text):
        return text.replace('</s>', '').strip()

    def speech_to_text_with_lang_detection(self, audio_array):
        try:
            inputs = self.processor(audios=audio_array, return_tensors="pt", sampling_rate=16000).to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(**inputs, generate_speech=False)
            token_ids = outputs.sequences[0].cpu().tolist()
            transcription = self.clean_output(self.processor.decode(token_ids))
            
            # Language detection (simplified for this example)
            detected_lang = transcription.split()[0] if transcription else "unk"
            clean_transcription = ' '.join(transcription.split()[1:])
            
            return clean_transcription, detected_lang
        except Exception as e:
            logger.error(f"Error in speech_to_text_with_lang_detection: {str(e)}")
            raise

    def translate_text(self, text, tgt_lang):
        try:
            inputs = self.processor(text=text, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(**inputs, tgt_lang=tgt_lang, generate_speech=False)
            token_ids = outputs.sequences[0].cpu().tolist()
            return self.clean_output(self.processor.decode(token_ids))
        except Exception as e:
            logger.error(f"Error in translate_text: {str(e)}")
            raise
