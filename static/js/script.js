/**
 * ============================================================================
 * GENERATIVE AI RECIPE GENERATOR - MAIN JAVASCRIPT
 * ============================================================================
 * This file handles all frontend interactions with the Generative AI backend.
 */

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🍳 Recipe Generator UI loaded');
    checkBackendHealth();
});

/**
 * Check if backend is healthy
 */
async function checkBackendHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        if (data.status === 'healthy') {
            console.log('✅ Backend connected, using model:', data.genai_model);
        }
    } catch (error) {
        console.error('❌ Backend not responding:', error);
    }
}

/**
 * Main function to generate recipe using Generative AI
 */
async function generateRecipe() {
    // Get form values
    const ingredients = document.getElementById('ingredients').value;
    const cuisine = document.getElementById('cuisine').value;
    const mealType = document.getElementById('meal-type').value;
    const dietary = document.getElementById('dietary').value;
    const servings = document.getElementById('servings').value;

    // Validate input
    if (!ingredients.trim()) {
        showError('Please enter some ingredients!');
        return;
    }

    // Show loading state
    showLoading(true);
    hideEmptyState();

    try {
        // Call the Generative AI backend
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ingredients: ingredients,
                cuisine: cuisine,
                meal_type: mealType,
                dietary: dietary,
                servings: parseInt(servings)
            })
        });

        const recipe = await response.json();

        // Hide loading
        showLoading(false);

        // Display recipe
        if (recipe.error) {
            showError(recipe.error);
        } else {
            displayRecipe(recipe);
        }

    } catch (error) {
        console.error('Error:', error);
        showLoading(false);
        showError('Error connecting to Generative AI. Please try again.');
    }
}

/**
 * Display the generated recipe in the UI
 */
