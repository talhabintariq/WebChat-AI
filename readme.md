# WebChat AI

This project is a chatbot that allows users to interact with website content directly, enabling question-answering based on loaded web pages. Built using OpenAI’s GPT-3.5-turbo and LangChain, it uses ChromaDB for storing and retrieving vectorized content and is designed with a simple Streamlit interface.

### Requirements

- Python 3.10
- OpenAI API Key
- Dependencies in `requirements.txt`

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/talhabintariq/chat-with-web.git
   cd chat-with-web
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   Add your OpenAI API key in a `.env` file:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the Chatbot**:
   ```bash
   streamlit run src/app.py
   ```

## How to Use

1. **Load a Website**: Enter a URL in the Streamlit app to load web content.
2. **Ask Questions**: Once loaded, ask questions about the content, and the bot will respond.
