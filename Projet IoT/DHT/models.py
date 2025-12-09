
from django.db import models


class Dht11(models.Model):
    temp = models.FloatField(null=True)
    hum = models.FloatField(null=True)
    dt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Temp: {self.temp}"


class Incident(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    type_incident = models.CharField(max_length=100)  # ex: "Surchauffe Machine 1"
    niveau_urgence = models.CharField(max_length=20, default='CRITIQUE')

    # État de validation
    est_traite = models.BooleanField(default=False)
    traite_par = models.CharField(max_length=100, null=True, blank=True)  # Nom de l'employé
    date_traitement = models.DateTimeField(null=True, blank=True)
    note_intervention = models.TextField(null=True, blank=True)  # "J'ai redémarré le système"

    def __str__(self):
        return f"{self.type_incident} - {self.est_traite}"