"""
File: main.py
Author: BioSensUM 
Description: Ce script utilisera un Emstat3 pour effectuer un SWV avec des paramètres prédéfinis. Le fichier CSV sera
             traité et analysé sous forme de pandas.dataframe. Le gain sera alors calculé et affiché à l'utilisateur
             avec le graphique obtenu.
"""
import utils
import plot_advanced_swv

#Nom du csv(à changer pour output.txt)
csv_name = "output/output.csv"

def main():
    #Faire la SWV(+Reverse SWV) avec comme resultat un output.csv
    #plot_advanced_swv.SWV_Console()

    #Recuperer les data et clean-up
    df = utils.read_current_from_csv(csv_name)
    units = utils.read_units_from_csv(csv_name)
    print(units)
    cleaned_df = utils.clean_data(df)
    smoothed_df = utils.smooth_data(cleaned_df)

    #Affichage des données  
    min, maxima = utils.plot_current_vs_potential_with_units(smoothed_df, units)
    print("The difference is ", utils.calculate_current_difference(smoothed_df, min, maxima[0], maxima[1])," ", units['Current'])
    

if __name__ == '__main__':
    main()
