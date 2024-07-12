"""
File: utils.py
Author: BioSensUM 
Description: Ce fichier contient plusieurs fonctions qui seront utilisées dans le fichier main.py pour analyser les données.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_units_from_csv(csv_file):
    """
    Lit les informations d'unités à partir de lignes spécifiques d'un fichier CSV.

    Paramètres :
    - csv_file (str) : Chemin ou lien vers le fichier CSV contenant les informations d'unités.

    Retourne :
    - dict : Dictionnaire contenant les unités extraites pour chaque colonne.
    """
    try:
        # Read the CSV to extract units
        unit_row = pd.read_csv(csv_file,  skiprows=5, nrows=1, header=None, encoding='utf-16').iloc[0]
        units = {}
        units['Potential'] = unit_row[0].split(':')[-1].strip()
        units['Current'] = unit_row[1].strip()

        return units

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{csv_file}' is empty.")
        return None
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file '{csv_file}': {e}")
        return None
    

def read_current_from_csv(csv_file):
    """
    Lis un csv contenant des colonnes Potential et Current et forme un dataframe avec

    Parameters:
    - csv_file (str): Nom/Lien du fichier csv

    Returns:
    - pd.DataFrame: DataFrame contenant le Potential et le courant.
    """
    try:
        # Lire le CSV en pd.dataframe
        df = pd.read_csv(csv_file, skiprows=6, encoding='utf-16', header=None)
        #'Potential' et 'Current'
        df.columns = ['Potential', 'Current']

        return df

    # Traitement des erreurs
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{csv_file}' is empty.")
        return None
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file '{csv_file}': {e}")
        return None
    
    
def clean_data(df):
    """
    Clean-up du dataframe en enlevant les lignes avec NaN

    Parameters:
    - df (pd.DataFrame): Dataframe en entrée à modifier

    Returns:
    - pd.DataFrame: Dataframe modifié.
    """
    # Drop rows with any NaN values
    cleaned_df = df.dropna()

    return cleaned_df


def smooth_data(df, window_size=3):
    """
    Lisse les données dans le DataFrame à l’aide d’une rolling average.

    Parameters:
    - df (pd.DataFrame): Dataframe en entrée à modifier
    - window_size (int): Taille de la window pour la rolling average

    Returns:
    - pd.DataFrame: DataFrame with smoothed 'Potential' and 'Current' columns.
    """
    # Apply rolling average to 'Potential' and 'Current' columns
    smoothed_df = df.rolling(window=window_size).mean().dropna()

    return smoothed_df

def plot_current_vs_potential_with_units(df, units):
    """
    Trace 'Current' par rapport à 'Potentiel' à partir du DataFrame avec les unités spécifiées.

    Paramètres :
    - df (pd.DataFrame) : DataFrame d'entrée contenant les colonnes 'Potentiel' et 'Courant'.
    - units (dict) : Dictionnaire contenant les unités pour chaque colonne ('Potential' et 'Current').

    """
    # Vérification de l'existence des colonnes dans le DataFrame
    if 'Potential' not in df.columns or 'Current' not in df.columns:
        print("Erreur : Le DataFrame ne contient pas les colonnes 'Potential' et 'Current'.")
        return

    # Tracé de 'Courant' par rapport à 'Potentiel' avec les unités spécifiées
    plt.figure(figsize=(10, 6))  # Ajuster la taille de la figure si nécessaire
    plt.plot(df['Potential'], df['Current'], marker='o', linestyle='-', color='b', label='Courant vs Potentiel')
    plt.xlabel(f'Potentiel ({units["Potential"]})')  # Mise à jour de l'étiquette de l'axe x avec les unités appropriées
    plt.ylabel(f'Courant ({units["Current"]})')      # Mise à jour de l'étiquette de l'axe y avec les unités appropriées
    plt.title('Tracé Courant vs Potentiel')          # Mise à jour du titre du tracé
    plt.legend()
    plt.grid(True)
    plt.show()

