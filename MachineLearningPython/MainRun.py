import PreprocessDataSet

### PARAMETROS
# Rutas de los datasets
local_base_path = "E:/GoogleDrive/Maestria_DataMining/Aprendizaje Automatico (Lunes)/TP1/GitHub"
original_dataset_url = local_base_path + "/datasets/hotel_bookings.csv"
preprocessed_dataset_url = local_base_path + "/datasets/hotel_bookings_preprocessed.csv"
countries_dataset_url = local_base_path + "/datasets/country-and-continent-codes-list.csv"


# Se ejecuta el preprocesamiento del DataSet
booking_dataset = PreprocessDataSet.LoadAndPreprocessDataFrame(original_dataset_url, countries_dataset_url)

# TODO separar un test data set con el 20% y dejar el 80% para traininig/validation
# TODO armar las 50 particiones del 80% restante con una propocion 80%/20% traininig/validation con 50 semillas distintas
# TODO Entrenar el arbol, validar, testear

# Se guarda el dataset procesado
booking_dataset.to_csv(preprocessed_dataset_url, sep=',', encoding='utf-8')
