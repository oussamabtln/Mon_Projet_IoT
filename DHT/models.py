from django.db import models


class Dht11(models.Model):
    # Les champs existants
    temp = models.FloatField(null=True)
    hum = models.FloatField(null=True)

    # --- NOUVEAUX CHAMPS ---
    co = models.FloatField(null=True)  # Pour le capteur de Gaz (MQ9)
    light = models.FloatField(null=True)  # Pour le capteur de Lumière (LDR)
    # -----------------------

    dt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"T:{self.temp} | H:{self.hum} | CO:{self.co} | L:{self.light}"