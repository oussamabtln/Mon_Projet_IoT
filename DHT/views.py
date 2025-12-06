import joblib
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Dht11

# Chemin vers le fichier du modèle IA
MODEL_PATH = os.path.join(settings.BASE_DIR, 'weather_model.joblib')


def dashboard(request):
    return render(request, 'dashboard.html')


def graph_temp(request): return render(request, 'graph_temp.html')


def graph_hum(request): return render(request, 'graph_hum.html')


def graph_co(request): return render(request, 'graph_co.html')


def graph_light(request): return render(request, 'graph_light.html')


def download_csv(request): pass  # À compléter si besoin


def latest_json(request):
    # 1. Récupérer la dernière donnée reçue
    current = Dht11.objects.order_by('-dt').first()

    if not current:
        return JsonResponse({"error": "Pas de données"}, status=404)

    # Récupérer la donnée précédente pour les flèches de tendance
    previous = Dht11.objects.order_by('-dt')[1] if Dht11.objects.count() > 1 else None

    # 2. PRÉDICTION IA
    prediction = "Analyse..."

    if os.path.exists(MODEL_PATH):
        try:
            # On charge le cerveau
            model = joblib.load(MODEL_PATH)

            # On prépare les 4 valeurs pour l'IA : [Temp, Hum, CO, Light]
            # (On met 0 si une valeur est manquante pour éviter le crash)
            X_input = [[
                current.temp if current.temp is not None else 0,
                current.hum if current.hum is not None else 0,
                current.co if current.co is not None else 0,
                current.light if current.light is not None else 0
            ]]

            # L'IA fait sa prédiction
            prediction = model.predict(X_input)[0]

        except Exception as e:
            print(f"Erreur IA : {e}")
            prediction = "Erreur IA"
    else:
        prediction = "Modèle non trouvé"

    # 3. Envoi de la réponse au site
    return JsonResponse({
        "temperature": current.temp,
        "humidity": current.hum,
        "co": current.co,
        "light": current.light,
        "timestamp": current.dt.strftime("%H:%M:%S"),

        "prev_temp": previous.temp if previous else None,
        "prev_hum": previous.hum if previous else None,
        "prev_co": previous.co if previous else None,
        "prev_light": previous.light if previous else None,

        "prediction": prediction  # <--- Le résultat de l'IA (ex: "Incendie", "Pluie")
    })