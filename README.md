# Chat Server and Client

This repository contains the source code for a real-time chat application with a focus on art history discussions. The system is divided into two primary components:

Backend (Flask Server): Handles message exchange, channel management, user authentication, and feedback generation based on chat content.
Frontend (React App): Provides a user interface for chatting, displaying messages, and interacting with the server.
The backend and frontend are both integrated to work together seamlessly. The backend also supports AI-based message feedback and content moderation such as off-topic detection and profanity filtering.

##Table of Contents
Features
Installation
Backend Setup
Frontend Setup
Usage
Endpoints
License

## Features
Backend:
Channel Management: Registers and manages channels dynamically through the Hub.
User Authentication: Handles user management and login with Flask-Login.
Profanity Filtering: Messages are screened for inappropriate content using the better_profanity package.
Off-Topic Detection: An AI model based on Naive Bayes detects if a message is off-topic (e.g., not related to art history).
Feedback Generation: The server generates informative and random feedback about art, history, and artists based on chat messages.
Frontend:
Username Management: Users can set their username and it’s stored in localStorage.
Real-Time Messaging: Users can send and receive messages in real-time.
Search Functionality: Allows users to search through the chat messages.
Unread Message Counter: Tracks the number of unread messages.

# Usage
Backend:

The backend exposes a Flask API that interacts with the frontend and handles channels, user authentication, and message posting.
Routes include:
/home: Displays list of channels.
/show: Displays messages from a specific channel.
/post: Post a message to a channel.
/health: A health check endpoint to verify server status.
/: The main endpoint for fetching and sending messages.
Frontend:

The React app allows users to join a channel, set a username, send messages, and interact with the chat in real-time.
Features:
Search messages based on content.
View unread messages count.
Chat input with real-time feedback.
Endpoints
Backend API Routes:
GET /home: Retrieve the list of available channels.
GET /show: Retrieve messages for a specific channel.
Query Parameter: channel (required)
POST /post: Post a message to a channel.
Body Parameters: channel, content, sender, timestamp
GET /health: Check the health of the channel server.
GET /: Retrieve all messages for the channel.
POST /: Post a message to the channel with content validation.
Frontend React App:
Message Viewing: Displays the chat messages, allowing users to send and filter them.
Message Sending: Users can send messages which are posted to the backend.
Username Management: Prompts users to set their username.
