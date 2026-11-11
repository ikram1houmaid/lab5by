
# Exception personnalisée
class SoldeInsuffisantException(Exception):
    def __init__(self, message):
        super().__init__(message)


# Classe CompteBancaire
class CompteBancaire:

    def __init__(self, nom, solde=0):
        self.nom = nom
        self.solde = solde

    # Méthode pour déposer de l'argent
    def deposer(self, montant):
        if montant > 0:
            self.solde += montant
            print("Dépôt effectué avec succès.")
        else:
            print("Le montant doit être positif.")

    # Méthode pour retirer de l'argent
    def retirer(self, montant):
        if montant > self.solde:
            raise SoldeInsuffisantException(
                "Solde insuffisant pour ce retrait."
            )

        if montant <= 0:
            print("Le montant doit être positif.")
            return

        self.solde -= montant
        print("Retrait effectué avec succès.")

    # Méthode pour afficher le compte
    def afficher(self):
        print(f"Compte: {self.nom}, Solde: {self.solde}€")


# Exemple d'utilisation
try:
    compte = CompteBancaire("Alice", 100)

    compte.afficher()

    compte.retirer(150)

    compte.afficher()

except SoldeInsuffisantException as e:
    print("Erreur:", e)
