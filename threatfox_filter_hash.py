import json

"""Script qui filtre les IoCs de type hash depuis le fichier JSON brut (de base) exporté de ThreatFox
et les enregistre dans un nouveau fichier JSON formaté pour GravityZone.
donc il lit le fichier 'Import_IoC_Threatfox.json' et écrit dans 'filtered_hashes_for_gravityzone.json' 
et pour l'instant ne gère que les hashes de type sha256, sha1 et md5 parce que gravityzone ne gère que ces types de hash.
dans le futur on pourrait ajouter d'autres types d'IoCs comme les domaines, les URLs, et éventuellement les adresses IP.
mais ca dépend vachement de gravityzone.
par contre ce qui dépend moins de gravityzone c'est le payload qu'on envoie. (voir la doc 'AddToBlocklist' de l'API gravityzone)
pour l'instant il est trop light, ce serait bien d'ajouter des champs comme 'expiration_date'(pour vraiment les expirer), 'comment', 'source', etc.
aussi il faut ABSOLUMENT voir pour éviter les doublons, parce que il y a déjà beaucoup de transferts d'IoCs vers gravityzone avec ce script.
et en plus on va répéter ce script quotidiennement dans un pipeline donc il y a une marge d'erreur puissante, probablement.
en tout cas ce script là est testé et ca marche."""

# types de hash valides et leur correspondance au format de l'API GravityZone
valid_hash_types = {
    "sha256_hash": "sha256",
    "sha1_hash": "sha1",
    "md5_hash": "md5"
}

# quand ça charge le fichier JSON brut
try:
    with open("Import_IoC_Threatfox.json", "r", encoding="utf-16") as infile:            # oui, c'est de l'utf-16, aucune idée pourquoi
        data = json.load(infile)
        print("Données chargées avec succès.")                                           # à un moment faudrait ajouter des logs plus avancés
except FileNotFoundError:
    print("Erreur : le fichier Import_IoC_Threatfox.json est introuvable.")
    exit()
except json.JSONDecodeError:                                                             # impossible que l'utf-16 soit mal formé mais pourquoi pas
    print("Erreur : le fichier JSON est mal formé.")
    exit()


    """Pour revenir sur les logs, faudrait prévoir dans le code les entrées mal formées et les logger, avec les même logs utilisés sur l'autre script.
    Par exemple si un IoC a pas de type/champ correct, ou si le hash est bizarre (valider la forme du hash avec les différents regex genre 32/40/64).
    petite flemme pour l'instant, il y a beaucoup à améliorer d'autre."""


# extraire et transformer les IoCs de type hash
rules = []
for ioc in data.get("data", []):
    ioc_type = ioc.get("ioc_type")
    print(f"Traitement de l'IoC : {ioc}")                           # ça print pour chaque IoC
    if ioc_type in valid_hash_types:
        rules.append({                                              # rien compris mais apparemment gravityzone veut ce format
            "details": {
                "algorithm": valid_hash_types[ioc_type],
                "hash": ioc.get("ioc")
            }
        })

# à quoi ressemble le json final
gravityzone_payload = {
    "type": "hash",
    "rules": rules,
    "recursive": True                           # sais pas ça sert à quoi mais c'est dans la doc
}

# là c'est où on crée le fichier de sortie
with open("filtered_hashes_for_gravityzone.json", "w", encoding="utf-8") as outfile:
    json.dump(gravityzone_payload, outfile, indent=2)

print(f"{len(rules)} hashes filtrés et formatés pour GravityZone.")

"""ça manque cruellement de fonctions genre load_data(), save_to_file(), etc.
après j'ai jamais transformé des fichiers d'entrée/sortie aussi gros, donc pas sur de comment la mémoire va tenir.
ensuite niveau sécurité faudrait voir pour vérifier le code entrant, parce que c'est exploitable, probablement.
et pareil niveau permissions sur les fichiers, mais en vrai ca va juste être mis sur le DC donc ca va aller, probablement."""