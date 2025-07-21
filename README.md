# 🤖 Hotel Premier Chatbot.
## Español:
The following content is in Spanish, if you want to read the readme in English, scroll down to the English section.  
El siguiente contenido está en Español, si desea leer el readme en Inglés, desplace hacia abajo a la sección en Inglés.
## 📝 Descripción.
Un chatbot inteligente para servicio al cliente hotelero desarrollado con **Flask**, **Tensorflow** y tecnologías web modernas. El sistema procesa consultas en **español** en tiempo real y proporciona respuestas automatizadas para preguntas comunes sobre reservas, servicios, ubicación y políticas del hotel.
## 🚀 Características principales.
- Procesamiento en lenguaje natural: Comprende y responde consultas de huéspedes en idioma español.
- Clasificación de Intenciones: Categoriza mensajes en 23 tipos de consultas hoteleras predefinidas.
- Interfáz de chat en tiempo real: Experiencia de chat web interactiva con animaciones de escritura.
- Aprendizaje continuo: registra automáticamente interacciones fallidas para mejorar el modelo.
- Generación de respuestas comerciales: Selecciona respuestas apropiadas de plantillas predefinidas.
## 🏗️ Arquitectura del sistema.
Frontend (HTML/JS/CSS) --> Flask App --> AI Processing --> ML Mpdel Assets --> Continuous Learning System.
## 📁 Estructura del proyecto.
hotel-chatbot/  
├── Backend/  
│ ├── chatbot.py # Motor de procesamiento de IA  
│ ├── chatbot_model.h5 # Modelo de red neuronal entrenado  
│ ├── words.pkl # Vocabulario procesado  
│ ├── classes.pkl # Etiquetas de intenciones  
│ ├── intents.json # Plantillas de respuestas  
│ └── retraining.txt # Log de consultas fallidas  
├── Frontend/  
│ ├── templates/  
│ │ └── index.html # Interfaz de chat  
│ └── static/  
│ ├── js/script.js # Lógica del frontend  
│ └── css/style.css # Estilos y animaciones  
└── app.py # Servidor Flask principal  
## 🔧 Tecnologías usadas:
- Backend: Flask 2.x, TensorFlow 2.x, NLTK, NumPy.
- Frontend: HTML5, TailwindCSS, JavaScript Vanilla.
- ML/AI: Redes neuronales para clasificación de intenciones.
- Datos: JSON, Pickle, archivos de texto para logging.
## 💬 Funcionalidades:
El chatbot puede responder consultas sobre:  
- 🕑 Reservaciones y disponibilidad.
- 🛎️ Servicios del hotel.
- 📍 Ubicación y direcciones.
- ☀️ Horarios de chack-in / check-out.
- 🚨 Políticas del hotel.
- 🤑 Métodos de pago.
- ❌ Cancelaciones.
- ✅ Promos y ofertas.
- 👨‍🍳 Restaurante y servicio a la habitación.
- 🚕 Transporte.
- 🛏️ Tipos de habitaiones.
- 🎊 Eventos y salones.
- ✅ Accesibilidad.
- ❓ Objetos perdidos.
- 🩺 Servicios médicos.
## 🧠 Sistema de Aprendizaje Continuo.
El chatbot incluye un mecanismo de mejora continua que:  
- Registra consultas con baja confianza en retraining.txt.
- Permite el reentrenamiento del modelo con nuevos datos.
- Mejora la precisión de respuestas con el tiempo y uso.
## 🌊 Flujo de procesamiento.
1.- Usuario envía mensaje en español.  
2.- Preprocesamiento de texto (eliminar acentos, tokenización, lematización).  
3.- Conversión a vector numérico (bag of words).  
4.- Clasificación de interacciónusando red neuronal.  
5.- Selección de respuesta apropiada.  
6.- Logging de consultas fallidas para aprendizaje.
## 🤝 Contribuidores.
- Gustavo Cortés (Seeker-17).
- Angel Sánchez (NoisyArchie).
- Sebastián Chapa (Chapinguin).
## 📞 Contacto.
Para cualquier duda o comentario no dude en contactarme al 844 140 6339 o por medio de mi correo electrónico gustavocortes@gmail.com

---
# 🤖 Hotel Premier Chatbot.
## English:
El siguiente contenido está en Inglés, si desea leer el readme en español, desplace hacia arriba a la sección en Español.  
The following content is in English, if you wish to read the readme in Spanish, scroll up to the Spanish section.
## 📝 Desciption.
An intelligent chatbot for hotel customer service developed with Flask, TensorFlow, and modern web technologies. The system processes queries in Spanish in real time and provides automated responses to common questions about reservations, services, location, and hotel policies.
## 🚀 Key Features.
- Natural Language Processing: Understands and responds to guest queries in Spanish
- Intent Classification: Categorizes messages into 23 predefined types of hotel-related queries.
- Continuous Learning: Automatically logs failed interactions to improve the model.
- Business-Oriented Response Generation: Selects appropriate responses from predefined templates.
## 🏗️ System Architecture.
Frontend (HTML/JS/CSS) --> Flask App --> AI Processing --> ML Mpdel Assets --> Continuous Learning System.
## 📁 Project Structure.
hotel-chatbot/  
├── Backend/  
│ ├── chatbot.py # AI proccessing engine  
│ ├── chatbot_model.h5 # Trained neural network model  
│ ├── words.pkl # Processed vocabulary  
│ ├── classes.pkl # Intent labels  
│ ├── intents.json # Response templates  
│ └── retraining.txt # Log of failed queries  
├── Frontend/  
│ ├── templates/  
│ │ └── index.html # Chat interface  
│ └── static/  
│ ├── js/script.js # Frontend logic  
│ └── css/style.css # Styles and animations  
└── app.py # Main Flask Server  
## 🔧 Used Technologies:
- Backend: Flask 2.x, TensorFlow 2.x, NLTK, NumPy.
- Frontend: HTML5, TailwindCSS, JavaScript Vanilla.
- ML/AI: Neural networks for intent classification.
- Datos: JSON, Pickle, text files for logging.
## 💬 Functionality:
The chatbot can respond to questions about:  
- 🕑 Reservations and availability.
- 🛎️ Hotel services.
- 📍 Location and directions.
- ☀️ Check-in / check-out times.
- 🚨 Hotel policies.
- 🤑 Payment methods.
- ❌ Cancellations.
- ✅ Promotions and offers.
- 👨‍🍳 Restaurant and room service.
- 🚕 Transportation.
- 🛏️ Room types.
- 🎊 Events and meeting rooms.
- ✅ Accessibility.
- ❓ Lost and found.
- 🩺 Medical services.
## 🧠 Continuous Learning System.
The chatbot includes a continuous improvement mechanism that:  
- Logs low-confidence queries in retraining.txt
- Allows model retraining with new data
- Improves response accuracy over time and usage
## 🌊 Processing Flow.
1.- User sends a message in Spanish.  
2.- Text preprocessing (remove accents, tokenization, lemmatization).  
3.- Conversion to numeric vector (bag of words).  
4.- Interaction classification using neural network.  
5.- Selection of appropriate response.  
6.- Logging of failed queries for learning.  
## 🤝 Contributors.
- Gustavo Cortés (Seeker-17).
- Angel Sánchez (NoisyArchie).
- Sebastián Chapa (Chapinguin).
## 📞 Contact.
For any questions or comments, feel free to contact me at 844 140 6339 or via email at gustavocortes@gmail.com
