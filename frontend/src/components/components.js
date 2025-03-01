import React, { useState, useEffect, useCallback } from "react";
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

  
// Fetch messages when component mounts and periodically
const fetchMessages =  useCallback(async () => {
  try {
    const response = await axios.get(CHANNEL_URL, { headers });
    const newMessages = response.data;
    setMessages(newMessages);
    // Update unread count
    const currentCount = newMessages.length - messages.length;
    if (currentCount > 0) setUnreadCount(prev => prev + currentCount);
  } catch (error) {
    console.error("Error fetching messages:", error);
  }
}, [messages.length]); 
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
    <div className="client-container">
      <h1 className="header">Chat Here!</h1>
      {/* If no username is set, prompt user to enter one */}
      {!isUsernameSet ? (
        <div>
          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="username-input"
          />
          <button
            onClick={saveUsername} className="button save-button"
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
            className="search-input"
          />
          {/* Unread messages*/}
          <div>
            <h3>Unread Messages<span className="unread-messages">{unreadCount > 0 && `(${unreadCount})`}</span></h3>
          </div>
          {/* Message display area */}
          <div className="messages-container">
          {filteredMessages.map((msg, index) => (
              <div
                key={index} 
                className="message"
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
            className="message-input"
          />
          {/* Send button */}
          <button
            onClick={sendMessage}
            className="button send-button"
          >
            Send
          </button>
        </>
      )}
    </div>
  );
}