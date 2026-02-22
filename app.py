"""
================================================================================
🍳 GENERATIVE AI RECIPE GENERATOR - COMPLETE BACKEND WITH WEB INTERFACE
================================================================================
This file contains the complete Generative AI implementation for recipe generation.
Using Google Gemini 2.5 Flash - Latest and Fastest Model
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any
from enum import Enum
import hashlib
import time

# ==============================================================================
# GENERATIVE AI IMPORTS - CORE GEN AI
# ==============================================================================
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# ==============================================================================
# WEB FRAMEWORK IMPORTS
# ==============================================================================
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# ==============================================================================
# INITIALIZATION
# ==============================================================================
load_dotenv()

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# ==============================================================================
# GENERATIVE AI CONFIGURATION - USING GEMINI 2.5
# ==============================================================================

class GenAIConfig:
    """Generative AI Configuration - Updated for Gemini 2.5"""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Using Gemini 2.5 Flash - Fast and efficient for recipe generation
    # You can also use:
    # - "models/gemini-2.5-pro" for more detailed recipes
    # - "models/gemini-2.0-flash" for faster responses
    # - "models/gemini-flash-latest" for always using the latest flash model
    GEMINI_MODEL = "models/gemini-2.5-flash"  # Fast and capable
    
    GEMINI_TEMPERATURE = 0.8  # Creativity level (0.0 - 1.0)
    GEMINI_MAX_TOKENS = 2048  # Maximum response length
    GEMINI_TOP_P = 0.95
    GEMINI_TOP_K = 40
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = 30
    CACHE_TTL = 3600  # 1 hour

# ==============================================================================
# ENUMS FOR RECIPE CATEGORIES
# ==============================================================================

class CuisineType(str, Enum):
    ANY = "any"
    ITALIAN = "italian"
    ASIAN = "asian"
    MEXICAN = "mexican"
    INDIAN = "indian"
    MEDITERRANEAN = "mediterranean"
    AMERICAN = "american"

class DietaryRestriction(str, Enum):
    NONE = "none"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"

class MealType(str, Enum):
    ANY = "any"
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

# ==============================================================================
# GENERATIVE AI SERVICE - CORE IMPLEMENTATION
# ==============================================================================

class GenerativeAIService:
    """
    ============================================================================
    CORE GENERATIVE AI SERVICE - Using Gemini 2.5 Flash
    ============================================================================
    """
    
    def __init__(self):
        """Initialize the Generative AI service"""
        self.setup_logging()
        self.api_key = GenAIConfig.GEMINI_API_KEY
        self.model = None
        self.request_timestamps = []
        self.cache = {}
        
        # Initialize Gemini
        self.initialize_gemini()
        
        self.logger.info("✅ Generative AI Service initialized with Gemini 2.5")
    
    def setup_logging(self):
        """Setup logging for GenAI service"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("GenerativeAI")
    
    def initialize_gemini(self):
        """Initialize Google Gemini AI with Gemini 2.5"""
        try:
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            self.logger.info(f"📡 Connecting to Gemini model: {GenAIConfig.GEMINI_MODEL}")
            
            # Safety settings
            self.safety_settings = {
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            # Generation config
            self.generation_config = {
                "temperature": GenAIConfig.GEMINI_TEMPERATURE,
                "top_p": GenAIConfig.GEMINI_TOP_P,
                "top_k": GenAIConfig.GEMINI_TOP_K,
                "max_output_tokens": GenAIConfig.GEMINI_MAX_TOKENS,
            }
            
            # Initialize the model with Gemini 2.5 Flash
            self.model = genai.GenerativeModel(
                model_name=GenAIConfig.GEMINI_MODEL,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            # Quick test
            test_response = self.model.generate_content("Generate a simple recipe name")
            self.logger.info(f"✅ Gemini 2.5 connected successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Gemini AI: {str(e)}")
            raise
    
    def check_rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        self.request_timestamps = [t for t in self.request_timestamps if current_time - t < 60]
        
        if len(self.request_timestamps) >= GenAIConfig.MAX_REQUESTS_PER_MINUTE:
            return False
        
        self.request_timestamps.append(current_time)
        return True
    
    def generate_cache_key(self, ingredients: str, cuisine: str, dietary: str, meal_type: str, servings: int) -> str:
        """Generate cache key from request parameters"""
        content = f"{ingredients}_{cuisine}_{dietary}_{meal_type}_{servings}"
        return hashlib.md5(content.encode()).hexdigest()
    
    # ============================================================================
    # CORE GEN AI METHOD - PROMPT ENGINEERING
    # ============================================================================
    
    def build_recipe_prompt(self, ingredients: str, cuisine: str, dietary: str, meal_type: str, servings: int) -> str:
        """
        ============================================================================
        ADVANCED PROMPT ENGINEERING FOR GEMINI 2.5
        ============================================================================
        """
        
        prompt = f"""You are an expert professional chef. Create a delicious recipe using these ingredients: {ingredients}

RECIPE REQUIREMENTS:
- Cuisine: {cuisine if cuisine != 'any' else 'Any cuisine'}
- Dietary: {dietary if dietary else 'None'}
- Meal Type: {meal_type if meal_type else 'Any'}
- Servings: {servings} people

GUIDELINES:
1. Use the provided ingredients as main components
2. Only add essential pantry items (oil, salt, pepper, water) if needed
3. Make instructions clear and easy to follow
4. Include professional chef tips
5. Provide nutritional estimates

Return the recipe in this EXACT JSON format:
{{
    "name": "Creative recipe name",
    "description": "Brief appetizing description",
    "prep_time": "X minutes",
    "cook_time": "Y minutes",
    "total_time": "X+Y minutes",
    "difficulty": "Easy/Medium/Hard",
    "servings": {servings},
    "ingredients": [
        {{"name": "ingredient 1", "quantity": "amount", "unit": "unit"}},
        {{"name": "ingredient 2", "quantity": "amount", "unit": "unit"}}
    ],
    "instructions": [
        "Step 1: ...",
        "Step 2: ..."
    ],
    "tips": ["Tip 1", "Tip 2"],
    "nutrition": {{
        "calories": "approx per serving",
        "protein": "approx grams",
        "carbs": "approx grams",
        "fat": "approx grams"
    }}
}}

Return ONLY the JSON, no other text."""
        
        return prompt
    
    def parse_recipe_response(self, response_text: str, original_ingredients: str) -> Dict[str, Any]:
        """
        ============================================================================
        GENERATIVE AI RESPONSE PARSER
        ============================================================================
        """
        
        try:
            # Clean response
            cleaned_text = response_text.strip()
            
            # Remove markdown if present
            if "```json" in cleaned_text:
                cleaned_text = cleaned_text.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned_text:
                cleaned_text = cleaned_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            recipe_dict = json.loads(cleaned_text)
            
            # Ensure required fields
            required_fields = ['name', 'description', 'prep_time', 'cook_time', 
                              'ingredients', 'instructions']
            
            for field in required_fields:
                if field not in recipe_dict:
                    if field == 'ingredients':
                        recipe_dict[field] = []
                    elif field == 'instructions':
                        recipe_dict[field] = []
                    else:
                        recipe_dict[field] = "Not specified"
            
            return recipe_dict
            
        except Exception as e:
            self.logger.error(f"Parse error: {e}")
            return self.create_fallback_recipe(original_ingredients)
    
    def create_fallback_recipe(self, ingredients: str) -> Dict[str, Any]:
        """Create a fallback recipe when AI parsing fails"""
        ingredient_list = [i.strip() for i in ingredients.split(',')]
        
        return {
            "name": "Simple Home-Style Recipe",
            "description": "A delicious and easy-to-make dish using your ingredients",
            "prep_time": "15 minutes",
            "cook_time": "25 minutes",
            "total_time": "40 minutes",
            "difficulty": "Medium",
            "servings": 4,
            "ingredients": [{"name": ing, "quantity": "to taste", "unit": ""} for ing in ingredient_list],
            "instructions": [
                "Step 1: Prepare all ingredients by washing and chopping as needed",
                "Step 2: Heat oil in a pan and add aromatics (onion, garlic if available)",
                "Step 3: Add main ingredients and cook until done",
                "Step 4: Season with salt and pepper to taste",
                "Step 5: Serve hot and enjoy!"
            ],
            "tips": [
                "Feel free to adjust seasoning according to your taste",
                "Fresh herbs can elevate the flavor significantly"
            ],
            "nutrition": {
                "calories": "~350 kcal",
                "protein": "~20g",
                "carbs": "~30g",
                "fat": "~15g"
            }
        }
    
    # ============================================================================
    # MAIN GENERATIVE AI METHOD
    # ============================================================================
    
    def generate_recipe(self, ingredients: str, cuisine: str = "any", 
                       dietary: str = "", meal_type: str = "", servings: int = 4) -> Dict[str, Any]:
        """
        ============================================================================
        PRIMARY GENERATIVE AI METHOD - Using Gemini 2.5
        ============================================================================
        """
        
        self.logger.info(f"Generating recipe for: {ingredients}")
        
        # Check cache
        cache_key = self.generate_cache_key(ingredients, cuisine, dietary, meal_type, servings)
        if cache_key in self.cache:
            cache_time, cached_recipe = self.cache[cache_key]
            if time.time() - cache_time < GenAIConfig.CACHE_TTL:
                self.logger.info("Returning cached recipe")
                return cached_recipe
        
        # Check rate limit
        if not self.check_rate_limit():
            return {
                "error": "Rate limit reached. Please wait a minute.",
                "name": "Rate Limit Exceeded"
            }
        
        try:
            # Build prompt
            prompt = self.build_recipe_prompt(ingredients, cuisine, dietary, meal_type, servings)
            
            self.logger.info("📤 Sending request to Gemini 2.5...")
            
            # Call Gemini API
            response = self.model.generate_content(prompt)
            
            self.logger.info("📥 Received response from Gemini 2.5")
            
            # Parse response
            recipe = self.parse_recipe_response(response.text, ingredients)
            
            # Add metadata
            recipe['generated_at'] = datetime.now().isoformat()
            recipe['model_used'] = "Gemini 2.5 Flash"
            recipe['ingredients_used'] = ingredients
            
            # Cache the result
            self.cache[cache_key] = (time.time(), recipe)
            
            self.logger.info(f"✅ Recipe generated: {recipe.get('name')}")
            return recipe
            
        except Exception as e:
            self.logger.error(f"Recipe generation failed: {e}")
            return self.create_fallback_recipe(ingredients)

# ==============================================================================
# INITIALIZE GENERATIVE AI SERVICE
# ==============================================================================

try:
    genai_service = GenerativeAIService()
    print(f"✅ Using Gemini Model: {GenAIConfig.GEMINI_MODEL}")
except Exception as e:
    print(f"❌ Failed to initialize GenAI service: {e}")
    print("\nPlease check your GEMINI_API_KEY in the .env file")
    genai_service = None

# ==============================================================================
# FLASK ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Render the main webpage"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_recipe():
    """Generate recipe using Gemini 2.5 AI"""
    
    if not genai_service:
        return jsonify({'error': 'AI service not initialized. Check API key.'}), 503
    
    try:
        data = request.json
        ingredients = data.get('ingredients', '').strip()
        cuisine = data.get('cuisine', 'any')
        dietary = data.get('dietary', '')
        meal_type = data.get('meal_type', '')
        servings = int(data.get('servings', 4))
        
        if not ingredients:
            return jsonify({'error': 'Please enter ingredients'}), 400
        
        recipe = genai_service.generate_recipe(
            ingredients=ingredients,
            cuisine=cuisine,
            dietary=dietary,
            meal_type=meal_type,
            servings=servings
        )
        
        return jsonify(recipe)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'genai_model': GenAIConfig.GEMINI_MODEL,
        'genai_initialized': genai_service is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api-info')
def api_info():
    """API information"""
    return jsonify({
        'service': 'Generative AI Recipe Generator',
        'model': 'Gemini 2.5 Flash',
        'capabilities': [
            'Recipe generation from ingredients',
            'Multiple cuisine support',
            'Dietary restriction handling',
            'Nutritional estimation',
            'Chef tips generation'
        ],
        'rate_limit': f"{GenAIConfig.MAX_REQUESTS_PER_MINUTE} requests per minute"
    })

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     GENERATIVE AI RECIPE GENERATOR - GEMINI 2.5              ║
    ║           Powered by Google Gemini 2.5 Flash                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    if not GenAIConfig.GEMINI_API_KEY:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
        print("Please create a .env file with: GEMINI_API_KEY=your-api-key-here")
        exit(1)
    
    if genai_service:
        print(f"✅ Generative AI Service initialized with {GenAIConfig.GEMINI_MODEL}")
    else:
        print("❌ Failed to initialize Generative AI Service")
        exit(1)
    
    print("\n🚀 Starting web server...")
    print("🌐 Open your browser to: http://localhost:5000")
    print("📝 API documentation: http://localhost:5000/api-info")
    print("💻 Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)