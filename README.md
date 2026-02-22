# 🍳 Generative AI Recipe Generator

A powerful web application that uses **Google Gemini AI** to generate custom recipes based on ingredients you have at home. This project demonstrates the implementation of Generative AI in a real-world application.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Generative AI Implementation](#generative-ai-implementation)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Submission Guidelines](#submission-guidelines)
- [License](#license)

---

## 🎯 Project Overview

This Generative AI Recipe Generator allows users to input ingredients they have available, and using Google's Gemini AI model, it creates unique, personalized recipes. The application demonstrates:

- **Generative AI integration** with Google Gemini 1.5 Pro
- **Advanced prompt engineering** for structured recipe generation
- **Real-time web interface** with responsive design
- **Professional software architecture** with proper separation of concerns

---

## ✨ Features

### Core Generative AI Features
- ✅ **AI-Powered Recipe Generation** - Creates unique recipes from any ingredients
- ✅ **Multiple Cuisine Support** - Italian, Asian, Mexican, Indian, Mediterranean, and more
- ✅ **Dietary Restriction Handling** - Vegetarian, Vegan, Gluten-Free, etc.
- ✅ **Nutritional Estimation** - Approximate calories, protein, carbs, and fat
- ✅ **Professional Chef Tips** - AI-generated cooking tips and suggestions
- ✅ **Equipment Recommendations** - Suggests needed kitchen tools

### Technical Features
- ✅ **Rate Limiting** - 30 requests per minute to prevent API abuse
- ✅ **Caching Mechanism** - 1-hour cache for identical requests
- ✅ **Error Handling** - Graceful degradation with fallback recipes
- ✅ **Structured Logging** - Comprehensive logging for debugging
- ✅ **Input Validation** - Validates and sanitizes user inputs
- ✅ **Response Parsing** - Robust JSON parsing with fallbacks

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.3.3** - Web framework
- **Google Generative AI 0.3.0** - Gemini AI integration
- **python-dotenv** - Environment variable management
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with animations
- **JavaScript (ES6+)** - Client-side interactivity
- **Font Awesome 6** - Icons

### Development Tools
- **Virtual Environment (venv)** - Dependency isolation
- **Git** - Version control

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   ```bash
   python --version