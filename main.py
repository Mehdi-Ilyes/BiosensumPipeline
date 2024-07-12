"""
File: main.py
Author: BioSensUM 
Description: Ce script utilisera un Emstat3 pour effectuer un SWV avec des paramètres prédéfinis. Le fichier CSV sera
             traité et analysé sous forme de pandas.dataframe. Le gain sera alors calculé et affiché à l'utilisateur
             avec le graphique obtenu.
"""
import plot_advanced_swv
import utils

def main():
    #Faire la SWV(+Reverse SWV) avec comme resultat un output.csv
    plot_advanced_swv.SWV_Console()

    #Recuperer les data et clean-up
    df = utils.read_voltage_current_from_csv("output.txt")
    cleaned_df = utils.clean_data(df)
    smoothed_df = utils.smooth_data(cleaned_df)

if __name__ == '__main__':
    main()
