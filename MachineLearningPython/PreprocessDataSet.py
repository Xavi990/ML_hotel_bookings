import CountryData
import DateMng

import pandas

def LoadAndPreprocessDataFrame(original_dataset_url, countries_dataset_url):
    # Carga del dataset original
    booking_dataset = pandas.read_csv(original_dataset_url, parse_dates=['reservation_status_date'])

    # Se llama a la libreria de fechas para ajustar el dataset
    booking_dataset = DateMng.mapDateAttributes(booking_dataset)

    # Se llama a la libreria de countries para manejo de atributos country
    booking_dataset = CountryData.mapCountryAtributesToDF(countries_dataset_url, booking_dataset)

    # Eliminacion de columnas
    # Se elimina variable 'hotel' para permitir generalizar para otros hoteles, no especificamente los del dataset
    # Se elimina variable 'reservation_status' por no ser una variable de entrada, sino una de salida a predecir compatible con 'is_canceled'

    booking_dataset.drop(['hotel', 'reservation_status'], axis=1, inplace=True)

    # Se convierte en variable binaria el atributo agent
    booking_dataset['agent'].fillna(0, inplace=True)
    booking_dataset['agent_b'] = booking_dataset['agent'].apply(lambda x: 1 if x > 0 else 0)
    booking_dataset.drop(['agent'], axis=1, inplace=True)

    # Se convierte en variable binaria el atributo company
    booking_dataset['company'].fillna(0, inplace=True)
    booking_dataset['company_b'] = booking_dataset['company'].apply(lambda x: 1 if x > 0 else 0)
    booking_dataset.drop(['company'], axis=1, inplace=True)


    #TODO confirmar que campo adr es el valor de la reserva, si es por dia o por el total.
    #TODO generar campo nuevo de valor de reserva por noche
    #TODO generar campo nuevo de valor de reserva por persona
    #TODO separar un test data set con el 20% y dejar el 80% para traininig/validation
    #TODO armar las 50 particiones del 80% restante con una propocion 80%/20% traininig/validation con 50 semillas distintas

    #print(original_dataset.head())
    #original_dataset.info()
    #print(original_dataset.shape)
    #original_dataset.drop_duplicates(inplace=True)
    #print(original_dataset.columns)
    #for i in original_dataset:
    #    print (i)
    #print(original_dataset.isnull().sum())
    #original_dataset.describe()

    return booking_dataset
