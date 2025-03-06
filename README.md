# Banter - Real-Time Chat App
Banter is a real-time chat application built using FastAPI for the backend and WebSocket for real-time communication. It allows users to participate in live chats within specific contests, send messages, and toggle reactions on messages.

## Features
 - Real-time messaging within contests.
 - Message reactions (like, love, etc.).
 - RESTful API endpoints for retrieving messages and toggling reactions.

  
## Run the application

    uvicorn app.main:app --reload

## Directory Structure

├── app/
│ ├── __init__.py
│ ├── models/
│ │ ├── __init__.py
│ │ └── banter_message_model.py
│ ├── repositories/
│ │ ├── __init__.py
│ │ └── banter_message_repository.py
│ ├── schemas/
│ │ ├── __init__.py
│ │ └── banter_message_schema.py
│ ├── services/
│ │ ├── __init__.py
│ │ └── banter_message.py
│ ├── util/
│ │ ├── __init__.py
│ │ └── websocket_connection_manager.py
│ ├── __init__.py
│ ├── database.py
│ └── main.py
├── templates/
├── .env
└── .gitignore
