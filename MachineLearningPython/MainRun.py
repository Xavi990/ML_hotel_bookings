

import PreprocessDataSet

### PARAMETROS
# Rutas de los datasets
original_dataset_url = "E:/GoogleDrive/Maestria_DataMining/Aprendizaje Automatico (Lunes)/TP1/datasets/hotel_bookings.csv"
preprocessed_dataset_url = "E:/GoogleDrive/Maestria_DataMining/Aprendizaje Automatico (Lunes)/TP1/datasets/hotel_bookings_preprocessed.csv"
countries_dataset_url = "E:/GoogleDrive/Maestria_DataMining/Aprendizaje Automatico (Lunes)/TP1/datasets/country-and-continent-codes-list.csv"


# Se ejecuta el preprocesamiento del DataSet
booking_dataset = PreprocessDataSet.LoadAndPreprocessDataFrame(original_dataset_url, countries_dataset_url)

# Se guarda el dataset procesado
booking_dataset.to_csv(preprocessed_dataset_url, sep=',', encoding='utf-8')
