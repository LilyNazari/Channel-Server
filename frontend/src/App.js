import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
//import Home from './pages/Home';
import Chat from './pages/Chat';
import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import ChannelList from './components/ChannelList';
function App() {
  const [selectedChannel, setSelectedChannel] = useState(null);
  //const cors = require('cors');

  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/"/>
        <Route path="/chat/:channelName" element={<Chat />} />
      </Routes>
      <div className="flex h-screen p-4 bg-gray-200">
      <div className="w-1/4">
        <ChannelList onSelectChannel={setSelectedChannel} />
      </div>
      <div className="w-3/4"></div>
      {selectedChannel ? (
          <ChatWindow channelId={selectedChannel} />
        ) : (
          <p className="text-center text-gray-600"> </p>
        )}
        </div>
    </Router>
  );
}
//app.use(cors());
export default App;
