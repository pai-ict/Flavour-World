from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "a9295f34e81a4f59aa0268d1ba123a8b"

# Function to fetch recipes
def get_recipes(ingredient):
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&query={ingredient}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch recipes: {e}"}

# Function to fetch recipe details
def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch recipe details: {e}"}

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to search recipes based on an ingredient
@app.route('/search', methods=['POST'])
def search_recipes():
    ingredient = request.form['ingredient']
    if not ingredient:
        return jsonify({"error": "Please enter an ingredient."})
    
    recipes = get_recipes(ingredient)
    return jsonify(recipes)

# Route to get details of a recipe
@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    details = get_recipe_details(recipe_id)
    return jsonify(details)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Binding to all network interfaces
