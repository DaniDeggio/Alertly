# Aletrly

**Aletrly – Innovation that Amplifies the Citizens' Voice**  
Aletrly revolutionizes the dialogue between citizens and public administrations. Through a simple and accessible platform, citizens can report issues and share their experiences. Public administrations, empowered by cutting-edge AI, gain real-time insights into the most pressing concerns, allowing them to act quickly and effectively to address problems.

### Technology serving the common good  
Aletrly harnesses the power of **Llama 3.1** running on **Groq** for high-performance, precise responses. With the integration of **LlamaIndex**, the platform implements **RAG (Retrieval-Augmented Generation)**, which queries an SQL database containing all citizen reports. When public administrations ask a question, the AI searches the database, gathering and combining the relevant information to deliver accurate and actionable insights, enabling informed decision-making.

With Aletrly, artificial intelligence is not just about technological innovation but becomes a practical tool for improving the lives of citizens, creating a more efficient, participatory, and responsive city ready to tackle future challenges.

---

## Setup Guide

### Backend Setup

1. **Create virtual environment**  
   Run the following command to create a virtual environment:
   ```bash
   python3 -m venv ~/venv/Ai

2. **Activate venv**
   ```bash
	source ~/venv/Ai/bin/activate

3. **Install dependencys**
   ```bash
	pip install -r requirements.txt

4. **Run backend**
   ```bash
	python3 Backend.py 


### Frontend Setup

   Run the following command:

1. **Install dependencys**  
   ```bash
   npm i

2. **Run frontend**
   ```bash
	npm run dev 