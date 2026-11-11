
import unittest
import tempfile
import os

from csv_reader import (
    charger_csv,
    FichierIntrouvableException,
    LigneInvalideException,
    PrixNegatifException
)


class TestCsvReader(unittest.TestCase):

    def setUp(self):
        # Créer un dossier temporaire
        self.dossier = tempfile.TemporaryDirectory()
        self.chemin = os.path.join(
            self.dossier.name, "articles.csv"
        )

    def tearDown(self):
        # Supprimer le dossier temporaire
        self.dossier.cleanup()

    # Test 1 : fichier CSV valide
    def test_csv_valide(self):
        with open(self.chemin, "w", encoding="utf-8") as f:
            f.write("id;nom;prix\n")
            f.write("1;Ordinateur;4500\n")
            f.write("2;Clavier;150\n")
            f.write("3;Souris;80\n")

        articles = charger_csv(self.chemin)

        self.assertEqual(len(articles), 3)
        self.assertEqual(articles[0]["nom"], "Ordinateur")
        self.assertEqual(articles[0]["prix"], 4500.0)

    # Test 2 : fichier absent
    def test_fichier_introuvable(self):
        with self.assertRaises(FichierIntrouvableException):
            charger_csv("fichier_inexistant.csv")

    # Test 3 : prix non numérique
    def test_prix_non_numerique(self):
        with open(self.chemin, "w", encoding="utf-8") as f:
            f.write("id;nom;prix\n")
            f.write("1;Ordinateur;abc\n")

        with self.assertRaises(LigneInvalideException):
            charger_csv(self.chemin)

    # Test 4 : prix négatif
    def test_prix_negatif(self):
        with open(self.chemin, "w", encoding="utf-8") as f:
            f.write("id;nom;prix\n")
            f.write("1;Ordinateur;-100\n")

        with self.assertRaises(PrixNegatifException):
            charger_csv(self.chemin)

    # Test 5 : nombre de colonnes incorrect
    def test_ligne_invalide(self):
        with open(self.chemin, "w", encoding="utf-8") as f:
            f.write("id;nom;prix\n")
            f.write("1;Ordinateur\n")

        with self.assertRaises(LigneInvalideException):
            charger_csv(self.chemin)

    # Test 6 : prix égal à zéro
    def test_prix_zero(self):
        with open(self.chemin, "w", encoding="utf-8") as f:
            f.write("id;nom;prix\n")
            f.write("1;Ordinateur;0\n")

        with self.assertRaises(PrixNegatifException):
            charger_csv(self.chemin)


if __name__ == "__main__":
    unittest.main()
