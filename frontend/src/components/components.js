import React, { useState, useEffect } from "react";

const API_URL = "http://localhost:5005/show?channel=http%253A//localhost%253A5001";

export default function Client() {
  // State variables for messages, user input, and username
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [username, setUsername] = useState(localStorage.getItem("username") || "");
  const [isUsernameSet, setIsUsernameSet] = useState(!!localStorage.getItem("username"));
  const [searchTerm, setSearchTerm] = useState(""); // State for search term

  // Fetch messages when component mounts and refresh every 5 seconds
  useEffect(() => {
    fetchMessages();
    const interval = setInterval(fetchMessages, 5000);
    return () => clearInterval(interval);
  }, []);

  // Function to fetch the latest messages from the server
  const fetchMessages = async () => {
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      setMessages(data.slice(-10)); // Limit to last 10 messages
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  // Function to save username and move to chat screen
  const saveUsername = () => {
    if (username.trim()) {
      localStorage.setItem("username", username);
      setIsUsernameSet(true);
    }
  };

  // Function to send a new message to the server
  const sendMessage = async () => {
    if (!input.trim()) return;
    const newMessage = { username, text: input };
    setInput(""); // Clear input field after sending
    try {
      await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newMessage),
      });
      fetchMessages(); // Refresh messages after sending
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };
  // Function to filter messages based on the search term
  const filteredMessages = messages.filter((msg) =>
    msg.text.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ padding: "20px", maxWidth: "500px", margin: "auto" }}>
      {/* If no username is set, prompt user to enter one */}
      {!isUsernameSet ? (
        <div>
          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
          />
          <button
            onClick={saveUsername}
            style={{ width: "100%", padding: "10px", backgroundColor: "#007bff", color: "white", border: "none", cursor: "pointer" }}
          >
            Save Username
          </button>
        </div>
      ) : (
        <>
        {/* Search bar for filtering messages */}
        <input
            type="text"
            placeholder="Search messages..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "10px",
              border: "1px solid #ccc",
              borderRadius: "5px",
            }}
          />

          {/* Message display area */}
          <div style={{ height: "300px", overflowY: "auto", border: "1px solid #ccc", padding: "10px", marginBottom: "10px" }}>
          {filteredMessages.map((msg, index) => (
              <div
                key={index}
                style={{
                  padding: "5px",
                  backgroundColor: "#f1f1f1",
                  marginBottom: "5px",
                  borderRadius: "5px",
                }}
              >
                <strong>{msg.username}:</strong> {msg.text}
              </div>
            ))}
          </div>
          {/* Input field for typing messages */}
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
          />
          {/* Send button */}
          <button
            onClick={sendMessage}
            style={{ width: "100%", padding: "10px", backgroundColor: "#28a745", color: "white", border: "none", cursor: "pointer" }}
          >
            Send
          </button>
        </>
      )}
    </div>
  );
}