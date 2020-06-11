import pandas
import datetime

def mapDateAttributes(df):
    # Se crea una nueva columna con la fecha arrival_date en datetime
    df['arrival_date'] = df.apply(get_date, axis = 1)

    # Se quitan del dataset las columnas arrival date que vienen particionadas
    df.drop(['arrival_date_year', 'arrival_date_month', 'arrival_date_day_of_month', 'arrival_date_week_number'], axis=1, inplace=True)

    # Se calcula la cantidad de dias en la que se produce el cancelamiento respecto a la fecha esperada de arrival
    df['cancel_days_before_arrival'] = df.apply(calcula_dias_anticipo_cancelamiento, axis=1)

    # Se crean columnas dummies para los meses de arrival_date
    # Estas pueden servir para establecer temporadas de tendencias, como ser el pais de origen, los
    dummy_arrival_month = pandas.get_dummies(df['arrival_date'].apply(lambda x: 'arrival_month_' + str(x.month)))
    df = df.merge(dummy_arrival_month, left_index=True, right_index=True)

    # TODO eliminar las variables fecha reservation_status_date	arrival_date
    df.drop(['reservation_status_date', 'arrival_date'], axis=1, inplace=True)

    return df

# Funcion que toma el mes en nombre y devuelve el numero de mes calendario entre 1 y 12
def get_month_num(month_name):
    month_dicc = \
        {'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12}
    return month_dicc[month_name]

# Funcion que toma la tres componentes de la fecha segun dataset en uso y devuelve la fecha en datetime.
def get_date(df):
    return datetime.datetime( \
        int(df['arrival_date_year']),
        int(get_month_num(df['arrival_date_month'])), \
        int(df['arrival_date_day_of_month']))

def calcula_dias_anticipo_cancelamiento(df):
    if df['is_canceled'] == 1:
        return (df['arrival_date'] - df['reservation_status_date']).days
    else:
        return 0

