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

interface ApiResponse {
  [key: string]: unknown;
}

// Utility function to get the base URL
const getBaseUrl = (): string => {
  if (process.env.NODE_ENV === "development") {
    return "http://127.0.0.1:8000/api";
  }
  return (
    process.env.NEXT_PUBLIC_API_URL ||
    "https://uob-hackathon-dragons.vercel.app/api"
  );
};

// Utility function for API calls
const apiCall = async <T extends ApiResponse>(
  endpoint: string,
  method: string = "GET",
  body?: Record<string, unknown>
): Promise<T> => {
  const baseUrl = getBaseUrl();
  const url = `${baseUrl}${endpoint}`;

  const response = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      (errorData.error as string) || `HTTP error! status: ${response.status}`
    );
  }

  return response.json() as Promise<T>;
};

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
      const data = await apiCall<{ conversations: ConversationItem[] }>(
        `/pr/${prId}/conversations`
      );
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
    if (!input.trim()) return;
    setLoading(true);
    setError(null);

    const userMessage = input;
    setInput("");

    const newMessages = [...messages, { user: userMessage, bot: "" }];
    setMessages(newMessages);

    try {
      await sendConversationToAPI(userMessage, "User");

      const data = await apiCall<{ response: string }>(
        `/pr/${prId}/groq-response`,
        "POST",
        { message: userMessage }
      );
      const botResponse = data.response;

      const updatedMessages = [...newMessages, { user: "", bot: botResponse }];
      setMessages(updatedMessages);

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
      await apiCall<{ success: boolean }>(`/pr/${prId}/conversation`, "POST", {
        message,
        role,
      });
      console.log("Conversation saved successfully!");
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
            <p className="font-semibold">
              {msg.user ? "You:" : "UOB Code Reviewer:"}
            </p>
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
