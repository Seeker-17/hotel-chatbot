document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    let isTyping = false;

    // Función para añadir mensajes al chat
    function addMessage(text, sender, isQuickReply = false) {
        const messageDiv = document.createElement('div');
        const isUser = sender === 'user';

        // Set classes for user or bot
        messageDiv.className =
        `message ${isUser ? 'user-message self-end bg-blue-600 text-white' : 'bot-message self-start bg-white text-[#333]'} shadow-md rounded-[18px] ${isUser ? 'rounded-br-[5px]' : 'rounded-bl-[5px]'} p-4 max-w-[80%] flex flex-col`;

        // Message text
        const textDiv = document.createElement('div');
        textDiv.textContent = text;

        // Time
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time text-xs text-gray-400 mt-1 text-right';
        timeDiv.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});

        messageDiv.appendChild(textDiv);
        messageDiv.appendChild(timeDiv);

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Función para mostrar "escribiendo..."
    function showTypingIndicator() {
        if (isTyping) return;
        
        isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('flex', 'justify-start', 'my-2');
        typingDiv.id = 'typing-indicator';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'bg-gray-200 text-gray-800 px-4 py-2 rounded-lg max-w-[75%] text-sm shadow flex items-center';
        
        // Puntos de animación
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            dot.classList.add('typing-dot', 'w-2', 'h-2', 'bg-gray-600', 'rounded-full', 'mx-1', 'inline-block');
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
                throw new Error(`Error HTTP: ${response.status}`);
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
    //quickButtons.forEach(button => {
    //    button.addEventListener('click', function() {
    //        const message = this.getAttribute('data-message');
    //        addMessage(message, 'user', true);
    //        sendMessageToBackend(message);
    //    });
    //});

    // Efecto de enfoque automático en el input
    userInput.focus();

    // Mensaje de bienvenida inicial (opcional)
    setTimeout(() => {
        addMessage("¡Hola! ¿En que puedo ayudarte hoy?", 'bot');
    }, 1000);
});