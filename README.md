<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assistant IA Multifonction</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        a {
            color: #3498db;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        .document-container {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="document-container">
        <div class="document">
            <div class="document-header">
                <h1>Assistant IA Multifonction</h1>
                <!-- Vous pouvez ajouter une image de bannière ici si vous en avez une -->
            </div>
            <div class="document-content">
                <h2>Description</h2>
                <p>Ce projet est une application d'assistant IA multifonction qui combine l'analyse de code Python, le traitement de documents PDF, un assistant général et un chatbot vocal. L'application utilise une interface utilisateur Streamlit et un backend FastAPI, intégrant des modèles d'IA avancés pour fournir une assistance intelligente dans divers domaines.</p>
                
                <h2>Table des matières</h2>
                <ul>
                    <li><a href="#fonctionnalités">Fonctionnalités</a></li>
                    <li><a href="#technologies-utilisées">Technologies utilisées</a></li>
                    <li><a href="#configuration-et-démarrage">Configuration et Démarrage</a></li>
                    <li><a href="#contribution">Contribution</a></li>
                    <li><a href="#licence">Licence</a></li>
                </ul>
                
                <h2 id="fonctionnalités">Fonctionnalités</h2>
                <ul>
                    <li><strong>Analyse de Code Python et Assistant Code :</strong>
                        <p>L'application permet d'analyser le code Python, de détecter et corriger les erreurs, et de répondre aux questions relatives au code.</p>
                    </li>
                    <li><strong>Analyse de PDF et Assistant PDF :</strong>
                        <p>L'utilisateur peut extraire du texte et des métadonnées de fichiers PDF, obtenir des résumés automatiques et poser des questions sur le contenu des documents.</p>
                    </li>
                    <li><strong>Assistant Général :</strong>
                        <p>Une IA polyvalente capable de répondre à une variété de questions, d'aider à la recherche et à la résolution de problèmes, et de fournir des suggestions créatives.</p>
                    </li>
                    <li><strong>Chatbot Vocal :</strong>
                        <p>Une interface de conversation vocale permettant la transcription automatique de la voix en texte et la génération de réponses vocales.</p>
                    </li>
                </ul>
                
                <h2 id="technologies-utilisées">Technologies Utilisées</h2>
                <h3>Backend</h3>
                <ul>
                    <li><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python"> : Langage de programmation principal</li>
                    <li><img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"> : Framework Python pour la création d'API RESTful</li>
                    <li><img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"> : Framework Python pour la création d'applications web interactives</li>
                    <li><img src="https://img.shields.io/badge/PyPDF2-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="PyPDF2"> : Bibliothèque pour l'extraction de texte à partir de fichiers PDF</li>
                    <li><img src="https://img.shields.io/badge/Transformers-FF9900?style=for-the-badge&logo=transformers&logoColor=white" alt="Transformers"> : Bibliothèque pour les modèles de traitement du langage naturel (NLP)</li>
                    <li><img src="https://img.shields.io/badge/LangChain-00BFFF?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"> : Bibliothèque pour construire des applications d'intelligence artificielle conversationnelle</li>
                </ul>
                
                <h3>Modèles de Langage Pré-entraînés</h3>
                <ul>
                    <li><img src="https://img.shields.io/badge/GPT--3-412991?style=for-the-badge&logo=openai&logoColor=white" alt="GPT-3"> : Modèle de langage avancé pour la génération de texte</li>
                </ul>
                
                <h2 id="configuration-et-démarrage">Configuration et Démarrage</h2>
                <ol>
                    <li>Clonez le dépôt GitHub :
                        <pre><code>git clone https://github.com/votre-utilisateur/assistant-ia-multifonction.git</code></pre>
                    </li>
                    <li>Créez et activez un environnement virtuel Python :
                        <pre><code>cd assistant-ia-multifonction
python -m venv venv
source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`</code></pre>
                    </li>
                    <li>Installez les dépendances requises :
                        <pre><code>pip install -r requirements.txt</code></pre>
                    </li>
                    <li>Configurez les variables d'environnement :
                        <pre><code>export GROQ_API_KEY=votre_clé_api_groq</code></pre>
                    </li>
                    <li>Démarrez l'application :
                        <pre><code>streamlit run app.py</code></pre>
                    </li>
                </ol>
                <p>Accédez à l'application Streamlit via votre navigateur à l'adresse <a href="http://localhost:8501">http://localhost:8501</a>.</p>
                
                <h2 id="contribution">Contribution</h2>
                <p>Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou à soumettre des pull requests si vous avez des suggestions d'amélioration ou si vous avez identifié des bugs.</p>
                
                <h2 id="licence">Licence</h2>
                <p>Ce projet est sous licence MIT. Voir le fichier <code>LICENSE</code> pour plus de détails.</p>
                
                <h2>Contact</h2>
                <ul>
                    <li>Email : <a href="mailto:zakariae.yh@gmail.com">zakariae.yh@gmail.com</a></li>
                    <li>LinkedIn : <a href="https://www.linkedin.com/in/zakariae-yahya/">Zakariae Yahya</a></li>
                    <li>GitHub : <a href="https://github.com/zakariaeyahya">zakariaeyahya</a></li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
