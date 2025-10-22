import json

# Types de hash valides et leur correspondance GravityZone
valid_hash_types = {
    "sha256_hash": "sha256",
    "sha1_hash": "sha1",
    "md5_hash": "md5"
}

# Charger le fichier JSON brut
try:
    with open("Import_IoC_Threatfox.json", "r", encoding="utf-16") as infile:
        data = json.load(infile)
        print("Données chargées avec succès.")
except FileNotFoundError:
    print("Erreur : le fichier Import_IoC_Threatfox.json est introuvable.")
    exit()
except json.JSONDecodeError:
    print("Erreur : le fichier JSON est mal formé.")
    exit()

# Extraire et transformer les IoCs de type hash
rules = []
for ioc in data.get("data", []):
    ioc_type = ioc.get("ioc_type")
    print(f"Traitement de l'IoC : {ioc}")  # Ajout d'un log pour chaque IoC
    if ioc_type in valid_hash_types:
        rules.append({
            "details": {
                "algorithm": valid_hash_types[ioc_type],
                "hash": ioc.get("ioc")
            }
        })

# Construire le payload final
gravityzone_payload = {
    "type": "hash",
    "rules": rules,
    "recursive": True
}

# Sauvegarder dans un fichier JSON
with open("filtered_hashes_for_gravityzone.json", "w", encoding="utf-8") as outfile:
    json.dump(gravityzone_payload, outfile, indent=2)

print(f"{len(rules)} hashes filtrés et formatés pour GravityZone.")