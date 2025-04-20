/**
 * HR Policy Chatbot - Client-side JavaScript
 * 
 * This script handles the chat interface functionality including:
 * - Sending user messages to the backend API
 * - Displaying user and bot messages
 * - Managing typing indicators and UI interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    
    // Scroll to the bottom of the chat container
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Display a user message in the chat
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('user-message');
        messageElement.innerHTML = `
            <div class="message-content">
                <p>${escapeHTML(message)}</p>
            </div>
        `;
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Display a bot message in the chat
    function addBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('bot-message');
        
        // Replace newlines with paragraph breaks for better formatting
        const formattedMessage = message
            .split('\n')
            .filter(line => line.trim() !== '')
            .map(line => `<p>${escapeHTML(line)}</p>`)
            .join('');
        
        messageElement.innerHTML = `
            <div class="message-content">
                ${formattedMessage}
            </div>
        `;
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Show the typing indicator
    function showTypingIndicator() {
        typingIndicator.classList.remove('d-none');
        scrollToBottom();
    }
    
    // Hide the typing indicator
    function hideTypingIndicator() {
        typingIndicator.classList.add('d-none');
    }
    
    // Escape HTML special characters to prevent XSS
    function escapeHTML(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // Display user message
        addUserMessage(message);
        
        // Clear input field
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Send message to backend API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            // Check if the response is successful
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            
            // Parse the response JSON
            const data = await response.json();
            
            // Hide typing indicator
            hideTypingIndicator();
            
            // Display bot response
            if (data.error) {
                addBotMessage(`عذراً، حدث خطأ: ${data.error}`);
            } else {
                addBotMessage(data.response);
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            
            // Hide typing indicator
            hideTypingIndicator();
            
            // Display error message
            addBotMessage('عذراً، حدث خطأ أثناء معالجة طلبك. الرجاء المحاولة مرة أخرى لاحقاً.');
        }
    });
    
    // Allow submitting the form with Ctrl+Enter or Command+Enter
    userInput.addEventListener('keydown', function(event) {
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
    
    // Focus the input field when the page loads
    userInput.focus();
    
    // Initial scroll to bottom
    scrollToBottom();
});
