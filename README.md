# Financial Institution HR Policy Chatbot

A minimalist, powerful, and highly performant HR policy chatbot for employees of a financial institution. The chatbot uses a Retrieval-Augmented Generation (RAG) approach powered by Google's Gemini LLM to answer employee questions based on an internal policy knowledge base, with excellent Arabic language support.

## Features

- Single-page web application with clean, modern UI
- Right-to-Left (RTL) layout for Arabic
- Responsive and fast performance
- Retrieval-Augmented Generation (RAG) for accurate answers
- Minimalist design focused on core functionality

## Requirements

- Python 3.12 or higher
- Poetry for dependency management
- Google Gemini API key

## Setup

1. Clone the repository:
   ```
   git clone URL
   cd hr-policy-chatbot
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Create a `.env` file based on the provided `.env.example`:
   ```
   cp .env.example .env
   ```

4. Edit the `.env` file and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the application

   ```
   poetry run start
   ```
