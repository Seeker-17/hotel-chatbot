from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

base_dir = os.path.abspath(os.path.dirname(__file__))

from Backend.chatbot import predict_class, get_response
import Backend.chatbot

app = Flask(__name__,
            static_folder=os.path.join(os.path.dirname(__file__), 'Frontend', 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), 'Frontend', 'templates'))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    print(f"Ruta a templates: {app.template_folder}")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not request.is_json:
        return jsonify({"error": "Se esperaba JSON"}), 400

    try:
        data = request.get_json()
        user_message = data.get('message')
        print(f"Mensaje recibido: {user_message}")  # Debug
        
        if not user_message:
            return jsonify({'response': 'No se recibió mensaje', 'status': 'error'}), 400
        
        ints = predict_class(user_message)
        bot_response = get_response(ints, Backend.chatbot.intents, user_message)
        
        print(f"Respuesta generada: {bot_response}")  # Debug
        return jsonify({'response': bot_response, 'status': 'success'})
        
    except Exception as e:
        print(f"Error completo: {str(e)}")
        return jsonify({'response': 'Error interno del servidor', 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug = True, port=5000)