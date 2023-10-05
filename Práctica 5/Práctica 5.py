import pandas as pd
import statsmodels.api as sm
from typing import List
from statsmodels.formula.api import ols

#Práctica 5: ANOVA
#Este script imprime los resultados.

def doANOVA(df: pd.DataFrame, variablesStr: str, typeOfANOVA: int, title:str, hypothesis: List[str]):
    print('\n' + title)
    model = ols(variablesStr, data=df).fit()
    anovaDF = sm.stats.anova_lm(model, typ=typeOfANOVA)
    print(anovaDF)
    print('\nConclusión:')

    if anovaDF['PR(>F)'][0] < 0.05:
        print(f'Hay {hypothesis[0]}') #Hay significancia
    else:
        print(f'No hay {hypothesis[0]}') #No hay significancia

    if typeOfANOVA > 1:
        if anovaDF['PR(>F)'][1] < 0.05:
            print(f'Hay {hypothesis[1]}') #Hay significancia
        else:
            print(f'No hay {hypothesis[1]}') #No hay significancia  


def main():
    try:
        GVDdf = pd.read_csv('2013-01_2018-03.csv', index_col=0)
    except:
        raise Exception('Por favor, corre Pre-Práctica 5.py antes de ejecutarme.')
    
### ANOVA 1: 
#   State   Date (per Month)  
#           31-01-2014  31-02-2014 ...
#   Texas   3           2
#   Calif   4           1
#   Orego   5           5
#   Michi   6           3
#
#   Data represents amount of participants per state per day.
#   Two-Way ANOVA.
    GVDdf.date = pd.to_datetime(GVDdf.date)
    peoplePerStateDay = GVDdf.groupby(['state',pd.Grouper(key='date', freq="M")])[['n_participants']].sum()
    peoplePerStateDay.reset_index(inplace=True)
    peoplePerStateDay.set_index('date', inplace=True)
    peoplePerStateDay.reset_index(inplace=True)
    #print(peoplePerStateDay)
    doANOVA(peoplePerStateDay, 'n_participants ~ state + date', 2, 
            '¿El estado y el mes influyen en la cantidad de participantes?', 
            ['influencia entre el estados y la cantidad de participantes.',
             'influencia entre los meses y la cantidad de participantes.'])

### ANOVA 2:
#   Gender  Participant-Type  
#           Subject-Suspect  Victim  Unknown
#   Woman   3                2       3
#   Man     4                1       6
#   Unknown 5                5       8
#
#   Data represents amount of participants per gender per type.
#   Two-Way ANOVA.
    perGenderAndType = pd.read_csv('../Práctica 3/porGeneroYTipo.csv')
    perGenderAndType.drop(4, inplace=True) #El indice 4 apunta a un género "Male - Female", un error.
    #print(perGenderAndType)
    doANOVA(perGenderAndType, 'participant_age ~ participant_gender + participant_type', 2, 
            '¿El género y el rol (victima/victimario) tienen significancia en la muestra de participantes?', 
            ['significancia en (o diferencias entre) los géneros de los participante.',
             'importancia en el rol del participante (victima/victimario).'])


### ANOVA 3:
#   n_guns  n_participants
#           1   2   3   4   5   
#   1       4   8   5   9   4
#   2       4   9   3   6   0
#   3       3   8   4   9   4
#
#   Data represents amount of injured people per number of guns.
#   One-Way ANOVA.
    perGunsAndInjured = GVDdf.groupby(['n_guns_involved','n_participants'])[['n_injured']].sum()
    perGunsAndInjured.reset_index(inplace=True)
    perGunsAndInjured.set_index('n_guns_involved', inplace=True)
    perGunsAndInjured.reset_index(inplace=True)
    perGunsAndInjured.drop('n_participants', axis=1, inplace=True)
    #print(perGunsAndInjured)
    doANOVA(perGunsAndInjured, 'n_injured ~ n_guns_involved', 1, 
            '¿La cantidad de pistolas afecta en la cantidad de personas heridas?', 
            ['influencia de la cantidad de pistolas en las personas heridas.'])


### ANOVA 4:
#   n_injured   date
#               01-01-2013  02-01-2013 ...
#   1           4           8
#   2           4           9
#   3           3           8
#
#   Data represents amount of killed people per injured person.
#   One-Way ANOVA.
    perInjuredAndKilled = GVDdf.groupby(['n_injured','date'])[['n_killed']].sum()
    perInjuredAndKilled.reset_index(inplace=True)
    perInjuredAndKilled.set_index('n_injured', inplace=True)
    perInjuredAndKilled.reset_index(inplace=True)
    perInjuredAndKilled.drop('date', axis=1, inplace=True)
    #print(perInjuredAndKilled)
    doANOVA(perInjuredAndKilled, 'n_killed ~ n_injured', 1, 
            '¿La cantidad de heridos influye en el número de muertos?', 
            ['influencia de la cantidad de heridos en el número de muertos.'])


### ANOVA 5:
#   status      participant_type
#               Subject-Suspect   Victim
#   Arrested    5                 9
#   Injured     8                 2
#   Killed      4                 3
#   ...
#   Data represents amount of people per status per type.
#   Two-Way ANOVA.
    perStatusAndType = pd.read_csv('../Práctica 3/porEstatusYTipo.csv')
    #print(perStatusAndType)
    doANOVA(perStatusAndType, 'participant_age_group ~ participant_type + participant_status', 2, 
            '¿El rol del participante influye en su futuro paradero (muerto, herido, arrestado)?', 
            ['influencia del rol del participante en su futuro paradero.',
             'influencia del estatus en los participantes.'])


### ANOVA 6:
#   age_group     participant_type
#                 Subject-Suspect    Victim
#   Adult         7                  2
#   Teen          2                  4
#   Child         9                  1
#
#   Data represents amount of people per age group per type.
#   Two-Way ANOVA.
    perAgeGroupAndType = pd.read_csv('../Práctica 3/porGrupoEdadyTipo.csv')
    #print(perAgeGroupAndType)
    doANOVA(perAgeGroupAndType, 'participant_age ~ participant_age_group + participant_type', 2, 
            '¿La edad del participante influye en su rol (victima/victimario)?', 
            ['influencia de la edad del participante en el rol de los participantes.', 
             'influencia del rol en los participantes.'])


if __name__ == "__main__":
    main()
