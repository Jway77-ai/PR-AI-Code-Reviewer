"use client";
import { useState } from 'react';

const Chatbot: React.FC = () => {
    const [messages, setMessages] = useState<{ user: string; bot: string }[]>([]);
    const [input, setInput] = useState<string>("");

    const handleSend = async () => {
        if (!input.trim()) return; // Ignore empty messages

        const userMessage = input;
        setInput("");

        // Add user's message to chat
        setMessages(prevMessages => [...prevMessages, { user: userMessage, bot: '' }]);

        // Simulate a delay for the bot's response
        setTimeout(() => {
            // Simulate bot's response based on user message
            let botResponse = "I don't understand the question.";

            if (userMessage.toLowerCase().includes("diff")) {
                botResponse = "Here is a mock diff for your pull request.";
            } else if (userMessage.toLowerCase().includes("code quality")) {
                botResponse = "You could improve code quality by using more descriptive variable names.";
            }

            console.log("Bot Response:", botResponse); // Debugging line

            // Add bot's response to chat
            setMessages(prevMessages => [...prevMessages, { user: '', bot: botResponse }]);
        }, 1000); // 1-second delay for simulation
    };

    return (
        <div className="p-4 bg-white border border-gray-300 rounded-lg shadow-lg flex flex-col h-80">
            <div className="flex-1 overflow-y-auto p-2 space-y-2">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`p-2 rounded-lg ${msg.user ? 'bg-blue-100 text-blue-800 self-end' : 'bg-gray-200 text-gray-800 self-start'}`}
                    >
                        <p className="font-semibold">{msg.user ? 'You:' : 'Bot:'}</p>
                        <p>{msg.user || msg.bot}</p>
                    </div>
                ))}
            </div>
            <div className="flex mt-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about diffs or code quality..."
                    className="flex-1 p-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    onClick={handleSend}
                    className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                    Send
                </button>
            </div>
        </div>
    );
};

export default Chatbot;
