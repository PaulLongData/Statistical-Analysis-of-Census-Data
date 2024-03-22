# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 14:29:52 2023

@author: pauly
"""

import pandas as pd
import numpy as np

CSOD = pd.read_csv("C:/Users/pauly/Documents/Education/3rd Level/NCI/Semester 2/Statistics II/CA1/Data/CSO Data.csv")
CSOG = pd.read_csv("C:/Users/pauly/Documents/Education/3rd Level/NCI/Semester 2/Statistics II/CA1/Data/CSO Glossary.csv")
CSO2011 = pd.read_csv("C:/Users/pauly/Documents/Education/3rd Level/NCI/Semester 2/Statistics II/CA1/Data/CSO 2011.csv")

CSOD.sort_values('GUID', ascending=True)
CSOG.sort_values('GUID', ascending=True)


CSO = pd.merge(CSOD, CSOG, how='outer', on=['GUID'])

#CSO.to_csv('CSO.csv', index = False)
#CSO2011.to_csv('CSO2011.csv', index = False)
# ______________________________________________________________________________
# Insight 1
CSOCorkCity = CSO.loc[CSO['COUNTY'] == 'CC']
CSOCorkCounty = CSO.loc[CSO['COUNTY'] == 'CK']
CSODublinCity = CSO.loc[CSO['COUNTY'] == 'DC']
CSODunLaoighre = CSO.loc[CSO['COUNTY'] == 'DR']
CSOFingal = CSO.loc[CSO['COUNTY'] == 'FL']
CSOSouthDublin = CSO.loc[CSO['COUNTY'] == 'SD']
CSOGalwayCity = CSO.loc[CSO['COUNTY'] == 'GC']
CSOGalwayCounty = CSO.loc[CSO['COUNTY'] == 'GY']

CSODublinCounty = pd.concat([CSODunLaoighre, CSOFingal, CSOSouthDublin])
CSODublinCounty['COUNTY'] = CSODublinCounty['COUNTY'].replace(
    ['COUNTY', 'FL'], 'DCo')
CSODublinCounty['COUNTY'] = CSODublinCounty['COUNTY'].replace(
    ['COUNTY', 'DR'], 'DCo')
CSODublinCounty['COUNTY'] = CSODublinCounty['COUNTY'].replace(
    ['COUNTY', 'SD'], 'DCo')

CSOInsight1 = pd.concat([CSOCorkCity, CSOCorkCounty,
                         CSODublinCity, CSODublinCounty,
                         CSOGalwayCity, CSOGalwayCounty])
CSOInsight1.sort_values('COUNTY', ascending=True)

CSOPrimarySecondaryProp = (CSOInsight1['AFF T']+CSOInsight1['BC T']+CSOInsight1['MI T'])/CSOInsight1['Total T.5']
CSOInsight1['PrimarySecondaryProp'] = CSOPrimarySecondaryProp 
CSOInsight1 = CSOInsight1[['COUNTY', 'PrimarySecondaryProp']]

CSOInsight1['Urbanity'] = np.nan
CSOInsight1['County'] = np.nan

CSOInsight1 = CSOInsight1.reset_index()

for i in range(0, len(CSOInsight1['COUNTY'])):
    if CSOInsight1['COUNTY'][i] == 'GC':
        CSOInsight1['Urbanity'][i] = 'City'
    elif CSOInsight1['COUNTY'][i] == 'DC':
        CSOInsight1['Urbanity'][i] = 'City'
    elif CSOInsight1['COUNTY'][i] == 'CC':
        CSOInsight1['Urbanity'][i] = 'City'
    else:
        CSOInsight1['Urbanity'][i] = 'Country'

for i in range(0, len(CSOInsight1['COUNTY'])):
    if CSOInsight1['COUNTY'][i] == 'GC' or CSOInsight1['COUNTY'][i] == 'GY':
        CSOInsight1['County'][i] = 'Galway'
    elif CSOInsight1['COUNTY'][i] == 'CC' or CSOInsight1['COUNTY'][i] == 'CK':
        CSOInsight1['County'][i] = 'Cork'
    else:
        CSOInsight1['County'][i] = 'Dublin'

CSOInsight1 = CSOInsight1[['PrimarySecondaryProp', 'Urbanity', 'County']]

CSOInsight1.to_csv('CSOInsight1.csv', index=False)
# ______________________________________________________________________________
# Insight 2
CSODonegal = CSO.loc[CSO['COUNTY'] == 'DL']
CSODonegal = CSODonegal[['GUID', 'SMALL_AREA',
                         'COUNTY', 'COUNTYNAME', 'EDNAME',
                         'Broadband?', 'Other?', 'None',
                         'Not Stated.11', 'Total.14']]
CSOCarlow = CSO.loc[CSO['COUNTY'] == 'CW']
CSOCarlow = CSOCarlow[['GUID', 'SMALL_AREA',
                       'COUNTY', 'COUNTYNAME', 'EDNAME',
                       'Broadband?', 'Other?', 'None',
                       'Not Stated.11', 'Total.14']]

CSODonegalCarlow = pd.concat([CSODonegal, CSOCarlow])
CSOInsight2 = CSODonegalCarlow.copy()

CSOInsight2 = CSOInsight2.reset_index()

CSOInsight2['Int Prop'] = (CSOInsight2['Broadband?']+CSOInsight2['Other?'])/(CSOInsight2['Total.14']-CSOInsight2['Not Stated.11'])

for i in range(0, len(CSOInsight2['COUNTY'])):
    if CSOInsight2['COUNTY'][i] == 'DL':
       CSOInsight2['COUNTY'][i] = 1
    elif CSOInsight2['COUNTY'][i] == 'CW':
       CSOInsight2['COUNTY'][i] = 2

# _________________

CSO2011.rename(columns={'GEOGDESC': 'SMALL_AREA'}, inplace=True)

CSO2011 = CSO2011[['SMALL_AREA', 'T15_3_B', 'T15_3_OTH', 'T15_3_N',
                   'T15_3_NS', 'T15_3_T']]
CSOInsight2_16 = CSODonegalCarlow.merge(CSO2011, on='SMALL_AREA', how='inner')

CSOInsight2_16 = CSOInsight2_16 .reset_index()

CSOInsight2_16['2011'] = np.nan
for i in range(0, len(CSOInsight2_16['T15_3_B'])):
    CSOInsight2_16['2011'][i] = (CSOInsight2_16['T15_3_B'][i]+CSOInsight2_16['T15_3_OTH'])[
        i]/(CSOInsight2_16['T15_3_T'][i]-CSOInsight2_16['T15_3_NS'][i])

CSOInsight2_16['2016'] = np.nan
for i in range(0, len(CSOInsight2_16['Broadband?'])):
    CSOInsight2_16['2016'][i] = (CSOInsight2_16['Broadband?'][i]+CSOInsight2_16['Other?'][i])/(
        CSOInsight2_16['Total.14'][i]-CSOInsight2_16['Not Stated.11'][i])


CSOInsight2_16 = CSOInsight2_16[['2011', '2016']]

CSOInsight2[' '] = np.nan
CSOInsight2['2011'] = np.nan
CSOInsight2['2016'] = np.nan

for i in range(0, len(CSOInsight2_16['2011'])):
    CSOInsight2['2011'][i] = CSOInsight2_16['2011'][i]
    CSOInsight2['2016'][i] = CSOInsight2_16['2016'][i]

CSOInsight2 = CSOInsight2[['COUNTY', 'Int Prop', ' ', '2011', '2016']]

#CSOInsight2.to_csv('CSOInsight2.csv', index=False)


# ______________________________________________________________________________
# Insight 3
CSOWaterford = CSO.loc[CSO['COUNTY'] == 'WD']
CSOLimerick = CSO.loc[CSO['COUNTY'] == 'LK']
CSODublinCounty['COUNTY'] = CSODublinCounty['COUNTY'].replace(
    ['COUNTY', 'DCo'], 'DC')
CSODublin = pd.concat([CSODublinCity, CSODublinCounty])
CSOCorkCounty['COUNTY'] = CSOCorkCounty['COUNTY'].replace(
    ['COUNTY', 'CK'], 'CC')
CSOCork = pd.concat([CSOCorkCity, CSOCorkCounty])
CSOGalwayCounty['COUNTY'] = CSOGalwayCounty['COUNTY'].replace(
    ['COUNTY', 'GY'], 'GC')
CSOGalway = pd.concat([CSOGalwayCity, CSOGalwayCounty])

CSOInsight3 = pd.concat(
    [CSOGalway, CSODublin, CSOCork, CSOLimerick, CSOWaterford])
CSOInsight3.sort_values('COUNTY', ascending=True)
CSOInsight3['Working Proportion'] = (CSOInsight3['W T']/CSOInsight3['Total T.1'])
CSOInsight3Mini = CSOInsight3['Working Proportion'].min()
#CSOInsight3 = CSOInsight3[['COUNTY', 'Working Proportion']]
CSOInsight3min = CSOInsight3.loc[CSOInsight3['Working Proportion'] == CSOInsight3Mini]

CSOInsight3.sort_values(['Working Proportion'], inplace=True)
CSOInsight3 = CSOInsight3.reset_index()
CSOInsight3['Rank'] = np.nan
for i in range(0, len(CSOInsight3['Working Proportion'])):
    CSOInsight3['Rank'][i] = i+1
for i in range(0, len(CSOInsight3['COUNTY'])):
    if CSOInsight3['COUNTY'][i]=='DC':
        CSOInsight3['COUNTY'][i]=1
    elif CSOInsight3['COUNTY'][i]=='GC':
        CSOInsight3['COUNTY'][i]=2
    elif CSOInsight3['COUNTY'][i]=='CC':
        CSOInsight3['COUNTY'][i]=3
    elif CSOInsight3['COUNTY'][i]=='WD':
        CSOInsight3['COUNTY'][i]=4
    elif CSOInsight3['COUNTY'][i]=='LK':
        CSOInsight3['COUNTY'][i]=5

CSOInsight3 = CSOInsight3.reset_index()
CSOInsight3['Galway'] = np.nan
CSOInsight3['Cork'] = np.nan
CSOInsight3['Dublin'] = np.nan
CSOInsight3['Limerick'] = np.nan
CSOInsight3['Waterford'] = np.nan
CSOInsight3['GalwayValues'] = np.nan
CSOInsight3['CorkValues'] = np.nan
CSOInsight3['DublinValues'] = np.nan
CSOInsight3['LimerickValues'] = np.nan
CSOInsight3['WaterfordValues'] = np.nan


for i in range(0, len(CSOInsight3['COUNTY'])):
    if CSOInsight3['COUNTY'][i] == 'CC': 
        CSOInsight3['Cork'][i] = CSOInsight3['Rank'][i]
        CSOInsight3['CorkValues'][i] = CSOInsight3['Working Proportion'][i]

    elif CSOInsight3['COUNTY'][i] == 'GC': 
        CSOInsight3['Galway'][i] = CSOInsight3['Rank'][i]
        CSOInsight3['GalwayValues'][i] = CSOInsight3['Working Proportion'][i]

    elif CSOInsight3['COUNTY'][i] == 'DC': 
        CSOInsight3['Dublin'][i] = CSOInsight3['Rank'][i]
        CSOInsight3['DublinValues'][i] = CSOInsight3['Working Proportion'][i]

    elif CSOInsight3['COUNTY'][i] == 'WD': 
        CSOInsight3['Waterford'][i] = CSOInsight3['Rank'][i]
        CSOInsight3['WaterfordValues'][i] = CSOInsight3['Working Proportion'][i]

    elif CSOInsight3['COUNTY'][i] == 'LK': 
        CSOInsight3['Limerick'][i] = CSOInsight3['Rank'][i]
        CSOInsight3['LimerickValues'][i] = CSOInsight3['Working Proportion'][i]
    
CSOInsight3.to_csv('CSOInsight3.csv', index = False)


#______________________________________________________________________________
# Insight 4
CSOClare = CSO.loc[CSO['COUNTY'] == 'CE']
CSOTipperary = CSO.loc[CSO['COUNTY'] == 'TY']
CSOKerry = CSO.loc[CSO['COUNTY'] == 'KY']
CSOMunster = pd.concat(
    [CSOKerry, CSOTipperary, CSOCork, CSOLimerick, CSOWaterford, CSOClare])
CSOMunster.sort_values('COUNTY', inplace=True)

CSOMunster['0min'] = np.nan
CSOMunster['15min'] = CSOMunster['D1']
CSOMunster['30min'] = CSOMunster['D1'] + CSOMunster['D2'] 
CSOMunster['45min'] = CSOMunster['D1'] + CSOMunster['D2'] + CSOMunster['D3'] 
CSOMunster['60min'] = CSOMunster['D1'] + CSOMunster['D2'] + CSOMunster['D3'] + CSOMunster['D4'] 
CSOMunster['90min'] = CSOMunster['D1'] + CSOMunster['D2'] + CSOMunster['D3'] + CSOMunster['D4'] + CSOMunster['D5'] 
CSOMunster['90min+'] = CSOMunster['D1'] + CSOMunster['D2'] + CSOMunster['D3'] + CSOMunster['D4'] + CSOMunster['D5'] + CSOMunster['D6']


Min0Total = 0
Min15Total = 0
Min30Total = 0
Min45Total = 0
Min60Total = 0
Min90Total = 0
Min90OverTotal = 0

CSOMunster = CSOMunster.reset_index()

for i in range(0, len(CSOMunster['15min'])):
    Min15Total += int(CSOMunster['15min'][i])
    Min30Total += int(CSOMunster['30min'][i])
    Min45Total += int(CSOMunster['45min'][i])
    Min60Total += int(CSOMunster['60min'][i])
    Min90Total += int(CSOMunster['90min'][i])
    Min90OverTotal += int(CSOMunster['90min+'][i])

CSOInsight4 = [Min0Total, Min15Total, Min30Total, Min45Total, 
               Min60Total, Min90Total, Min90OverTotal]

CSOInsight4 = pd.DataFrame(CSOInsight4, columns = ['Total People'])
CSOInsight4['Minutes'] = np.nan
CSOInsight4['Minutes'][0] = 1
for i in range(1, len(CSOInsight4['Total People'])):
    CSOInsight4['Minutes'][i] = i*15
CSOInsight4['Minutes'][5] = 90
CSOInsight4['LRx'] = np.log(CSOInsight4['Minutes'])

CSOInsight4['Minutes'][6] = 'Total People'
CSOInsight4['LRx'][6] = np.nan

#CSOInsight4.to_csv('CSOInsight4.csv', index = False)

#______________________________________________________________________________
# Insight 5

CSOInsight5Intelligence = CSO.sample(n=100,replace=False)
CSOInsight5Intelligence = CSOInsight5Intelligence.reset_index()

CSOInsight5Intelligence['Verbal Male'] = np.nan
CSOInsight5Intelligence['Numeric Male'] = np.nan
CSOInsight5Intelligence['Other Male'] = np.nan
CSOInsight5Intelligence['Verbal Female'] = np.nan
CSOInsight5Intelligence['Numeric Female'] = np.nan
CSOInsight5Intelligence['Other Female'] = np.nan
CSOInsight5Intelligence['Verbal Total'] = np.nan
CSOInsight5Intelligence['Numeric Total'] = np.nan
CSOInsight5Intelligence['Other Total'] = np.nan


CSOInsight5Intelligence['Verbal Male'] = (CSOInsight5Intelligence['HUM M'] + 
                                       CSOInsight5Intelligence['SOC M'] + 
                                       CSOInsight5Intelligence['EDU M'])
CSOInsight5Intelligence['Numeric Male'] = (CSOInsight5Intelligence['ENG M'] + 
                                           CSOInsight5Intelligence['SCI M'] + 
                                           CSOInsight5Intelligence['ART M']) 
CSOInsight5Intelligence['Other Male'] = (CSOInsight5Intelligence['AGR M '] + 
                                      CSOInsight5Intelligence['SER M'] + 
                                      CSOInsight5Intelligence['Other M.1'] +
                                      CSOInsight5Intelligence['HEA M ']) 
CSOInsight5Intelligence['Verbal Female'] = (CSOInsight5Intelligence['HUM F'] + 
                                       CSOInsight5Intelligence['SOC F'] + 
                                       CSOInsight5Intelligence['EDU F'])
CSOInsight5Intelligence['Numeric Female'] = (CSOInsight5Intelligence['ENG F'] + 
                                           CSOInsight5Intelligence['SCI F'] + 
                                           CSOInsight5Intelligence['ART F']) 
CSOInsight5Intelligence['Other Female'] = (CSOInsight5Intelligence['AGR F'] + 
                                      CSOInsight5Intelligence['SER F'] + 
                                      CSOInsight5Intelligence['Other F.1'] + 
                                      CSOInsight5Intelligence['HEA F']) 
CSOInsight5Intelligence['Verbal Total'] = (CSOInsight5Intelligence['HUM T'] + 
                                       CSOInsight5Intelligence['SOC T'] + 
                                       CSOInsight5Intelligence['EDU T '])
CSOInsight5Intelligence['Numeric Total'] = (CSOInsight5Intelligence['ENG T'] + 
                                           CSOInsight5Intelligence['SCI T'] + 
                                           CSOInsight5Intelligence['ART T']) 
CSOInsight5Intelligence['Other Total'] = (CSOInsight5Intelligence['AGR T'] + 
                                      CSOInsight5Intelligence['SER T'] + 
                                      CSOInsight5Intelligence['Other T.1'] + 
                                      CSOInsight5Intelligence['HEA T']) 


CSOInsight5Intelligence = CSOInsight5Intelligence[['Verbal Male', 'Numeric Male', 'Other Male',
                                                   'Verbal Female', 'Numeric Female', 'Other Female',
                                                   'Verbal Total', 'Numeric Total', 'Other Total']]


TotalVM = sum(CSOInsight5Intelligence['Verbal Male'])  
TotalNVM = sum(CSOInsight5Intelligence['Numeric Male'])  
TotalOM = sum(CSOInsight5Intelligence['Other Male'])
TotalVF = sum(CSOInsight5Intelligence['Verbal Female'])  
TotalNVF = sum(CSOInsight5Intelligence['Numeric Female'])  
TotalOF = sum(CSOInsight5Intelligence['Other Female'])
TotalVT = sum(CSOInsight5Intelligence['Verbal Total'])  
TotalNVT = sum(CSOInsight5Intelligence['Numeric Total'])  
TotalOT = sum(CSOInsight5Intelligence['Other Total'])

MTot = TotalVM + TotalNVM + TotalOM
FTot = TotalVF + TotalNVF + TotalOF
TTot = TotalVT + TotalNVT + TotalOT

VTot = TotalVM + TotalVF + TotalVT
NVTot = TotalNVM + TotalNVF + TotalNVT
OTot = TotalOM + TotalOF + TotalOT

Male = ['Male', TotalVM, TotalNVM, TotalOM, MTot]
Female = ['Female', TotalVF, TotalNVF, TotalOF, FTot]
Total = ['Total', TotalVT, TotalNVT, TotalOT, TTot]
CSOInsight5 = []
CSOInsight5 = pd.DataFrame(CSOInsight5, columns = ['Gender', 'Verbal', 'Numeric ', 'Other', 'Total'])

CSOInsight5.loc[len(CSOInsight5)] = Male
CSOInsight5.loc[len(CSOInsight5)] = Female
CSOInsight5.loc[len(CSOInsight5)] = Total

#CSOInsight5.to_csv('CSOInsight5.csv', index = False)

#______________________________________________________________________________


del CSOInsight2_16
del CSOCarlow
del CSOClare
del CSOCork
del CSODonegal
del CSODublin
del CSOGalway
del CSOWaterford
del CSOTipperary
del CSOMunster
del CSOLimerick
del CSOKerry
del i
del Min0Total
del Min15Total
del Min30Total
del Min45Total
del Min60Total
del Min90Total
del Min90OverTotal
del CSOSouthDublin
del CSOGalwayCity
del CSOGalwayCounty
del CSOFingal
del CSODunLaoighre
del CSODublinCity
del CSODublinCounty
del CSODonegalCarlow
del CSOCorkCounty
del CSOCorkCity
del MTot
del FTot
del TTot
del VTot
del NVTot
del Male
del Female
del Total
del TotalNVF
del TotalNVM
del TotalNVT
del TotalVF
del TotalVM
del TotalVT
del OTot
del TotalOF
del TotalOM
del TotalOT
del CSOInsight5Intelligence