function displayRecipe(recipe) {
    const outputDiv = document.getElementById('recipe-output');

    // Build ingredients HTML
    let ingredientsHtml = '';
    if (recipe.ingredients && recipe.ingredients.length > 0) {
        recipe.ingredients.forEach(ing => {
            const name = ing.name || ing;
            const quantity = ing.quantity ? ` (${ing.quantity} ${ing.unit || ''})` : '';
            const notes = ing.notes ? `<br><small>${ing.notes}</small>` : '';
            
            ingredientsHtml += `
                <div class="ingredient-item">
                    <span class="ingredient-name">${name}</span>
                    <span class="ingredient-quantity">${quantity}</span>
                    ${notes}
                </div>
            `;
        });
    }

    // Build instructions HTML
    let instructionsHtml = '';
    if (recipe.instructions && recipe.instructions.length > 0) {
        recipe.instructions.forEach((step, index) => {
            // Clean up step text (remove "Step X:" if present)
            const cleanStep = step.replace(/^Step \d+:\s*/i, '');
            instructionsHtml += `
                <li class="instruction-step">
                    <span class="step-number">${index + 1}</span>
                    <span class="step-text">${cleanStep}</span>
                </li>
            `;
        });
    }

    // Build tips HTML
    let tipsHtml = '';
    if (recipe.tips && recipe.tips.length > 0) {
        tipsHtml = `
            <div class="tips-section">
                <h4><i class="fas fa-lightbulb"></i> Chef's Tips</h4>
                <ul>
                    ${recipe.tips.map(tip => `<li>${tip}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    // Build equipment HTML
    let equipmentHtml = '';
    if (recipe.equipment_needed && recipe.equipment_needed.length > 0) {
        equipmentHtml = `
            <h3 class="section-title"><i class="fas fa-tools"></i> Equipment Needed</h3>
            <div class="ingredients-list">
                ${recipe.equipment_needed.map(item => 
                    `<div class="ingredient-item"><span class="ingredient-name">${item}</span></div>`
                ).join('')}
            </div>
        `;
    }

    // Build nutrition HTML
    let nutritionHtml = '';
    if (recipe.nutrition) {
        nutritionHtml = `
            <h3 class="section-title"><i class="fas fa-chart-line"></i> Nutrition (approx per serving)</h3>
            <div class="nutrition-grid">
                <div class="nutrition-item">
                    <span class="nutrient">Calories</span>
                    <span class="value">${recipe.nutrition.calories || 'N/A'}</span>
                </div>
                <div class="nutrition-item">
                    <span class="nutrient">Protein</span>
                    <span class="value">${recipe.nutrition.protein || 'N/A'}</span>
                </div>
                <div class="nutrition-item">
                    <span class="nutrient">Carbs</span>
                    <span class="value">${recipe.nutrition.carbs || 'N/A'}</span>
                </div>
                <div class="nutrition-item">
                    <span class="nutrient">Fat</span>
                    <span class="value">${recipe.nutrition.fat || 'N/A'}</span>
                </div>
            </div>
        `;
    }

    // Format generation time
    const generatedTime = recipe.generated_at 
        ? new Date(recipe.generated_at).toLocaleString() 
        : new Date().toLocaleString();

    // Complete recipe HTML
    const recipeHtml = `
        <div class="recipe-card">
            <div class="recipe-header">
                <h2><i class="fas fa-utensils"></i> ${recipe.name || 'AI Generated Recipe'}</h2>
                <p class="recipe-description">${recipe.description || 'A delicious meal created from your ingredients'}</p>
                
                <div class="recipe-meta">
                    <div class="meta-item">
                        <span class="label"><i class="far fa-clock"></i> Prep</span>
                        <span class="value">${recipe.prep_time || '15'} min</span>
                    </div>
                    <div class="meta-item">
                        <span class="label"><i class="fas fa-clock"></i> Cook</span>
                        <span class="value">${recipe.cook_time || '25'} min</span>
                    </div>
                    <div class="meta-item">
                        <span class="label"><i class="fas fa-hourglass-half"></i> Total</span>
                        <span class="value">${recipe.total_time || '40'} min</span>
                    </div>
                    <div class="meta-item">
                        <span class="label"><i class="fas fa-chart-bar"></i> Difficulty</span>
                        <span class="value">${recipe.difficulty || 'medium'}</span>
                    </div>
                </div>
            </div>

            <h3 class="section-title"><i class="fas fa-shopping-basket"></i> Ingredients</h3>
            <div class="ingredients-list">
                ${ingredientsHtml || '<div class="ingredient-item">No ingredients specified</div>'}
            </div>

            <h3 class="section-title"><i class="fas fa-list-ol"></i> Instructions</h3>
            <ul class="instructions-list">
                ${instructionsHtml || '<li class="instruction-step">No instructions provided</li>'}
            </ul>

            ${equipmentHtml}
            ${tipsHtml}
            ${nutritionHtml}

            <div class="genai-footer">
                <i class="fas fa-microchip"></i> Generated by ${recipe.model_used || 'Google Gemini 1.5 Pro'} · 
                <i class="fas fa-code-branch"></i> Running in venv ·
                ${generatedTime}
            </div>
        </div>
    `;

    outputDiv.innerHTML = recipeHtml;
    
    // Scroll to recipe
    outputDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Show loading animation
 */
function showLoading(show) {
    const loadingDiv = document.getElementById('loading');
    const generateBtn = document.querySelector('.generate-btn');
    
    if (show) {
        loadingDiv.classList.add('active');
        generateBtn.disabled = true;
    } else {
        loadingDiv.classList.remove('active');
        generateBtn.disabled = false;
    }
}

/**
 * Hide empty state
 */
function hideEmptyState() {
    const emptyState = document.getElementById('empty-state');
    if (emptyState) {
        emptyState.style.display = 'none';
    }
}

/**
 * Show error message
 */
function showError(message) {
    const outputDiv = document.getElementById('recipe-output');
    outputDiv.innerHTML = `
        <div class="error-message">
            <i class="fas fa-exclamation-circle"></i>
            ${message}
        </div>
    `;
}

/**
 * Validate ingredients input
 */
function validateIngredients(ingredients) {
    const list = ingredients.split(',').map(i => i.trim()).filter(i => i);
    if (list.length === 0) {
        return { valid: false, message: 'Please enter at least one ingredient' };
    }
    if (list.length > 20) {
        return { valid: false, message: 'Too many ingredients (max 20)' };
    }
    return { valid: true, list: list };
}

/**
 * Copy recipe to clipboard
 */
function copyRecipe() {
    const recipeText = document.getElementById('recipe-output').innerText;
    navigator.clipboard.writeText(recipeText).then(() => {
        alert('Recipe copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

/**
 * Print recipe
 */
function printRecipe() {
    window.print();
}

/**
 * Save recipe as text file
 */
function saveRecipe(recipe) {
    const text = `
${recipe.name}
${'='.repeat(recipe.name.length)}

${recipe.description}

TIME: ${recipe.prep_time} min prep + ${recipe.cook_time} min cook = ${recipe.total_time} min
DIFFICULTY: ${recipe.difficulty}
SERVINGS: ${recipe.servings}

INGREDIENTS:
${recipe.ingredients.map(i => `- ${i.name}${i.quantity ? ` (${i.quantity})` : ''}`).join('\n')}

INSTRUCTIONS:
${recipe.instructions.map((step, i) => `${i+1}. ${step.replace(/^Step \d+:\s*/i, '')}`).join('\n')}

${recipe.tips ? 'TIPS:\n' + recipe.tips.map(t => `- ${t}`).join('\n') : ''}

Generated by Generative AI on ${new Date().toLocaleString()}
    `;

    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${recipe.name.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// Add keyboard shortcut (Ctrl+Enter) to generate
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();
        generateRecipe();
    }
});

// Add input character counter
const ingredientsInput = document.getElementById('ingredients');
if (ingredientsInput) {
    ingredientsInput.addEventListener('input', function() {
        const count = this.value.split(',').filter(i => i.trim()).length;
        const helpText = document.querySelector('.ingredient-help');
        if (helpText) {
            helpText.textContent = `${count} ingredients entered`;
        }
    });
}