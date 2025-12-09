from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import Dht11
from .serializers import DHT11serialize
import csv


# --- VUES PRINCIPALES ---

def dashboard(request):
    """ Affiche la page principale du Dashboard Usine """
    return render(request, "dashboard.html")


def graph_temp(request):
    """ Affiche la page du graphique Température """
    return render(request, 'graph_temp.html')


def graph_hum(request):
    """ Affiche la page du graphique Humidité """
    return render(request, 'graph_hum.html')


# --- API DE DONNÉES (Pour le JS du Dashboard) ---

def latest_json(request):
    """
    Renvoie la dernière mesure en JSON pour le Dashboard.
    Seulement Température et Humidité (Projet Usine).
    """
    # On récupère la toute dernière mesure
    data = Dht11.objects.last()

    # Sécurité si la base de données est vide
    if not data:
        return JsonResponse({"detail": "Pas de données"}, status=404)

    # On renvoie tout en JSON
    return JsonResponse({
        "temperature": data.temp,
        "humidity": data.hum,
        "timestamp": data.dt.strftime("%H:%M:%S") if data.dt else "--"
    })


# --- FONCTIONNALITÉS SUPPLÉMENTAIRES ---

def download_csv(request):
    """ Permet de télécharger tout l'historique en fichier Excel/CSV """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'

    writer = csv.writer(response)
    # En-têtes du fichier CSV (Juste Temp et Hum)
    writer.writerow(['ID', 'Température', 'Humidité', 'Date'])

    # Récupération des données
    model_values = Dht11.objects.values_list('id', 'temp', 'hum', 'dt')

    for row in model_values:
        writer.writerow(row)

    return response


def table(request):
    """ Affiche un tableau simple (page /index/) """
    derniere_ligne = Dht11.objects.last()
    if not derniere_ligne:
        return HttpResponse("Pas de données")

    delta_temps = timezone.now() - derniere_ligne.dt
    difference_minutes = int(delta_temps.total_seconds() // 60)

    temps_ecoule = f' il y a {difference_minutes} min'
    if difference_minutes > 60:
        temps_ecoule = f'il y a {difference_minutes // 60}h {difference_minutes % 60}min'

    valeurs = {
        'date': temps_ecoule,
        'id': derniere_ligne.id,
        'temp': derniere_ligne.temp,
        'hum': derniere_ligne.hum
    }
    return render(request, 'value.html', {'valeurs': valeurs})


def graphique(request):
    """ Ancienne vue pour chart.html (Optionnelle) """
    data = Dht11.objects.all()
    return render(request, 'chart.html', {'data': data})


def test(request):
    return HttpResponse('IoT Project')