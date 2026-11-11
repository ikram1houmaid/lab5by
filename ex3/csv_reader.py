
import csv
import logging
import os

# Configuration du Logger
logging.basicConfig(
    filename="erreurs.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Exception principale
class CsvException(Exception):
    def __init__(self, message):
        super().__init__(message)


# Exceptions personnalisées
class FichierIntrouvableException(CsvException):
    pass


class LigneInvalideException(CsvException):
    pass


class PrixNegatifException(CsvException):
    pass


# Fonction de lecture du fichier CSV
def charger_csv(chemin):

    articles = []

    try:
        with open(chemin, "r", encoding="utf-8", newline="") as fichier:

            lecteur = csv.reader(fichier, delimiter=";")

            for numero, ligne in enumerate(lecteur, start=1):

                # Ignorer les lignes vides
                if not ligne or all(col.strip() == "" for col in ligne):
                    continue

                # Ignorer l'en-tête
                if numero == 1 and ligne == ["id", "nom", "prix"]:
                    continue

                # Vérifier le nombre de colonnes
                if len(ligne) != 3:
                    raise LigneInvalideException(
                        f"Ligne {numero} : exactement 3 colonnes sont requises."
                    )

                identifiant, nom, prix = ligne

                # Vérifier les champs obligatoires
                if not identifiant.strip() or not nom.strip():
                    raise LigneInvalideException(
                        f"Ligne {numero} : identifiant ou nom manquant."
                    )

                # Vérifier si le prix est numérique
                try:
                    prix = float(prix.strip())
                except ValueError:
                    raise LigneInvalideException(
                        f"Ligne {numero} : le prix doit être numérique."
                    )

                # Vérifier si le prix est positif
                if prix <= 0:
                    raise PrixNegatifException(
                        f"Ligne {numero} : le prix doit être supérieur à zéro."
                    )

                # Ajouter l'article à la liste
                articles.append({
                    "id": identifiant.strip(),
                    "nom": nom.strip(),
                    "prix": prix
                })

    except FileNotFoundError:
        raise FichierIntrouvableException(
            f"Le fichier '{chemin}' est introuvable."
        )

    except CsvException as e:
        logging.error(str(e))
        raise

    return articles
