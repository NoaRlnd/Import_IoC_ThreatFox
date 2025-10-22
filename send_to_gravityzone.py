import json
import os
import base64
import requests
import logging
from dotenv import load_dotenv


"""Comme le nom l'indique très clairement, il prends les IoCs filtrés et les envoie à gravityzone.
beaucoup de soucis à gérer ici, déjà il est pas testé donc aucune idée si ça marche.

ensuite gros problèmes de querry rate limit de l'API gravityzone, c'est un truc genre 10 requêtes minute donc gaffe au timeout qu'on peut se prendre.
en parlant de timout, faudrait gérer les interactions réseau, ajouter retries, timeouts, codes de sorties, tout ça.
TRES IMPORTANT de faire un mode test qui envoie peu ou rien puisque 2000 IoCs à chaque fois ils vont commencer à nous en vouloir.
tout en décallant les envois dans le temps, genre 6 par minute pour simplifier la gestion du rate limit, enfin probablement.

bien valider le format du payload avant envoi, sinon on va probablement prendre, au pire, des erreurs silencieuses.
ensuite faut voir pour les doublons mais aucune idée de comment faire ça proprement quand on les envoie en décalé et tout les jours.
peut-être garder une bdd locale des hashes ? mais ca va être lourd très vite et très fort tout en consommant de la ressource, et fort en plus."""


# pour charger les variables d'environnement
load_dotenv()

# logique
api_key = os.getenv("GZ_API_KEY")
api_url = os.getenv("GZ_API_URL")

# là c'est la création du fichier des logs. Faut que je regarde sur internet si on peut le faire en .log au lieu de .txt
logging.basicConfig(filename="log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# la vérification des variables d'environnement c'est cool pour le genre de personne qui lit pas les README si on prend mon repo sur github
if not api_key or not api_url:
    logging.error("Clé API ou URL manquante dans le fichier .env.")
    exit()

try:
    # encodage de l'authentification en base64 comme le veut l'API gravityzone
    encoded_auth = base64.b64encode((api_key + ":").encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    }

    # charge du payload JSON
    with open("filtered_hashes_for_gravityzone.json", "r", encoding="utf-8") as f:
        payload = json.load(f)

    #  pas compris mais c'est le format JSON-RPC de la doc
    rpc_payload = {
        "jsonrpc": "2.0",
        "method": "addToBlocklist",
        "params": payload,
        "id": "1"
    }

    # envoi requête
    response = requests.post(api_url, headers=headers, json=rpc_payload)

    # un des rare log du script 
    if response.status_code == 200:
        logging.info("Envoi réussi vers GravityZone.")
        logging.info(f"Réponse : {response.json()}")
    else:
        logging.error(f"Échec de l'envoi. Code : {response.status_code}")
        logging.error(f"Réponse : {response.text}")

except Exception as e:
    logging.exception(f"Erreur lors de l'envoi : {e}")