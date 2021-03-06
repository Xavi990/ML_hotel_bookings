import CountryData
import DateMng

import pandas

def LoadAndPreprocessDataFrame(original_dataset_url, countries_dataset_url):
    # Carga del dataset original
    booking_dataset = pandas.read_csv(original_dataset_url, parse_dates=['reservation_status_date'])

    # Se eliminan registros duplicados
    booking_dataset.drop_duplicates(keep=False, inplace=True)

    # Se ajustan las variables fecha del dataset
    booking_dataset = DateMng.mapDateAttributes(booking_dataset)

    # Se ajustan los atributos country
    booking_dataset = CountryData.mapCountryAtributesToDF(countries_dataset_url, booking_dataset)

    # Se convierte en variable binaria el atributo agent
    booking_dataset['agent'].fillna(0, inplace=True)
    booking_dataset['agent_b'] = booking_dataset['agent'].apply(lambda x: 1 if x > 0 else 0)
    booking_dataset.drop(['agent'], axis=1, inplace=True)

    # Se convierte en variable binaria el atributo company
    booking_dataset['company'].fillna(0, inplace=True)
    booking_dataset['company_b'] = booking_dataset['company'].apply(lambda x: 1 if x > 0 else 0)
    booking_dataset.drop(['company'], axis=1, inplace=True)
    
     ## valores faltantes 
    
    # variable children 4 registros null
    # lo reemplazamos por cero
    booking_dataset['children'].fillna(0, inplace=True)
    
    # variables con valores undefined
    # variale meal, reemplazo por la moda
    meal_moda= booking_dataset.meal.mode()
    booking_dataset['meal'] = booking_dataset['meal'].apply(lambda x: meal_moda[0] if x =="Undefined" else x)
 
    #variable market segment, reemplazo con la moda
    market_segment_moda= booking_dataset.market_segment.mode()
    booking_dataset['market_segment'] = booking_dataset['market_segment'].apply(lambda x: market_segment_moda[0] if x =="Undefined" else x)

    #variable ditribution_channel, reemplazo con la moda
    ditribution_channel_moda= booking_dataset.distribution_channel.mode()
    booking_dataset['distribution_channel'] = booking_dataset['distribution_channel'].apply(lambda x: ditribution_channel_moda[0] if x =="Undefined" else x)
    
    ## fin valores faltantes
    
    

    # Se convierte a variables dummies
    booking_dataset = addDummiesInDataFrame(booking_dataset, 'meal', 'meal_')
    booking_dataset = addDummiesInDataFrame(booking_dataset, 'market_segment', 'market_seg_')
    booking_dataset = addDummiesInDataFrame(booking_dataset, 'distribution_channel', 'dist_channel_')
    booking_dataset = addDummiesInDataFrame(booking_dataset, 'deposit_type', 'deposit_')
    booking_dataset = addDummiesInDataFrame(booking_dataset, 'customer_type', 'cust_type_')
    
    ## outliers de adr
    
    # ver qué asignamos a los outliers o valores que no tienen sentido???
    # habria que ver si lo queremos hacer y si sirve lo que hice abajo
    # pongo cero a los que serían valores incorrectos, por ser menores a 1 y mayor a 5000 
    # y luego los reemplazo por la media
    booking_dataset['adr'] = booking_dataset['adr'].apply(lambda x: 0 if x < 1  or x > 5000 else x)
    mean_adr = booking_dataset.adr.mean()
    booking_dataset['adr'] = booking_dataset['adr'].apply(lambda x: mean_adr if x == 0  else x)
    
    ## fin outliers adr

    # Variable adr se calcula la relacion por huesped. Los menores se los consiera a la mitad. Los babies no se toman para el calculo
    booking_dataset['adr_por_persona'] = booking_dataset.apply(lambda x: float(x['adr']) / (float(x['adults']) + 0.5 * float(x['children'])) if (float(x['adults']) + 0.5 * float(x['children'])) > 0 else 0, axis=1)

    #print(original_dataset.head())
    #original_dataset.info()
    #print(original_dataset.shape)
    #original_dataset.drop_duplicates(inplace=True)
    #print(original_dataset.columns)
    #for i in original_dataset:
    #    print (i)
    #print(original_dataset.isnull().sum())
    #original_dataset.describe()

    # Eliminacion de columnas
    # Se elimina variable 'hotel' para permitir generalizar para otros hoteles, no especificamente los del dataset
    # Se elimina variable 'reservation_status' por no ser una variable de entrada, sino una de salida a predecir compatible con 'is_canceled'
    # Se eliminan las variables 'reserved_room_type' y 'assigned_room_type' por no tener en claro que significa cada categoria,
    #   si son categoricas ordinales, o sin simplemente ID. Tampoco si el huespues conoce el valor de 'assigned_room_type'
    #   antes del check in
    booking_dataset.drop(['hotel', 'reservation_status', 'reserved_room_type', 'assigned_room_type'], axis=1, inplace=True)
    
     
    

    return booking_dataset


def addDummiesInDataFrame(df_aux, attribute, namePrefix):
    dummy_attribute = pandas.get_dummies(df_aux[attribute].apply(lambda x: namePrefix + str(x)))
    df_aux = df_aux.merge(dummy_attribute, left_index=True, right_index=True)
    df_aux.drop([attribute], axis=1, inplace=True)
    return df_aux
