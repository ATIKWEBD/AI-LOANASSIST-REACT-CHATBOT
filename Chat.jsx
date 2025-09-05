import { useState } from 'react';
import './styles.css'; // Import the stylesheet

function Chat() {
    const [chatMessages, setChatMessages] = useState([
        { text: "Hello! How can I help you with your loan inquiry today?", sender: "bot" }
    ]);
    const [userInput, setUserInput] = useState('');

    const handleSend = async (e) => {
        e.preventDefault();
        if (userInput.trim() === '') return;

        // Add user message to state
        const userMessage = { text: userInput, sender: "user" };
        const updatedMessages = [...chatMessages, userMessage];
        setChatMessages(updatedMessages);
        setUserInput(''); // Clear input field

        try {
            // Send the query to your FastAPI backend
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: userMessage.text }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Add bot's response to state
            const botMessage = { text: data.response, sender: "bot" };
            setChatMessages([...updatedMessages, botMessage]);

        } catch (error) {
            console.error('Error:', error);
            const errorMessage = { text: "Sorry, something went wrong. Please try again.", sender: "bot" };
            setChatMessages([...updatedMessages, errorMessage]);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h3>LoanAssist Chatbot</h3>
            </div>
            <div className="chat-box">
                {chatMessages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}-message`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <form className="chat-form" onSubmit={handleSend}>
                <input
                    type="text"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    placeholder="Type your question..."
                    required
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
}

export default Chat;