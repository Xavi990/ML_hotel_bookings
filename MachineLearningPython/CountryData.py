import pandas

def getCountries(countries_dataset_url):
    countries_df = pandas.read_csv(countries_dataset_url)
    return countries_df

def mapCountryAtributesToDF(countries_dataset_url, df):
    countryDF = getCountries(countries_dataset_url)
    df = df.merge(countryDF, how='left', left_on='country', right_on='Three_Letter_Country_Code', suffixes=(False, False))
    dummy_continent = pandas.get_dummies(df['Continent_Name'])
    df = df.merge(dummy_continent, left_index=True, right_index=True)
    df.drop(['Continent_Name', 'Continent_Code', 'Country_Name', 'Two_Letter_Country_Code', 'Three_Letter_Country_Code', 'Country_Number'], axis=1, inplace=True)
    # Se elimina la columna country
    df.drop(['country'], axis=1, inplace=True)

    return df
