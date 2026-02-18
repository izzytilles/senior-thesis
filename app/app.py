from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_seasonal_produce(location, month):
    """
    Takes info about user's location and current month, queries seasonal.json, returns list of in-season produce 
    """

def generate_recipes(produce_list):
    """
    Constructs prompt, calls AI API (OpenAI via Azure for now), returns list of recipes
    """

def get_current_month():
    """
    Returns current month as a string
    """

def load_seasonal_produce():
    """
    Loads and parses seasonal.json at startup
    """


if __name__ == "__main__":
    app.run(debug=True)