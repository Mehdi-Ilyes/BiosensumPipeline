"""
File: main.py
Author: BioSensUM 
Description: This script will use an Emstat3 to perform SWV with predefined parameters. The CSV output will
             then be treated and analyzed to obtain the gain. The output will then be printed to the user
             along with the plot obtained.
"""
import plot_advanced_swv

def main():
    #Faire la SWV(+Reverse SWV)
    print("hi")
    plot_advanced_swv.SWV_Console()
    

if __name__ == '__main__':
    main()