import os
import json
import pandas as pd
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from data_generator_lib import DataGenerator, generate_data, extract_json_from_text, clean_response_text

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise EnvironmentError("OPENROUTER_API_KEY not found in .env file")

# Initialize OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Model configurations
MODELS = {
    "OpenAI (GPT-4o Mini)": "openai/gpt-4o-mini",
    "Gemini Flash": "google/gemini-2.5-flash",
    "Grok Beta": "x-ai/grok-3-mini",
    "Claude Haiku": "anthropic/claude-3-haiku-20240307",
    "DeepSeek V3": "deepseek/deepseek-r1"
}

def build_prompt(dataset_type, size):
    customer_example = '''[
  {
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "full_name": "John Smith",
    "email": "john.smith@email.com",
    "phone": "+1-555-123-4567",
    "country": "USA",
    "city": "New York",
    "postal_code": "10001",
    "signup_date": "2023-05-15"
  }
]'''
    transaction_example = '''[
  {
    "transaction_id": "TXN-8f3a2b1c",
    "account_id": "ACC-987654",
    "transaction_date": "2024-02-15",
    "amount": 47.85,
    "currency": "USD",
    "merchant_name": "Walmart",
    "merchant_category": "Groceries",
    "transaction_type": "debit",
    "status": "completed"
  }
]'''
    tax_example = '''[
  {
    "taxpayer_id": "TAX-123456",
    "full_name": "Jane Doe",
    "country": "USA",
    "annual_income": 75000,
    "tax_paid": 15750,
    "employment_status": "employed",
    "filing_status": "single",
    "tax_year": 2023
  }
]'''
    healthcare_example = '''[
  {
    "patient_id": "PAT-789012",
    "full_name": "Robert Johnson",
    "age": 58,
    "gender": "Male",
    "blood_type": "O+",
    "diagnosis": "Hypertension",
    "admission_date": "2023-11-10",
    "country": "Canada"
  }
]'''
    ecommerce_example = '''[
  {
    "order_id": "ORD-543210",
    "customer_id": "CUST-98765",
    "order_date": "2024-01-20",
    "product_name": "Wireless Headphones",
    "category": "Electronics",
    "quantity": 1,
    "price": 89.99,
    "payment_method": "credit_card",
    "shipping_country": "USA"
  }
]'''
    templates = {
        "Customer Records": f"""
Generate {size} realistic customer records as a JSON array.
**CRITICAL INSTRUCTION:** Return ONLY a valid JSON array. No explanations, no markdown formatting, no backticks, no additional text.
**REQUIRED FIELDS (each object must include):**
- customer_id: UUID format (e.g., "123e4567-e89b-12d3-a456-426614174000")
- full_name: string (first and last name)
- email: string (valid email format)
- phone: string (include country code, e.g., "+1-555-123-4567")
- country: string
- city: string
- postal_code: string
- signup_date: string (YYYY-MM-DD format, between 2020-01-01 and today)
**DATA RULES:**
- Use double quotes (\") for strings, not single quotes
- Include diverse, realistic values across different countries and cities
- Ensure all emails are properly formatted
**EXAMPLE OUTPUT:**
{customer_example}
Return ONLY the JSON array with {size} objects:
""",
        "Financial Transactions": f"""
Generate {size} realistic banking transactions as a JSON array.
**CRITICAL INSTRUCTION:** Return ONLY a valid JSON array. No explanations, no markdown formatting, no backticks, no additional text.
**REQUIRED FIELDS:**
- transaction_id: string (format: TXN- followed by random chars)
- account_id: string (format: ACC- followed by digits)
- transaction_date: string (YYYY-MM-DD, within last 30 days)
- amount: number (decimal with 2 places, $5-$500 for purchases, up to $5000 for transfers)
- currency: string (mostly "USD", occasional "EUR", "GBP")
- merchant_name: string
- merchant_category: string (e.g., "Groceries", "Restaurant", "Retail", "Utilities")
- transaction_type: string ("debit" or "credit", ~60% debit, 40% credit)
- status: string ("completed", "pending", or "failed", 95% completed)
**EXAMPLE OUTPUT:**
{transaction_example}
Return ONLY the JSON array:
""",
        "Tax Payer Records": f"""
Generate {size} realistic taxpayer records as a JSON array.
**CRITICAL INSTRUCTION:** Return ONLY a valid JSON array. No explanations, no markdown formatting, no backticks, no additional text.
**REQUIRED FIELDS:**
- taxpayer_id: string (format: TAX- followed by digits)
- full_name: string
- country: string
- annual_income: integer (should correlate with employment status)
- tax_paid: integer (roughly 15-30% of income)
- employment_status: string ("employed", "self-employed", "retired", "unemployed")
- filing_status: string ("single", "married_filing_jointly", "head_of_household")
- tax_year: integer (2023 or 2022)
**EXAMPLE OUTPUT:**
{tax_example}
Return ONLY the JSON array:
""",
        "Healthcare Patients": f"""
Generate {size} realistic patient records as a JSON array.
**CRITICAL INSTRUCTION:** Return ONLY a valid JSON array. No explanations, no markdown formatting, no backticks, no additional text.
**REQUIRED FIELDS:**
- patient_id: string (format: PAT- followed by digits)
- full_name: string
- age: integer (0-90, realistic distribution)
- gender: string ("Male", "Female", or "Other")
- blood_type: string (A+, A-, B+, B-, AB+, AB-, O+, O-)
- diagnosis: string (common conditions: hypertension, diabetes, asthma, etc.)
- admission_date: string (YYYY-MM-DD, within last 5 years)
- country: string
**EXAMPLE OUTPUT:**
{healthcare_example}
Return ONLY the JSON array:
""",
        "E-commerce Orders": f"""
Generate {size} realistic e-commerce orders as a JSON array.
**CRITICAL INSTRUCTION:** Return ONLY a valid JSON array. No explanations, no markdown formatting, no backticks, no additional text.
**REQUIRED FIELDS:**
- order_id: string (format: ORD- followed by digits)
- customer_id: string (format: CUST- followed by digits)
- order_date: string (YYYY-MM-DD, within last 90 days)
- product_name: string
- category: string (Electronics, Clothing, Books, Home & Garden, Sports, Beauty)
- quantity: integer (1-5)
- price: number (decimal with 2 places, realistic for category)
- payment_method: string ("credit_card", "paypal", "apple_pay", "google_pay")
- shipping_country: string
**EXAMPLE OUTPUT:**
{ecommerce_example}
Return ONLY the JSON array:
"""
    }
    if dataset_type not in templates:
        raise ValueError(f"Unknown dataset type: {dataset_type}")
    return templates[dataset_type]

