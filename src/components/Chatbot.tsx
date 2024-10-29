"use client";
import { useCallback, useEffect, useRef, useState } from "react";

interface Props {
  prId: string;
}

interface ConversationItem {
  id: number;
  message: string;
  date_created: string;
  role: string;
}

interface Message {
  content: string;
  role: string;
}

interface ApiResponse {
  [key: string]: unknown;
}

const getBaseUrl = (): string => {
  if (process.env.NODE_ENV === "development") {
    return "http://127.0.0.1:8000/api";
  }
  return (
    process.env.NEXT_PUBLIC_API_URL || "https://pr-ai-code-reviewer.vercel.app"
  );
};

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

// Function to escape HTML in code blocks
const escapeHtml = (str: string) => {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
};

// Extended markdown parser to handle code blocks with styling
const parseMarkdown = (text: string) => {
  // Replace code blocks ```code``` with styled <pre><code> block
  text = text.replace(
    /```([\s\S]*?)```/g,
    (match, p1) =>
      `<pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto"><code>${escapeHtml(
        p1
      )}</code></pre>`
  );

  // Replace inline code `code` with <code> and escape HTML
  text = text.replace(
    /`([^`]+)`/g,
    (match, p1) => `<code>${escapeHtml(p1)}</code>`
  );

  // Replace bold syntax **bold** with <strong>bold</strong>
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Replace italics syntax *italic* with <em>italic</em>
  text = text.replace(/\*(.*?)\*/g, "<em>$1</em>");

  // Replace line breaks with <br />
  text = text.replace(/\n/g, "<br />");

  return text;
};

const Chatbot: React.FC<Props> = ({ prId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const messageEndRef = useRef<HTMLDivElement | null>(null); // Ref for scrolling

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
          content: conv.message,
          role: conv.role.toLowerCase(),
        })
      );
      setMessages(formattedMessages);
    } catch (error) {
      console.error("Error fetching conversation history:", error);
      setError("Failed to fetch conversation history. Please try again.");
    }
  }, [prId]);

  useEffect(() => {
    fetchConversationHistory();
  }, [fetchConversationHistory, prId]);

  useEffect(() => {
    // Scroll to bottom whenever messages change
    if (messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError(null);

    const userMessage = input;
    setInput("");

    const newMessages = [...messages, { content: userMessage, role: "user" }];
    setMessages(newMessages);

    try {
      await sendConversationToAPI(userMessage, "User");

      const data = await apiCall<{ response: string }>(
        `/pr/${prId}/groq-response`,
        "POST",
        { message: userMessage }
      );
      const botResponse = data.response;

      const updatedMessages = [
        ...newMessages,
        { content: botResponse, role: "system" },
      ];
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
    <div className="flex flex-col h-full">
      {error && <div className="text-red-500 mb-2">{error}</div>}
      <div className="flex-1 overflow-y-auto p-2 space-y-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-2 rounded-lg ${
              msg.role === "user"
                ? "bg-blue-100 text-blue-800 self-end"
                : "bg-gray-200 text-gray-800 self-start"
            }`}
          >
            <p className="font-semibold">
              {msg.role === "user" ? "You:" : "UOB Code Reviewer:"}
            </p>
            <p
              dangerouslySetInnerHTML={{ __html: parseMarkdown(msg.content) }}
            ></p>
          </div>
        ))}
        <div ref={messageEndRef} /> {/* Ref to scroll to the bottom */}
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
