document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const quickButtons = document.querySelectorAll('.quick-button'); // Or whatever class you use for quick reply buttons
    let isTyping = false;

    // Función para añadir mensajes al chat
    function addMessage(text, sender, isQuickReply = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', '${sender}-message');

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = text;

        const timeDiv = document.createElement('div');
        timeDiv.classList.add('message-time');
        timeDiv.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Función para mostrar "escribiendo..."
    function showTypingIndicator() {
        if (isTyping) return;
        
        isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing');
        typingDiv.id = 'typing-indicator';
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content', 'typing-content');
        
        // Puntos de animación
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            dot.classList.add('typing-dot');
            contentDiv.appendChild(dot);
        }
        
        typingDiv.appendChild(contentDiv);
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Función para ocultar "escribiendo..."
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        isTyping = false;
    }

    // Función para enviar mensaje al backend
    async function sendMessageToBackend(message) {
        try {
            showTypingIndicator();
            
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok){
                throw new Error('Error HTTP: ${response.status}');
            }
            
            const data = await response.json();
            console.log("Respuesat del Backend:", data);
            
            // Procesar respuesta del bot
            hideTypingIndicator();
            if (data.response) {
                addMessage(data.response, 'bot');
            } else {
                throw new Error("Respuesta inesperada del servidor")
            }
        } catch (error) {
            hideTypingIndicator();
            addMessage("Lo siento, estoy teniendo problemas para conectarme. Por favor intenta nuevamente.", 'bot');
            console.error('Error:', error);
        }
    }

    // Función para manejar el envío de mensajes
    function handleSendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            userInput.value = '';
            sendMessageToBackend(message);
        }
    }

    // Event Listeners
    sendButton.addEventListener('click', handleSendMessage);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });

    // Botones de acción rápida
    quickButtons.forEach(button => {
        button.addEventListener('click', function() {
            const message = this.getAttribute('data-message');
            addMessage(message, 'user', true);
            sendMessageToBackend(message);
        });
    });

    // Efecto de enfoque automático en el input
    userInput.focus();

    // Mensaje de bienvenida inicial (opcional)
    setTimeout(() => {
        addMessage("Puedo ayudarte con reservas, información de habitaciones, servicios del hotel y más. ¿En qué necesitas ayuda?", 'bot');
    }, 1000);
});