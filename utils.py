"""
File: utils.py
Author: BioSensUM 
Description: Ce fichier contient plusieurs fonctions qui seront utilisées dans le fichier main.py pour analyser les données.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, savgol_filter

def read_units_from_csv(csv_file):
    """
    Lit les informations d'unités à partir de lignes spécifiques d'un fichier CSV.

    Paramètres :
    - csv_file (str) : Chemin ou lien vers le fichier CSV contenant les informations d'unités.

    Retourne :
    - dict : Dictionnaire contenant les unités extraites pour chaque colonne.
    """
    try:
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
    Nettoie le DataFrame en supprimant les lignes contenant des valeurs NaN.

    Paramètres :
    - df (pd.DataFrame) : DataFrame à nettoyer.

    Retourne :
    - pd.DataFrame : DataFrame après suppression des lignes avec NaN.
    """
    try:
        # Vérifie que l'entrée est bien un DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError("L'entrée doit être un DataFrame.")

        # Supprimer les lignes avec des valeurs NaN
        cleaned_df = df.dropna()

        return cleaned_df

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None


def smooth_data(df, window_length=11, polyorder=3):
    """
    Lisse les données dans le DataFrame à l’aide d’une rolling average.

    Parameters:
    - df (pd.DataFrame): Dataframe en entrée à modifier
    - window_size (int): Taille de la window pour la rolling average

    Returns:
    - pd.DataFrame: DataFrame with smoothed 'Potential' and 'Current' columns.
    """
    # Apply rolling average to 'Potential' and 'Current' columns
    if 'Potential' not in df.columns or 'Current' not in df.columns:
        raise ValueError("DataFrame must contain 'Potential' and 'Current' columns.")
    
    # Apply Savitzky-Golay filter to 'Potential' and 'Current' columns
    smoothed_df = df.copy()
    smoothed_df['Potential'] = savgol_filter(df['Potential'], window_length=window_length, polyorder=polyorder)
    smoothed_df['Current'] = savgol_filter(df['Current'], window_length=window_length, polyorder=polyorder)
    
    return smoothed_df


def filter_peak_by_prominence(df, column='Current', prominence=0.1, m=1):
    """
    Finds local peaks in a DataFrame column with a certain prominence. If m = 1, it returns the minima, otherwise it returns maxima.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing the data.
    - column (str): The column name to search for local minimums.
    - prominence (float): The prominence threshold to identify local minimums.

    Returns:
    - List of indices where local minimums are found, or an empty list if none are found.
    """
    try:
        # Check if the specified column exists in the DataFrame
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame.")
        
        # Find local minimums by using the negative of the data
        if(m == 1):
            peaks, _ = find_peaks(-df[column], prominence=prominence)
        else:
            peaks, _ = find_peaks(df[column], prominence=prominence)

        
        # Return the indices of local minimums, or an empty list if none are found
        return peaks.tolist() if len(peaks) > 1 else []
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    


def find_extreme_peaks(df, column='Current', prominence=0.1, m=1):
    """
    Finds local peaks in a DataFrame column with a certain prominence, 
    adjusting prominence until at least one peak is found.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing the data.
    - column (str): The column name to search for local peaks.
    - prominence (float): The initial prominence threshold to identify local peaks.
    - m (int): Indicator for finding minima (1) or maxima (other).

    Returns:
    - List of indices where local peaks are found.
    """
    try:
        while filter_peak_by_prominence(df, column, prominence, m) == []:
            prominence /= 2
    
        print(prominence)
        return filter_peak_by_prominence(df, column, prominence, m)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    


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

    # Plot de 'Courant' par rapport à 'Potentiel' avec les unités spécifiées
    plt.figure(figsize=(10, 6))  # Ajuster la taille de la figure si nécessaire
    plt.plot(df['Potential'], df['Current'], marker='o', linestyle='-', color='b', label='Courant vs Potentiel')
    
    # Peaks
    min = find_extreme_peaks(df, 'Current', 0.1, 1)
    max =  find_extreme_peaks(df, 'Current', 0.1, 0)
    
    plt.plot(df['Potential'][max], df['Current'][max], 'ro', label='Maximum')
    plt.plot(df['Potential'][min], df['Current'][min], 'go', label='Minimum')


    plt.xlabel(f'Potentiel ({units["Potential"]})') 
    plt.ylabel(f'Courant ({units["Current"]})')      
    plt.title('Tracé Courant vs Potentiel')       
    plt.legend()
    plt.grid(True)
    plt.show()
