# 🧠 Second Brain Graph App

This app lets you write notes and builds a graph of related ideas using an LLM (like Groq’s LLaMA models) and Neo4j AuraDB.

## ✨ Features

- Write natural language notes
- Extract relationships using LLM (Groq API)
- Store and visualize notes as a graph (Neo4j AuraDB + vis.js)
- Powered by Groq LLaMA via API

## 🛠 Requirements

- Python 3.8+
- [Neo4j AuraDB Free](https://neo4j.com/cloud/platform/aura-graph-database/) (cloud, no local install needed)
- Groq API key (get from [Groq Cloud](https://console.groq.com/))
- [pip](https://pip.pypa.io/en/stable/installation/)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file:**
   ```
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct

   NEO4J_URI=neo4j+s://<your-aura-id>.databases.neo4j.io
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_aura_password
   ```
   - Replace `<your-aura-id>` and `your_aura_password` with your AuraDB details.
   - Never commit your `.env` file!

## 🚀 Usage

1. **Run the app:**
   ```bash
   python app.py
   ```
2. **Open your browser and go to:**  
   [http://localhost:5000](http://localhost:5000)

3. **Write a note and submit!**  
   The app will extract relationships and visualize them as a graph.

## 🛡️ Security

- **Never commit your `.env` file or secrets to GitHub.**
- Always reset your API keys if they are accidentally exposed.

## 📝