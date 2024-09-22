"use client";
import { useEffect, useState, useCallback } from "react";

interface Props {
  prId: string;
}

interface ConversationItem {
  id: number;
  message: string;
  date_created: string;
}

interface Message {
  user: string;
  bot: string;
}

const Chatbot: React.FC<Props> = ({ prId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchConversationHistory = useCallback(async () => {
    if (!prId) {
      console.error("Cannot fetch conversation history: No PR ID provided");
      setError("No PR ID available. Unable to fetch conversation history.");
      return;
    }
    setError(null);
    try {
      const response = await fetch(
        `https://uob-hackathon-dragons.vercel.app/api/pr/${prId}/conversations`
      );
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to fetch conversation history");
      }

      const formattedMessages: Message[] = data.conversations.map(
        (conv: ConversationItem) => ({
          user: conv.message,
          bot: "",
        })
      );

      setMessages(formattedMessages);
    } catch (error) {
      console.error("Error fetching conversation history:", error);
      setError("Failed to fetch conversation history. Please try again.");
    }
  }, [prId]);

  useEffect(() => {
    console.log("Current prId:", prId); // For debugging
    fetchConversationHistory();
  }, [fetchConversationHistory, prId]);

  const handleSend = async () => {
    if (!input.trim()) return; // Ignore empty messages
    setLoading(true);
    setError(null);

    const userMessage = input;
    setInput("");

    // Add user's message to chat
    const newMessages = [...messages, { user: userMessage, bot: "" }];
    setMessages(newMessages);

    try {
      // Save user message
      await sendConversationToAPI(userMessage, "User");

      // Send user message to Flask API to get the bot response
      const response = await fetch(
        `https://uob-hackathon-dragons.vercel.app/api/pr/${prId}/groq-response`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: userMessage, prId: prId }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to get response from API.");
      }

      const botResponse = data.response;

      // Add bot's response to chat
      const updatedMessages = [...newMessages, { user: "", bot: botResponse }];
      setMessages(updatedMessages);

      // Save bot response
      await sendConversationToAPI(botResponse, "System");
    } catch (error) {
      console.error("Error fetching bot response:", error);
      setError(
        `Error: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !loading) {
      handleSend();
    }
  };

  const sendConversationToAPI = async (message: string, role: string) => {
    try {
      const response = await fetch(
        `https://uob-hackathon-dragons.vercel.app/api/pr/${prId}/conversation`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message, role }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.error(
          "Error saving conversation:",
          response.status,
          data.message
        );
        throw new Error(data.message || "Failed to save conversation");
      } else {
        console.log("Conversation saved successfully!");
      }
    } catch (err) {
      console.error("Error sending conversation to API:", err);
      throw err;
    }
  };

  return (
    <div className="p-4 bg-white border border-gray-300 rounded-lg shadow-lg flex flex-col h-80">
      {error && <div className="text-red-500 mb-2">{error}</div>}
      <div className="flex-1 overflow-y-auto p-2 space-y-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-2 rounded-lg ${
              msg.user
                ? "bg-blue-100 text-blue-800 self-end"
                : "bg-gray-200 text-gray-800 self-start"
            }`}
          >
            <p className="font-semibold">{msg.user ? "You:" : "Bot:"}</p>
            <p>{msg.user || msg.bot}</p>
          </div>
        ))}
      </div>
      <div className="flex mt-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about diffs or code quality..."
          className="flex-1 p-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <button
          onClick={handleSend}
          className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
