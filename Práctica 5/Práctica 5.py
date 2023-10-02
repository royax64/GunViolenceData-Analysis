import pandas as pd
import statsmodels.api as sm
import json
from statsmodels.formula.api import ols


#Práctica 5: ANOVA
#No hay muchos datos numéricos con los que pueda hacer ANOVA
def main():
    try:
        GVDdf = pd.read_csv('2013-01_2018-03.csv', index_col=0)
    except:
        print('Por favor, corre Pre-Práctica 5.py antes de ejecutarme.')
        exit(1)
    

    
    



if __name__ == "__main__":
    main()

