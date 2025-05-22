# IMPORTACIÓN DE LIBRERÍAS Y COMPONENTES
# Importamos las mismas librerías que en el script de entrenamiento,
# ya que necesitamos realizar operaciones similares (tokenización, lematización)
# y cargar los objetos guardados.
# random Para elegir una respuesta aleatoria de la lista de respuestas posibles.
# json Para cargar el archivo de intenciones original (intents.json), que contiene las respuestas.
# pickle Para cargar nuestros objetos preprocesados (palabras y clases) desde los archivos .pkl.
# numpy Para manejar la bolsa de palabras como un array de NumPy.
# tensorflow Para cargar nuestro modelo de red neuronal entrenado.
# unicodedata Para eliminar acentos y caracteres especiales de las frases.
import random
import json
import pickle
import numpy as np
import tensorflow as tf
import unicodedata

# NLTK para procesamiento de lenguaje natural.
from nltk.stem import WordNetLemmatizer # Para reducir las palabras a su forma base (lema).
import nltk # La librería NLTK en sí.
# nltk.download('punkt', quiet=True) # No es estrictamente necesario volver a descargarlos aquí si ya se hizo en el entrenamiento
# nltk.download('wordnet', quiet=True) # y los recursos están disponibles, pero no hace daño.


def init_chatbot():
    # CARGA DE DATOS Y MODELO
    # Cargamos los artefactos que creamos y guardamos durante el entrenamiento.
    global lemmatizer, intents, words, classes, model
    lemmatizer = WordNetLemmatizer() # Creamos una instancia del lematizador.
    # Cargamos el archivo 'intents.json' para acceder a las respuestas.
    intents = json.loads(open('Backend/intents.json', encoding='utf-8').read())
    # Cargamos la lista de palabras (vocabulario) guardada. 'rb' = read binary.
    words = pickle.load(open('Backend/words.pkl', 'rb'))
    # Cargamos la lista de clases (etiquetas/tags) guardada.
    classes = pickle.load(open('Backend/classes.pkl', 'rb'))
    # Cargamos el modelo de red neuronal entrenado desde el archivo .h5.
    model = tf.keras.models.load_model('Backend/chatbot_model.h5')

init_chatbot()

