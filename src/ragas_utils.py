import pandas as pd
import json
import os

def process_information():

	# Nombre del archivo de texto
	archivo_txt = os.path.join(os.path.dirname(__file__), 'questions.txt')

	# Lista para almacenar las estructuras de datos
	datos_json = []

	try:
		# Leer el contenido del archivo de texto
		with open(archivo_txt, 'r') as file:
			lines = file.readlines()

		# Procesar las líneas del archivo
		i = 0
		while i < len(lines):
			if lines[i].startswith('Question:'):
				# Extraer la pregunta y la respuesta
				question = lines[i].strip().split('Question:')[1]
				ground_truth = lines[i + 1].strip().split('Answer:')[1]

				# Crear el diccionario con la estructura requerida
				dato = {
					"question": question,
					"answer": "",
					"contexts": [""],  
					"ground_truth": ground_truth
				}

				# Agregar el diccionario a la lista
				datos_json.append(dato)

				# Moverse al siguiente par de líneas (Question y Answer)
				i += 2

			else:
				i += 1

		# Convertir a DataFrame de Pandas
		df = pd.DataFrame(datos_json)
		
		return df
	
	except Exception as e:
		print(f"Unexpected error: {str(e)}")
		return None

def create_ragas_data_file(df):
	# Nombre de la carpeta que deseas crear
	file_name = "data.json"

	# Ruta completa de la carpeta
	file_path = os.path.join(os.path.dirname(__file__), file_name)

	json_output = df.to_dict(orient='records')

	try: 
		# Si se desea guardar el JSON en un archivo
		with open(file_path, 'w') as json_file:
			json.dump(json_output, json_file, indent=4)
		print("The data.json file was created successfully")
	except Exception as e:
		print("Error when trying to create data.json file")