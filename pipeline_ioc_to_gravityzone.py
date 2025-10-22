import subprocess
import logging
import os
from datetime import datetime


"""3 scripts, une pipeline.
plutôt simple, pas trop fancy, à part le run_step qui a un format agréable.
pas trop de phase de validation des étapes, faudrait en rajouter. probablement.
pareil, pas de TO, pas de retries, pas code de sortie, pas de cross-plateforme(probablement?), pas testé, pas de bras, pas de chocolat, bref, rien."""


# Configuration des logs
logging.basicConfig(
    filename="pipeline_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_step(description, command):
    logging.info(f"Début de l'étape : {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logging.info(f"Succès : {description}")
        logging.debug(f"Sortie : {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Échec : {description}")
        logging.error(f"Code retour : {e.returncode}")
        logging.error(f"Erreur : {e.stderr}")
        raise

def main():
    logging.info("=== DÉBUT DE LA PIPELINE IoC → GravityZone ===")

    # étape 1 : récupération des IoCs depuis ThreatFox
    try:
        run_step(
            "Récupération des IoCs depuis ThreatFox",
            "python3 threatfox_query_recent-iocs.py $(echo $GZ_API_KEY) 1 > Import_IoC_Threatfox.json"   # vraiment pas sûr pour le $(echo ...)
        )
    except Exception:
        logging.error("Arrêt de la pipeline suite à une erreur dans la récupération des IoCs.")
        return

    # étape 2 : filtrage (je sais pas si je met "hash" ou "hashes" un peu partout dans le reste du code, dans le doute je met les deux)
    try:
        run_step(
            "Filtrage des hashes",
            "python3 threatfox_filter_hashes.py"
        )
    except Exception:
        logging.error("Arrêt de la pipeline suite à une erreur dans le filtrage des hashes.")
        return

    # étape 3 : envoi sur l'API gravityzone
    try:
        run_step(
            "Envoi des hashes à GravityZone",
            "python3 send_to_gravityzone.py"
        )
    except Exception:
        logging.error("Arrêt de la pipeline suite à une erreur dans l'envoi à GravityZone.")
        return
    logging.info("=== FIN DE LA PIPELINE IoC → GravityZone ===")

if __name__ == "__main__":
    main()

    """Franchement, sans mentir, c'est vraiment pas ouf.
    d'ailleurs faudrait voir pour faire des fonctions, parce que là c'est vraiment du copié-collé de scripts.
    après c'est pas comme si c'etait pas le cas depuis le début, mais y'a du potentiel. probablement."""