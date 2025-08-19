from openai import OpenAI
import mysql.connector as mysql
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Récupération de la clé API
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Connexion MySQL
connexion = mysql.connect(
    host='localhost',
    user='root',
    password='example',
    database='cgvbot',
    port=3306
)
curseur = connexion.cursor()

def ask_openai(question):
    response = client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=[
            {"role": "system", "content": "Tu es EcomLegal, assistant CGV expert."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def log_to_db(prompt, response):
    statut = "1"  # <== chaîne compatible VARCHAR
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requete = """
        INSERT INTO echanges (conversation, prompt, reponse, statut, date)
        VALUES (%s, %s, %s, %s, %s)
    """
    valeurs = (1, prompt, response, statut, date)
    curseur.execute(requete, valeurs)
    connexion.commit()

try:
    while True:
        question = input("Votre question : ")
        if question.lower() == 'exit':
            break
        response = ask_openai(question)
        print("EcomLegal :", response)
        log_to_db(question, response)
finally:
    curseur.close()
    connexion.close()
