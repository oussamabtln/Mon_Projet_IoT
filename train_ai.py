import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
import os

print("🚀 Démarrage de l'entraînement TOUT-TERRAIN...")


def charger_dataset(fichier, label_cible, co_simule=None, light_simule=None):
    df = pd.DataFrame()

    # 1. TENTATIVE : Lire comme un Excel (même si c'est marqué .csv)
    # C'est souvent le cas quand on renomme un xlsx en csv
    try:
        df = pd.read_excel(fichier, engine='openpyxl')
        # Vérification si les colonnes sont lisibles
        cols = df.columns.astype(str).str.lower()
        if any('temp' in c for c in cols):
            print(f"   ✅ Lecture EXCEL réussie pour {fichier}")
    except Exception:
        # 2. TENTATIVE : Lire comme un vrai CSV (si ce n'est pas un Excel)
        encodages = ['utf-8', 'latin-1', 'cp1252']
        for enc in encodages:
            try:
                df_test = pd.read_csv(fichier, sep=None, engine='python', encoding=enc, on_bad_lines='skip')
                cols_test = df_test.columns.astype(str).str.lower()
                if any('temp' in c for c in cols_test):
                    df = df_test
                    print(f"   ✅ Lecture CSV réussie pour {fichier} ({enc})")
                    break
            except:
                continue

    if df.empty:
        print(f"   ❌ ÉCHEC : Impossible de lire {fichier}. Vérifiez le format.")
        return pd.DataFrame()

    try:
        # Nettoyage des noms de colonnes
        df.columns = df.columns.astype(str).str.strip()

        # Recherche intelligente des colonnes
        col_temp = next((c for c in df.columns if 'Temp' in c), None)
        col_hum = next((c for c in df.columns if 'Humid' in c), None)
        col_light = next((c for c in df.columns if 'Light' in c), None)
        col_co = next((c for c in df.columns if 'CO' in c), None)

        # Recherche de la colonne cible (Condition)
        col_target = next((c for c in df.columns if any(x in c for x in ['Condition', 'Rain', 'Fire', 'Fog'])), None)

        if not col_temp or not col_hum:
            print(f"   ⚠️ Colonnes Temp/Hum manquantes dans {fichier}")
            return pd.DataFrame()

        # Filtrage si colonne cible présente
        if col_target:
            df = df[df[col_target] == 1].copy()

        # Création du dataset propre
        data = pd.DataFrame()
        data['temp'] = df[col_temp]
        data['hum'] = df[col_hum]

        # Simulation Capteurs manquants
        n = len(data)
        if col_co:
            data['co'] = df[col_co]
        else:
            data['co'] = np.random.uniform(co_simule[0], co_simule[1], n)

        if col_light:
            data['light'] = df[col_light]
        else:
            data['light'] = np.random.uniform(light_simule[0], light_simule[1], n)

        data['label'] = label_cible
        print(f"      🔹 {n} lignes chargées.")
        return data

    except Exception as e:
        print(f"   ❌ Erreur traitement {fichier}: {e}")
        return pd.DataFrame()


# --- CHARGEMENT ---
# Pluie (Manque CO -> on met peu de gaz)
df_rain = charger_dataset('rain.csv', 'Pluie', co_simule=(0, 50))

# Feu (Manque Light -> on met de la lumière forte)
df_fire = charger_dataset('fire.csv', 'Incendie', light_simule=(400, 1000))

# Brouillard (Manque CO -> on met peu de gaz)
df_fog = charger_dataset('fog.csv', 'Brouillard', co_simule=(0, 80))

# Normal
print("🔹 Génération données 'Normal'...")
df_norm = pd.DataFrame({
    'temp': np.random.uniform(15, 30, 500),
    'hum': np.random.uniform(30, 60, 500),
    'co': np.random.uniform(0, 100, 500),
    'light': np.random.uniform(500, 1000, 500),
    'label': 'Normal'
})

# --- ENTRAÎNEMENT ---
dfs_to_concat = [df for df in [df_rain, df_fire, df_fog, df_norm] if not df.empty]
df_final = pd.concat(dfs_to_concat, ignore_index=True)

# Mélange
df_final = df_final.sample(frac=1).reset_index(drop=True)

X = df_final[['temp', 'hum', 'co', 'light']]
y = df_final['label']

print(f"🧠 Entraînement sur {len(df_final)} lignes...")
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# SAUVEGARDE
joblib.dump(model, 'weather_model.joblib')
print("🎉 SUCCÈS ! Cerveau IA créé : 'weather_model.joblib'")