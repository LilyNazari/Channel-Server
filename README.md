# Art History Chat Application

This is a Flask-based chat application that allows users to discuss art history topics. It uses Flask as the backend, React as the frontend, and features user authentication, message posting, and off-topic detection with AI. The app integrates with a hub server for managing multiple chat channels and provides an interactive environment for discussing art, artists, and history.

## Features

- User authentication with Flask-Login.
- Dynamic message posting and retrieval.
- Off-topic detection using a machine learning model.
- Profanity filter to ensure clean discussions.
- React frontend for an interactive and user-friendly interface.
- AI-generated feedback based on the content of messages.

## Tech Stack

- **Backend**: Flask, Flask-Login, Flask-SQLAlchemy
- **Frontend**: React
- **Machine Learning**: Scikit-learn (Naive Bayes), TextBlob
- **Database**: SQLite (via Flask-SQLAlchemy)
- **Additional Libraries**: Flask-CORS, better_profanity, requests

## Setup Instructions

### Prerequisites

Make sure you have the following installed:

- Python (3.x)
- Node.js and npm
- Flask and other Python dependencies
- React and Node dependencies

### Endpoints

- /home: Displays a list of available chat channels.
- /show: Shows the messages from a specific channel.
- /post: Used to send a message to a channel.
- /health: Returns the health status of the server.
- / (GET): Returns a list of messages from the channel.
- / (POST): Receives a new message and processes it (checks profanity and off-topic content).

### Frontend Routes
- /: The main chat interface.
- /static/*: Serves static files (CSS, JS, images) from the React app.

### How It Works
- Chat Channels:
  Channels are fetched from a hub server using the /channels endpoint.
Each channel can have multiple messages, and users can post new messages.
- Off-Topic Detection
The system uses a Naive Bayes classifier to detect off-topic messages based on pre-defined training data.
Messages deemed off-topic are rejected.
- Profanity Filter
The app uses the better_profanity library to censor inappropriate words in messages.
- AI Feedback
When a user posts a message, the system analyzes the content for certain topics (like art, artists, painting styles) and responds with relevant AI-generated feedback.
