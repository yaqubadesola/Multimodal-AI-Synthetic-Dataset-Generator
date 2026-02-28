---
title: AI Synthetic Data Generator
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
git clone https://huggingface.co/spaces/yourusername/ai-synthetic-data-generator
cd ai-synthetic-data-generator

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenRouter API key
echo "OPENROUTER_API_KEY=your_key_here" > .env

# Run the app
python app.py
```

### Hugging Face Spaces Deployment

1. Upload all files (including app.py, requirements.txt, data_generator_lib.py, README.md) to your Hugging Face Space.
2. Set `app.py` as the entry point in your Space settings.
3. Add your `OPENROUTER_API_KEY` as a secret or environment variable in the Space.
4. The Gradio app and Inference API will be available at your Space URL.

#### Inference API Example

```python
import requests

API_URL = "https://hf.space/embed/<your-space-id>/api/predict"

payload = {
    "model_name": "OpenAI (GPT-4o Mini)",
    "dataset_type": "Customer Records",
    "size": 10
}
response = requests.post(API_URL, json=payload)
print(response.json())
```

---

For more details, see Hugging Face Spaces documentation.
