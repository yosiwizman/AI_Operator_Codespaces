# AI Operator - GitHub Codespaces Version

This is a powerful AI-based operator assistant that can chat, browse the web, automate on-screen tasks, and fetch stock market data. This version is optimized for **GitHub Codespaces** with built-in support for **GitHub Copilot, AI debugging, and cloud automation**.

## Features
✅ AI Chatbot (GPT-4)  
✅ Web Scraping & Automation (Selenium, Playwright)  
✅ GUI Automation (PyAutoGUI)  
✅ Stock Market Data Fetching (Alpha Vantage)  
✅ Memory Retention (Pinecone, ChromaDB)  
✅ Fully Integrated with GitHub Codespaces & Copilot  

## Getting Started

### **1. Open in GitHub Codespaces**
1. Click **Code** → **Codespaces** → **Create Codespace on Main**
2. Wait for the environment to start.

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set Up API Keys**
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_stock_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### **4. Run the Chatbot**
```bash
python src/chatbot/main.py
```

### **5. Run Web Scraper**
```bash
python src/browser_automation/web_scraper.py
```

### **6. Deploy Automatically with GitHub Actions**
The project is configured to auto-deploy using GitHub Actions. Just **push changes to GitHub**, and it will deploy.

## 🚀 Full Development Guide
For a complete guide, check the **docs/** folder.
