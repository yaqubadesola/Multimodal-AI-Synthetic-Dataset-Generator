---
title: Multimodal AI Synthetic Data Generator
emoji: 🎭
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
---

# 🎭 Multimodal AI Synthetic Data Generator

Generate realistic synthetic datasets using multiple AI models via OpenRouter.

## ✨ Features

| Feature                | Description                                                                                   |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| 🤖 **Multiple Models** | OpenAI GPT-4o Mini, Gemini 1.5 Flash, Claude 3 Haiku, Mistral, Llama, DeepSeek, Qwen          |
| 📊 **5 Dataset Types** | Customer Records, Financial Transactions, Tax Records, Healthcare Patients, E-commerce Orders |
| 🔄 **Robust JSON**     | Automatic extraction from model responses with error recovery                                 |
| 📥 **CSV Export**      | Download generated data for immediate use                                                     |
| 🎨 **Clean UI**        | Intuitive Gradio interface with live preview                                                  |

## 🚀 Quick Start

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yaqubadesola/Multimodal-AI-Synthetic-Data-Generator-
cd Multimodal-AI-Synthetic-Data-Generator-

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenRouter API key
echo "OPENROUTER_API_KEY=your_key_here" > .env

# Run the app
python app.py
```

### Render Deployment

1. Push your code to GitHub (already done).
2. Go to [Render.com](https://render.com/) and create a new Web Service.
3. Connect your GitHub repository (`yaqubadesola/Multimodal-AI-Synthetic-Data-Generator-`).
4. Set the start command to `python app.py`.
5. Add your `OPENROUTER_API_KEY` as an environment variable in Render settings.
6. Choose a Python environment and build settings as needed.
7. Deploy! Your Gradio app will be available at your Render URL.

---

For more details, see Render documentation.
