import pandas
import PreprocessDataSet

def getCountries(countries_dataset_url):
    countries_df = pandas.read_csv(countries_dataset_url)
    return countries_df

def mapCountryAtributesToDF(countries_dataset_url, df):
    # Levanta el dataset de definicion de countries y lo agrega al df booking de acuerdo al country code.
    countryDF = getCountries(countries_dataset_url)
    df = df.merge(countryDF, how='left', left_on='country', right_on='Three_Letter_Country_Code', suffixes=(False, False))

    # se reemplazan los valores nulos por la moda 'Europe'
    continente_moda = df['Continent_Name'].mode()
    df['Continent_Name'].fillna(continente_moda[0], inplace=True)
    
    # Convierte la variables countries en dummies
    df = PreprocessDataSet.addDummiesInDataFrame(df, 'Continent_Name', 'continent_')

    df.drop(['Continent_Code', 'Country_Name', 'Two_Letter_Country_Code', 'Three_Letter_Country_Code', 'Country_Number'], axis=1, inplace=True)

    # Se elimina la columna country
    df.drop(['country'], axis=1, inplace=True)

    
    
    return df
