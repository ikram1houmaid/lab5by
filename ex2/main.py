
import logging

# Configuration du Logger
logging.basicConfig(
    filename="reservations.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Classe mère des exceptions
class ReservationException(Exception):
    def __init__(self, message):
        super().__init__(message)


# Exceptions personnalisées
class CapaciteDepasseeException(ReservationException):
    pass


class NombreInvalideException(ReservationException):
    pass


class NomClientInvalideException(ReservationException):
    pass


# Classe Evenement
class Evenement:

    def __init__(self, nom, capacite):
        self.nom = nom
        self.capacite = capacite
        self.places_reservees = 0

    # Méthode de réservation
    def reserver(self, nom_client, nb_places):

        try:
            # Vérifier le nom du client
            if not nom_client.strip():
                raise NomClientInvalideException(
                    "Nom du client requis."
                )

            # Vérifier le nombre de places
            if nb_places <= 0:
                raise NombreInvalideException(
                    "Nombre de places invalide."
                )

            # Vérifier la capacité
            if self.places_reservees + nb_places > self.capacite:
                raise CapaciteDepasseeException(
                    "Capacité dépassée."
                )

            # Effectuer la réservation
            self.places_reservees += nb_places

            print(
                f"Réservation confirmée pour {nom_client} "
                f"({nb_places} places)."
            )

            logging.info(
                f"Réservation réussie : {nom_client}, "
                f"{nb_places} places."
            )

        except ReservationException as e:
            logging.error(f"Échec de réservation : {e}")
            raise

    # Méthode d'affichage
    def afficher(self):
        print(
            f"Événement: {self.nom} — "
            f"{self.places_reservees}/{self.capacite} "
            "places réservées"
        )


# Exemple d'utilisation
try:
    event = Evenement("Concert", 5)

    event.reserver("", 2)

    event.afficher()

except ReservationException as e:
    print("Erreur:", e)