#Función de normalización de texto, eliminando acentos y caracteres especiales.
def remove_accents(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

# FUNCIONES DE PREPROCESAMIENTO DE ENTRADA 
# Estas funciones preparan la frase del usuario para que el modelo pueda entenderla.
def clean_up_sentence(sentence):
    """
    Toma una frase como entrada, la tokeniza (divide en palabras)
    y lematiza cada palabra (la reduce a su forma raíz y la convierte a minúsculas).
    Devuelve una lista de palabras procesadas.
    """
    # Elimina acentos en la frase.
    sentence = remove_accents(sentence)
    # Tokeniza la frase. Ejemplo: "Hola, ¿cómo estás?" -> ["Hola", ",", "¿", "cómo", "estás", "?"]
    sentence_words = nltk.word_tokenize(sentence)
        # Lematiza cada palabra y la convierte a minúsculas.
    # Ejemplo: ["Hola", ",", "¿", "cómo", "estás", "?"] -> ['hola', 'cómo', 'estar'] (asumiendo que ',' y '?' se filtran o no están en 'words')
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    """
    Toma una frase, la procesa usando clean_up_sentence(),
    y luego la convierte en una representación de "bolsa de palabras" (bag of words).
    La bolsa de palabras es un array de 0s y 1s, donde cada posición corresponde
    a una palabra en nuestro vocabulario ('words'). Si la palabra del vocabulario
    está en la frase procesada, se marca con un 1, si no, con un 0.
    Devuelve un array de NumPy.
    """
    # Procesa la frase de entrada.
    sentence_words = clean_up_sentence(sentence)
    # Inicializa la bolsa de palabras con ceros, con una longitud igual al tamaño de nuestro vocabulario.
    bag = [0] * len(words)
    # Itera sobre cada palabra en la frase procesada del usuario.
    for w_sentence in sentence_words:
        # Itera sobre cada palabra (y su índice) en nuestro vocabulario global.
        for i, word_vocab in enumerate(words):
            # Si la palabra del vocabulario coincide con la palabra de la frase del usuario...
            if word_vocab == w_sentence:
                # ...marca la posición correspondiente en la bolsa de palabras con un 1.
                bag[i] = 1
    # Devuelve la bolsa de palabras como un array de NumPy.
    return np.array(bag)

# FUNCIÓN DE PREDICCIÓN DE INTENCIÓN
# Esta función toma la frase del usuario, la convierte en una bolsa de palabras,
# y usa el modelo entrenado para predecir la intención más probable.
def predict_class(sentence):
    """
    Toma una frase, la convierte en una bolsa de palabras,
    y utiliza el modelo entrenado para predecir la intención.
    Filtra las predicciones por debajo de un umbral de error (ERROR_THRESHOLD)
    y las ordena por probabilidad descendente.
    Devuelve una lista de diccionarios, cada uno con la 'intent' (etiqueta)
    y su 'probability' (probabilidad).
    """
    # Convierte la frase del usuario en una bolsa de palabras.
    bow = bag_of_words(sentence)
    # Hace una predicción usando el modelo. El modelo espera un array de arrays (un batch),
    # por lo que convertimos 'bow' a [bow]. El [0] al final es para obtener
    # las predicciones del primer (y único) elemento del batch.
    # 'res' será un array de probabilidades, una para cada clase.
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.30  # Umbral de confianza. Si una predicción tiene una probabilidad menor a esto, se ignora.
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # Ordena los resultados por probabilidad en orden descendente (la más probable primero).
    # `key=lambda x: x[1]` le dice a sort que use el segundo elemento de cada sublista (la probabilidad) para ordenar.
    results.sort(key=lambda x: x[1], reverse=True)
    # Prepara la lista de intenciones a devolver.
    return_list = []
    for r in results:
            # Para cada resultado filtrado y ordenado, crea un diccionario
        # con la etiqueta de la intención (obtenida de 'classes' usando el índice)
        # y la probabilidad (convertida a string).
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# FUNCIÓN PARA OBTENER RESPUESTA
# Esta función toma la lista de intenciones predichas y el JSON de intenciones original
# para seleccionar una respuesta adecuada.
def get_response(intents_list, intents_json, user_message=None):
    """
    Toma la lista de intenciones predichas (devuelta por predict_class)
    y el objeto JSON de intenciones original.
    Si la lista de intenciones está vacía (ninguna predicción superó el umbral),
    devuelve un mensaje por defecto.
    Si no, toma la intención más probable (la primera en intents_list),
    busca esa etiqueta en intents_json y elige una respuesta aleatoria
    de la lista de respuestas asociadas a esa etiqueta.
    """
    # Si no se predijo ninguna intención con suficiente confianza...
    if not intents_list:
        with open("Backend/retraining.txt", "a", encoding="utf-8") as f: # Se escribe en un documento de texto, el mensaje que no se entendió correctamente.
            f.write(user_message + "\n")
        return "No entendí tu mensaje. ¿Puedes reformularlo?" # Pregunta al usuario si puede reformular el mensaje
    
    # Si el porcentaje de predicción es muy bajo...
    if float(intents_list[0]['probability']) < 0.65:
        with open("Backend/retraining.txt", "a", encoding="utf-8") as f: # Escribe en el documento de texto el mensaje que se predijo de manera baja.
            f.write(user_message + "\n")
        
        # Obtiene la etiqueta (tag) de la intención más probable (la primera en la lista).
    tag = intents_list[0]['intent']
        # Obtiene la lista de todas las intenciones del archivo JSON original.
    list_of_intents = intents_json['intents']
        # Itera sobre cada intención en el archivo JSON.
    print(f"Predicted tag: {tag}, probability: {intents_list[0]['probability']}")
    for i in list_of_intents:
                # Si la etiqueta de la intención actual en el JSON coincide con la etiqueta predicha...
        if i['tag'] == tag:
                # ...elige una respuesta aleatoria de la lista de respuestas para esa etiqueta.
            return random.choice(i['responses'])
    # Si no se encontró respuesta:
    with open("Backend/retraining.txt", "a", encoding="utf-8") as f: # Se escribe en un documento de texto, el mensaje que no se entendió correctamente.
            f.write(user_message + "\n")
    return "Lo siento, pero creo que no tengo una respuesta para eso."


def main():
    init_chatbot()
    print ("Hola! Soy el ChatBot de asistencia de Hotel Premier. ¿En qué puedo ayudarte?") # Mensaje de bienvenida.

    # Bucle infinito para mantener la conversación.
    while True:
            # Espera la entrada del usuario.
        message = input("Tú: ") # Muestra un prompt "Tú: "
        ints = predict_class(message)    # Obtiene una respuesta basada en la intención predicha.
        res = get_response(ints, intents, user_message=message)
            # Obtiene la respuesta del chatbot.
        print(res) # Imprime la respuesta del chatbot

# BUCLE PRINCIPAL DEL CHATBOT
# Esta es la parte que interactúa con el usuario.
if __name__ == "__main__":
    main()