# Create generator instance
generator = DataGenerator(client, MODELS, build_prompt)

DATASET_TYPES = [
    "Customer Records",
    "Financial Transactions",
    "Tax Payer Records",
    "Healthcare Patients",
    "E-commerce Orders"
]

def generate_dataset_ui(model_name, dataset_type, size):
    df = generator.generate(
        model_name=model_name,
        dataset_type=dataset_type,
        size=size,
        max_retries=3,
        temperature=0.4
    )
    filename = f"synthetic_{dataset_type.lower().replace(' ', '_')}_{size}.csv"
    df.to_csv(filename, index=False)
    return df, filename

def predict(model_name, dataset_type, size):
    """
    REST API endpoint for Render deployment.
    Returns JSON data.
    """
    df = generator.generate(
        model_name=model_name,
        dataset_type=dataset_type,
        size=size,
        max_retries=3,
        temperature=0.4
    )
    return df.to_dict(orient="records")

# Gradio app
with gr.Blocks(title="AI Synthetic Data Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎭 Multimodal AI Synthetic Data Generator")
    gr.Markdown("Generate realistic datasets using multiple AI models via OpenRouter.")
    with gr.Row():
        with gr.Column():
            model_dropdown = gr.Dropdown(
                choices=list(MODELS.keys()),
                value=list(MODELS.keys())[0],
                label="🤖 Select AI Model",
                info="Choose the AI model for generation"
            )
            dataset_dropdown = gr.Dropdown(
                choices=DATASET_TYPES,
                value=DATASET_TYPES[0],
                label="📊 Dataset Type",
                info="Select the type of synthetic data to generate"
            )
            size_slider = gr.Slider(
                minimum=5,
                maximum=50,
                value=50,
                step=5,
                label="📏 Number of Records",
                info="How many records to generate (5-50)"
            )
            generate_btn = gr.Button("🚀 Generate Dataset", variant="primary")
        with gr.Column():
            preview_output = gr.Dataframe(
                label="👁️ Data Preview",
                interactive=False,
                wrap=True
            )
            download_output = gr.File(
                label="📥 Download CSV",
                interactive=False
            )
    gr.Markdown("---")
    gr.Markdown("### 📋 Instructions")
    gr.Markdown("""
    1. Select an AI model from the dropdown
    2. Choose the type of dataset you want to generate
    3. Set the number of records (5-500)
    4. Click 'Generate Dataset' and wait a few seconds
    5. Preview the data and download as CSV
    """)
    generate_btn.click(
        fn=generate_dataset_ui,
        inputs=[model_dropdown, dataset_dropdown, size_slider],
        outputs=[preview_output, download_output]
    )
    gr.Markdown("---")
    gr.Markdown("Built with OpenRouter, Gradio, and ❤️ from Yaqub")

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
        debug=True
    )
