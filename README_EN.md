# 🍳 HowToCook-py-MCP 🥘 -- Your Weekly Meal Planner

English | [简体中文](./README.md)

> Turn your AI assistant into a personal chef that plans your daily meals!

This is a Python version of the recipe assistant MCP service, implemented using the FastMCP library. Based on [Anduin2017/HowToCook](https://github.com/Anduin2017/HowToCook), it enables AI assistants to recommend recipes and plan meals, solving the age-old question of "what to eat today"!

Special thanks to [worryzyy/HowToCook-mcp](https://github.com/worryzyy/HowToCook-mcp), as this Python version was inspired by their implementation 😄!

## 📸 Preview

![Feature Preview](img/01.png)

## 🔌 Supported MCP Clients

This server has been tested and works with the following clients:

- 📝 Cursor

## ✨ Features

This MCP server provides the following culinary tools:

1. **📚 Get All Recipes** (`get_all_recipes`) - Returns simplified data of all available recipes -- Use with caution as it creates a large context
2. **🔍 Get Recipes by Category** (`get_recipes_by_category`) - Query recipes by category: seafood? breakfast? meat dishes? staple food? All at your fingertips!
3. **🎲 What to Eat** (`what_to_eat`) - Perfect for the indecisive! Directly recommends today's menu based on the number of people
4. **🧩 Recommend Meal Plan** (`recommend_meals`) - Plans an entire week of delicious dishes based on your dietary restrictions, allergies, and number of diners

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.12.9+ 🐍
- Required Python dependencies 📦

### 💻 Installation Steps

1. Clone the repository

```bash
git clone https://github.com/DusKing1/howtocook-py-mcp.git
cd howtocook-py-mcp
```

2. Install dependencies (as simple as preparing ingredients!)

```bash
pip install -r requirements.txt
```

### ❓ Why not use uv?

You forget a thousand things everyday, how about make sure this is one of them?

## 🍽️ Getting Started

### 🔥 Start the Server

```bash
# Make sure you're in the project root directory
python -m src.app
```

The service will run on port 9000 using the SSE transmission protocol.

### 🔧 Configure your MCP Client

#### Quick Setup with Cursor

Add the MCP server configuration in Cursor settings:

```json
{
  "mcpServers": {
    "how to cook": {
      "url": "http://localhost:9000/sse"
    }
  }
}
```

#### Other MCP Clients

For other clients that support the MCP protocol, please refer to their respective documentation for configuration.

## 🧙‍♂️ Usage Guide

Here are example prompts for using the tools in various MCP clients:

### 1. 📚 Get All Recipes

No parameters needed, directly summon the cookbook!

```
Please use the howtocook-py-mcp MCP service to query all recipes
```

### 2. 🔍 Get Recipes by Category

```
Please use the howtocook-py-mcp MCP service to query seafood recipes
```

Parameters:

- `category`: Recipe category (seafood, breakfast, meat dishes, staple food, etc.)

### 3. 🎲 What to Eat?

```
Please use the howtocook-py-mcp MCP service to recommend a menu for 4 people for dinner
```

Parameters:

- `people_count`: Number of diners (1-10)

### 4. 🧩 Recommend Meal Plan

```
Please use the howtocook-py-mcp MCP service to recommend a week's worth of recipes for 3 people. We don't eat cilantro and are allergic to shrimp.
```

Parameters:

- `allergies`: List of allergens, e.g., ["garlic", "shrimp"]
- `avoid_items`: Foods to avoid, e.g., ["green onion", "ginger"]
- `people_count`: Number of diners (1-10)

## 📝 Tips

- This service is compatible with all AI assistants and applications that support the MCP protocol
- When using for the first time, the AI may need a little time to become familiar with how to use these tools (like heating up a wok!)

## 📄 Data Source

Recipe data comes from a remote JSON file, URL:
`https://mp-bc8d1f0a-3356-4a4e-8592-f73a3371baa2.cdn.bspapp.com/all_recipes.json`

## 🤝 Contribution

Feel free to Fork and submit Pull Requests. Let's improve this culinary assistant together!

## 📄 License

MIT License - Feel free to use it, just like sharing a recipe generously!

---

> 🍴 The feast is about to begin, is your appetite ready? 