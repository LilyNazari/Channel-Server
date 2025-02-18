import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const Chat = () => {
  const { channelName } = useParams();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    axios.get('http://localhost:5001/', {
      headers: {
        Authorization: 'authkey 1234567890'
      }
    })
    .then(response => {
      setMessages(response.data);
    })
    .catch(error => {
      console.error("Error fetching messages:", error);
    });
  }, []);

  const sendMessage = () => {
    const message = {
      content: newMessage,
      sender: "User", 
      timestamp: Date.now().toString()
    };

    axios.post('http://localhost:5001/', message, {
      headers: {
        Authorization: 'authkey 1234567890'
      }
    })
    .then(() => {
      setMessages([...messages, message]);
      setNewMessage('');
    })
    .catch(error => {
      console.error("Error sending message:", error);
    });
  };

  return (
    <div className="chat">
      <h2>{channelName}</h2>
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className="message">
            <strong>{msg.sender}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <input 
        type="text" 
        value={newMessage} 
        onChange={(e) => setNewMessage(e.target.value)} 
        placeholder="Type a message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default Chat;
