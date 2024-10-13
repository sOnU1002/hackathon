document.getElementById('send-button').addEventListener('click', sendMessage);

function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (message) {
        displayMessage(message, 'user');
        input.value = '';

        // Send the message to the Flask backend
        fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message }),
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function displayMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
    messageDiv.textContent = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}
