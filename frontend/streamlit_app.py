import streamlit as st
import requests
import tempfile
import os
# Fonction pour effacer l'historique
from streamlit.runtime.scriptrunner import RerunException
from streamlit.runtime.scriptrunner import RerunData
import streamlit as st
import requests
import numpy as np
import sounddevice as sd
import io
import wave
# Configuration de la page Streamlit
st.set_page_config(page_title="Analyseur de Code Python, PDF et Assistant IA", layout="wide")

# Initialisation des variables de session
if 'code' not in st.session_state:
    st.session_state.code = ""
if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {"code": [], "general": [], "pdf": [], "vocal": []}

# Fonction pour envoyer une requête au backend
def send_request(endpoint, data=None, files=None):
    try:
        url = f"http://localhost:8000/{endpoint}"
        if files:
            response = requests.post(url, files=files)
        elif data:
            response = requests.post(url, json=data)
        else:
            response = requests.post(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erreur de communication avec le serveur: {str(e)}")
        return None
def clear_history(assistant_type):
    response = send_request("clear_history", data={"assistant_type": assistant_type})
    if response and response.get('message'):
        st.success(response['message'])
        st.session_state.chat_history[assistant_type] = []
        st.rerun()
    else:
        st.error("Erreur lors de l'effacement de l'historique")
def transcribe_and_translate_page():
    st.title("Transcription et Traduction Audio")
    
    uploaded_file = st.file_uploader("Choisissez un fichier audio", type=["wav", "mp3", "opus"])
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/ogg')
        
        if st.button("Transcrire et Traduire"):
            with st.spinner("Traitement en cours..."):
                files = {'file': uploaded_file}
                response = send_request("transcribe_and_translate", files=files)
                
                if response:
                    st.success("Traitement terminé !")
                    st.write(f"Langue détectée : {response['detected_language']}")
                    st.write("Transcription :")
                    st.write(response['transcription'])
                    st.write("Traduction en français :")
                    st.write(response['french_translation'])
                else:
                    st.error("Une erreur s'est produite lors du traitement.")

# Ajoutez cette nouvelle page à votre dictionnaire de pages
def home_page():
    st.title("🏠 Bienvenue dans notre Application d'Analyse et d'Assistance IA")
    
    # Introduction
    st.markdown("""
    Bienvenue dans notre application révolutionnaire d'analyse et d'assistance IA. 
    Nous sommes ravis de vous offrir une expérience unique combinant analyse de code, 
    traitement de documents et interaction vocale, le tout propulsé par une IA de pointe.
    """)

    # Notre Vision
    st.header("🚀 Notre Vision")
    st.markdown("""
    Nous croyons en un avenir où l'IA est un outil accessible et puissant pour tous. 
    Notre application vise à démocratiser l'accès aux technologies de pointe en IA, 
    permettant à chacun d'améliorer sa productivité et sa compréhension dans divers domaines.
    """)

    # Nos Outils
    st.header("🛠️ Nos Outils")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. 🐍 Analyse de Code Python et Assistant Code")
        st.markdown("""
        - Analyse statique de code Python
        - Détection d'erreurs et suggestions de corrections
        - Assistant IA pour répondre à vos questions sur le code
        """)
        
        st.subheader("2. 📄 Analyse de PDF et Assistant PDF")
        st.markdown("""
        - Extraction de texte et de métadonnées de fichiers PDF
        - Résumé automatique du contenu
        - Assistant IA pour répondre à vos questions sur les documents
        """)
        
        st.subheader("3. 🤖 Assistant Général")
        st.markdown("""
        - IA polyvalente pour répondre à une variété de questions
        - Aide à la recherche et à la résolution de problèmes
        - Suggestions et idées créatives
        """)

    with col2:
        st.subheader("4. 🎙️ Chatbot Vocal")
        st.markdown("""
        - Interface de conversation vocale avec l'IA
        - Transcription automatique de la voix en texte
        - Réponses vocales générées par l'IA
        """)
    # Notre Engagement
    st.header("🌱 Notre Engagement")
    st.markdown("""
    Nous nous engageons à :
    - Fournir des outils IA éthiques et transparents
    - Améliorer continuellement nos modèles et fonctionnalités
    - Protéger la confidentialité et la sécurité de vos données
    - Rester à l'écoute de vos besoins et suggestions
    """)

    # Appel à l'action
    st.header("🚀 Prêt à commencer ?")
    st.markdown("""
    Explorez nos fonctionnalités via la barre latérale et découvrez comment notre IA peut transformer votre travail !
    N'hésitez pas à nous faire part de vos retours pour nous aider à améliorer continuellement notre application.
    """)

    # Bouton pour commencer
    if st.button("Commencer l'exploration"):
        st.session_state.page = "Analyse de Code et Assistant Code"
        st.rerun()
# Fonction générique pour afficher le chat et gérer les questions
def display_chat_and_handle_questions(assistant_type, content=""):
    st.header(f"Assistant {assistant_type.capitalize()}")

    # Créer un conteneur pour l'historique du chat
    chat_container = st.container()

    # Zone de saisie (en bas)
    user_question = st.text_input(f"Poser une question sur {assistant_type}", key=f"input_{assistant_type}")
    send_button = st.button("Envoyer", key=f"send_{assistant_type}_question")

    if send_button and user_question:
        # Ajouter la question de l'utilisateur à l'historique
        st.session_state.chat_history[assistant_type].append(("user", user_question))
        
        # Obtenir la réponse de l'assistant
        with st.spinner(f"L'assistant {assistant_type} réfléchit..."):
            chat_response = send_request("chat", data={
                "message": user_question,
                "content": content,
                "assistant_type": assistant_type
            })
            if chat_response:
                assistant_response = chat_response['response']
                st.session_state.chat_history[assistant_type].append(("assistant", assistant_response))

    # Afficher l'historique du chat dans le conteneur
    with chat_container:
        for role, message in st.session_state.chat_history[assistant_type]:
            with st.chat_message(role):
                st.write(message)

    # Bouton pour effacer l'historique du chat
    if st.button(f"Effacer l'historique du chat {assistant_type}"):
        clear_history(assistant_type)
        raise RerunException(RerunData())
        # Faire défiler automatiquement vers le bas
    st.markdown('<script>window.scrollTo(0,document.body.scrollHeight);</script>', unsafe_allow_html=True)

# Page d'analyse de code et assistant code
def code_analysis_and_assistant_page():
    st.title("Analyse de Code Python et Assistant Code")
    # Analyse de code
    st.header("Analyse de Code")
    uploaded_files = st.file_uploader("Choisissez un ou plusieurs fichiers Python", type="py", accept_multiple_files=True)
    requirements_file = st.file_uploader("Choisissez le fichier requirements.txt", type="txt", accept_multiple_files=False)

    if uploaded_files and requirements_file:
        for uploaded_file in uploaded_files:
            st.write("Fichier chargé :", uploaded_file.name)

        if st.button("Analyser et Corriger"):
            for uploaded_file in uploaded_files:
                with st.spinner(f"Analyse en cours pour {uploaded_file.name}..."):
                    files = {'file': uploaded_file, 'requirements_file': requirements_file}
                    result = send_request("analyze", files=files)

                    if result:
                        st.subheader(f"Résultats pour {uploaded_file.name}")
                        if result.get('error'):
                            st.error("Erreur détectée :")
                            st.code(result['error'])
                            st.write("Code corrigé :")
                            st.code(result['corrected_code'])
                        else:
                            st.success("Aucune erreur détectée.")
                            st.write("Analyse du code :")
                            st.write(result['analysis'])

                        st.session_state.code += f"\n\n# Fichier: {uploaded_file.name}\n{result.get('original_code', '')}"
        # Assistant Code
    if st.session_state.code:
        st.write("Code actuel :")
        st.code(st.session_state.code, language="python")
        display_chat_and_handle_questions("code", st.session_state.code)
    else:
        st.warning("Veuillez d'abord charger et analyser un ou plusieurs fichiers Python pour pouvoir poser des questions sur le code.")

# Page d'assistant général
def assistant_general_page():
    st.title("Assistant Général")
    display_chat_and_handle_questions("general")

def pdf_analysis_and_assistant_page():
    st.title("Analyse de PDF et Assistant PDF")

    # Analyse de PDF
    st.header("Analyse de PDF")
    uploaded_files = st.file_uploader("Choisissez un ou plusieurs fichiers PDF", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.write("Fichier chargé :", uploaded_file.name)

        if st.button("Analyser les PDFs"):
            for uploaded_file in uploaded_files:
                with st.spinner(f"Analyse en cours pour {uploaded_file.name}..."):
                    files = {'file': uploaded_file}
                    result = send_request("analyze_pdf", files=files)

                    if result and result.get('pdf_text'):
                        st.subheader(f"Résultats pour {uploaded_file.name}")
                        st.success("PDF analysé avec succès.")
                        st.session_state.pdf_text = result['pdf_text']
                    else:
                        st.error(f"Erreur lors de l'analyse du PDF {uploaded_file.name}.")
                        st.session_state.pdf_text = ""

        display_chat_and_handle_questions("pdf", st.session_state.pdf_text)
    else:
        st.warning("Aucun PDF n'a été chargé avec succès.")
def voice_chat_page():
    st.title("Chatbot Vocal")
    
    # Créer un conteneur pour l'historique du chat vocal
    chat_container = st.container()
    
    # Afficher l'historique du chat vocal (seulement les réponses de l'assistant)
    with chat_container:
        for role, message in st.session_state.chat_history["vocal"]:
            if role == "assistant":
                with st.chat_message(role):
                    st.write(message)
    
    audio_file = st.file_uploader("Choisissez un fichier audio", type=["wav", "mp3", "ogg", "opus"])
    
    if audio_file is not None:
        st.audio(audio_file)
        
        if st.button("Traiter l'audio"):
            files = [('audio_file', (audio_file.name, audio_file.getvalue(), f'audio/{audio_file.type}'))]
            
            with st.spinner("Traitement en cours..."):
                response = requests.post("http://localhost:8000/voice_chat", files=files)
            
            if response.status_code == 200:
                result = response.json()
                assistant_response = result["original_response"]
                
                # Ajouter seulement la réponse de l'assistant à l'historique
                st.session_state.chat_history["vocal"].append(("assistant", assistant_response))
                
                # Afficher la nouvelle réponse
                with st.chat_message("assistant"):
                    st.write(assistant_response)
            else:
                st.error(f"Erreur: {response.text}")
    
    # Bouton pour effacer l'historique du chat vocal
    if st.button("Effacer l'historique du chat vocal"):
        clear_history("vocal")
# Page À propos
def about_page():
    st.title("ℹ️ À propos de notre Projet IA Innovant")
    
    # Mission
    st.header("🌟 Notre Mission")
    st.markdown("""
    Nous visons à créer un écosystème IA intégré qui autonomise les utilisateurs dans leurs tâches quotidiennes, 
    de l'analyse de code à la compréhension de documents complexes. Notre objectif est de rendre l'IA accessible, 
    utile et transparente pour tous.
    """)

    # Technologie
    st.header("🔬 Technologie de Pointe")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Frontend")
        st.markdown("- Streamlit pour une interface utilisateur réactive et intuitive")
    with col2:
        st.subheader("Backend")
        st.markdown("- FastAPI pour des performances optimales et une scalabilité accrue")
    st.subheader("IA")
    st.markdown("- Modèles de traitement du langage naturel et de la parole à la pointe de la technologie")
    st.markdown("- Intégration de modèles multimodaux pour une compréhension contextuelle riche")

    # Objectifs
    st.header("🎯 Nos Objectifs")
    st.subheader("Court Terme")
    st.markdown("""
    1. Amélioration continue de la précision de nos modèles d'IA
    2. Intégration de nouvelles langues pour la transcription et la traduction
    3. Développement d'une fonctionnalité de génération de code assistée par IA
    """)
    st.subheader("Long Terme")
    st.markdown("""
    - Créer un assistant IA personnalisé adaptable à chaque industrie
    - Développer des capacités d'apprentissage en continu pour une amélioration constante
    - Établir des partenariats stratégiques pour étendre notre portée et notre impact
    """)

    # Innovation
    st.header("💡 Innovation Continue")
    st.markdown("""
    Notre équipe travaille sans relâche sur :
    - L'intégration de modèles d'IA multimodaux pour une compréhension plus riche du contexte
    - Le développement d'une plateforme collaborative basée sur l'IA pour le développement de logiciels
    - L'exploration de l'IA explicable pour renforcer la confiance et la transparence
    """)

    # Collaboration et Open Source
    st.header("🤝 Collaboration et Open Source")
    st.markdown("""
    Nous croyons en la puissance de la communauté. Certains de nos outils sont open source, 
    et nous encourageons activement les contributions externes pour façonner l'avenir de l'IA.
    Rejoignez-nous sur GitHub et participez à notre mission !
    """)

    # Impact Global
    st.header("🌍 Impact Global")
    st.markdown("""
    Notre objectif est de rendre l'IA accessible à tous, indépendamment de l'expertise technique, 
    contribuant ainsi à l'innovation et à la résolution de problèmes à l'échelle mondiale. Nous visons 
    à avoir un impact positif dans des domaines tels que l'éducation, la santé et la recherche scientifique.
    """)

    # Sécurité et Éthique
    st.header("🔒 Sécurité et Éthique")
    st.markdown("""
    La protection des données et l'utilisation éthique de l'IA sont au cœur de notre philosophie. 
    Nous adhérons aux meilleures pratiques en matière de sécurité et de confidentialité, et nous 
    nous engageons à utiliser l'IA de manière responsable et transparente.
    """)

    # L'équipe
    st.header("👥 Notre Équipe")
    st.markdown("""
    Notre équipe diversifiée est composée d'experts en IA, en développement logiciel, en sécurité des données 
    et en expérience utilisateur. Nous sommes unis par notre passion pour l'innovation et notre engagement 
    à créer des solutions IA qui améliorent réellement la vie des gens.
    """)

    # Rejoindre l'aventure
    st.header("🚀 Rejoignez l'Aventure")
    st.markdown("""
    Nous sommes toujours à la recherche de talents passionnés et d'utilisateurs enthousiastes 
    pour façonner l'avenir de l'IA. Que vous soyez développeur, data scientist, designer UX 
    ou simplement passionné par l'IA, il y a une place pour vous dans notre communauté.
    """)

    # Contact
    st.header("📞 Contact")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - 📧 Email : zakariae.yh@gmail.com
        - 💼 LinkedIn : [Zakariae Yahya](https://www.linkedin.com/in/zakariae-yahya/)
        """)
    with col2:
        st.markdown("""
        - 🐙 GitHub : [zakariaeyahya](https://github.com/zakariaeyahya)
        """)

    # Appel à l'action
    st.markdown("""
    Votre feedback est précieux ! N'hésitez pas à nous contacter pour toute suggestion, 
    question ou idée de collaboration. Ensemble, façonnons l'avenir de l'IA !
    """)

    # Bouton de contact
    if st.button("Contactez-nous"):
        st.markdown("📧 Envoyez-nous un email à : zakariae.yh@gmail.com")

# Définition des pages
pages = {
    "🏠 Accueil": home_page,
    "🐍 Analyse de Code et Assistant Code": code_analysis_and_assistant_page,
    "📄 Analyse de PDF et Assistant PDF": pdf_analysis_and_assistant_page,
    "🤖 Assistant Général": assistant_general_page,
    "🎙️ Chatbot Vocal": voice_chat_page,
    "ℹ️ À propos": about_page
}

# Navigation
st.sidebar.title("📌 Navigation")
selection = st.sidebar.radio("Aller à", list(pages.keys()))

# Appel de la fonction correspondant à la page sélectionnée
pages[selection]()

