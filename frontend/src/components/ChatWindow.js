import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ChatWindow = ({ channelId }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    const fetchMessages = async () => {
      if (channelId) {
        const response = await axios.get(`http://127.0.0.1:5005/channels/${channelId}/messages`, {headers: {'Authorization': 'authkey 1234567890'}});
        setMessages(response.data);
      }
    };
    fetchMessages();
  }, [channelId]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (newMessage.trim() === '') return;
    
    await axios.post(`http://127.0.0.1:5005/channels/${channelId}/messages`, {headers: {'Authorization': 'authkey 1234567890'}}, {
      content: newMessage,
      user: 'User1', // Replace with dynamic user if you have authentication
    });

    setNewMessage('');
    // Refresh messages after sending
    const response = await axios.get(`http://127.0.0.1:5005/channels/${channelId}/messages` , {headers: {'Authorization': 'authkey 1234567890'}}); 
    setMessages(response.data);
  };

  return (
    <div className="flex flex-col h-full p-4 bg-gray-100 rounded-xl">
      <div className="flex-grow overflow-y-auto mb-4">
        {messages.map((message) => (
          <div key={message._id} className="mb-2">
            <span className="font-bold">{message.user}: </span>
            <span>{message.content}</span>
          </div>
        ))}
      </div>
      <form onSubmit={handleSendMessage} className="flex">
        <input
          type="text"
          className="flex-grow p-2 border rounded-l-xl"
          placeholder="Type a message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
        />
        <button type="submit" className="bg-blue-500 text-white p-2 rounded-r-xl">Send</button>
      </form>
    </div>
  );
};

export default ChatWindow;
