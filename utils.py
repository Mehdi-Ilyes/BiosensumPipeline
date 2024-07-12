"""
File: utils.py
Author: BioSensUM 
Description: Ce fichier contient plusieurs fonctions qui seront utilisées dans le fichier main.py pour analyser les données.
"""
import pandas as pd


def read_current_from_csv(csv_file):
    """
    Lis un csv contenant des colonnes Voltage et Current et forme un dataframe avec

    Parameters:
    - csv_file (str): Nom/Lien du fichier csv

    Returns:
    - pd.DataFrame: DataFrame contenant le voltage et le courant.
    """
    try:
        # Lire le CSV en pd.dataframe
        df = pd.read_csv(csv_file)
        
        #'Voltage' et 'Current'
        df.columns = ['Voltage', 'Current']

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
    - pd.DataFrame: DataFrame with smoothed 'Voltage' and 'Current' columns.
    """
    # Apply rolling average to 'Voltage' and 'Current' columns
    smoothed_df = df.rolling(window=window_size).mean().dropna()

    return smoothed_df

