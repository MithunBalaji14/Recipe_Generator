# check_models.py
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load your API key from .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API key not found in .env file!")
    print("Make sure your .env file contains: GEMINI_API_KEY=your-key-here")
    exit(1)

# Configure Gemini
genai.configure(api_key=api_key)

print("🔍 Checking available Gemini models...\n")
print("=" * 50)

# List all available models
for m in genai.list_models():
    print(f"📌 Model Name: {m.name}")
    print(f"   Display Name: {m.display_name}")
    print(f"   Supported Methods: {m.supported_generation_methods}")
    print("-" * 50)

print("\n✅ Done checking models!")