import React, { useCallback, useState, useEffect } from "react";
import axios from 'axios';
import "../App.css";


const CHANNEL_URL = "http://localhost:5001";  // Channel server URL
const headers = { "Authorization": "authkey 1234567890" };

export default function Client() {
  // State variables for messages, user input, and username
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [username, setUsername] = useState(localStorage.getItem("username") || "");
  const [isUsernameSet, setIsUsernameSet] = useState(!!localStorage.getItem("username"));
  const [searchTerm, setSearchTerm] = useState(""); // State for search term
  const [unreadCount, setUnreadCount] = useState(0);

  

  // Function to fetch the latest messages from the server
  const fetchMessages = useCallback(async () => {
    try {
      const response = await axios.get(CHANNEL_URL, { headers });
      const newMessages = response.data;
      setMessages(newMessages);
      // Update unread count
      const currentCount = newMessages.length - messages.length;
      if (currentCount > 0) setUnreadCount((prev) => prev + currentCount);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  }, [messages]); // Add messages as a dependency if necessary
  
  useEffect(() => {
    fetchMessages();
    const interval = setInterval(fetchMessages, 5000);
    return () => clearInterval(interval);
  }, [fetchMessages]);

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

    const messageData = {
      content: input,
      sender: username,
      timestamp: new Date().toISOString(),
    };

    try {
      await axios.post(CHANNEL_URL, messageData, { headers });
      setInput("");  // Clear input after sending
      fetchMessages();  // Refresh messages
      setUnreadCount(0);  // Reset unread count
    } catch (error) {
      console.error("Error sending message:", error);
      if (error.response?.status === 400) {
        alert(error.response.data); // Show error message from server
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  //Function to format the text
  const formatText = (text) => {
    return text
      .replace(/\[nop\]_(.*?)_\[\/nop\]/g, "<b>$1</b>")
      .replace(/\[nop\]\*(.*?)\*\[\/nop\]/g, "<i>$1</i>");
  };
  // Function to filter messages based on the search term
  const filteredMessages = messages.filter((msg) =>
    msg.content?.toLowerCase().includes(searchTerm.toLowerCase())
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
            style={{ width: "95%", padding: "10px", marginBottom: "10px", border: "1px solid #ccc", borderRadius: "5px" }}
          />
          {/* Unread messages*/}
          <div>
            <h3>Unread Messages<span style={{ color: "red" }}>{unreadCount > 0 && `(${unreadCount} new)`}</span></h3>
          </div>
          {/* Message display area */}
          <div style={{ height: "300px", overflowY: "auto", border: "1px solid #ccc", padding: "10px", marginBottom: "10px" }}>
          {filteredMessages.map((msg, index) => (
              <div
                key={index}
                style={{
                  padding: "10px",
                  backgroundColor: "#f1f1f1",
                  marginBottom: "5px",
                  borderRadius: "5px",
                }}
              >
                <strong>{msg.sender}:</strong> <span dangerouslySetInnerHTML={{ __html: formatText(msg.content) }} />
              </div>
            ))}
          </div>
          {/* Input field for typing messages */}
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            style={{ width: "95%", padding: "10px", marginBottom: "10px" }}
          />
          {/* Send button */}
          <button
            onClick={sendMessage}
            style={{ width: "99.5%", padding: "10px", backgroundColor: "#28a745", color: "white", border: "none", cursor: "pointer" }}
          >
            Send
          </button>
        </>
      )}
    </div>
  );
}